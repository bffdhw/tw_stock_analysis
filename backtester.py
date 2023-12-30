import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import copy
from common import BACKTEST_START_DATE, STOP_LOSS_PCT, BACKTEST_END_DATE

class Backtester:
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        self.backtest_result_path = os.path.join('./backtest')
        os.makedirs(self.backtest_result_path, exist_ok=True)
        self.performance_path = os.path.join(self.data_folder, 'performance')
        self.performance = self.load_performance()
        self.dynamic_portfolio_path = os.path.join(self.backtest_result_path, 'dynamic_portfolio')
        os.makedirs(self.dynamic_portfolio_path, exist_ok=True)

    def init_benchmark_data(self):
        self.benchmark_data = self.process_data(stk_id='0050', backtest_start=BACKTEST_START_DATE, backtest_end=BACKTEST_END_DATE)
        self.benchmark_data['benchmark_updn(%)'] = self.benchmark_data['updn(%)']
        self.benchmark_data = self.benchmark_data[['Date', 'benchmark_updn(%)']]

    def load_data(self, stk_id:str) -> pd.DataFrame:
        data_path = os.path.join(self.data_folder, 'daily_close', f'{stk_id}.csv')
        return pd.read_csv(data_path)
    
    def process_data(self, stk_id, backtest_start:str, backtest_end:str) -> pd.DataFrame:
        data = self.load_data(stk_id=stk_id)
        data = data[(backtest_start <= data['Date']) & (data['Date'] <= backtest_end)].reset_index(drop=True)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        first_day_price = data['Close'].head(1).values[0]
        data['updn(%)'] = self.calculate_updn_pct(target_value=data['Close'], baseline_value=first_day_price)
        return data
    
    
    def advanced_buy_and_hold(self, target_data) -> pd.DataFrame:
        
        # strategy
        first_day_price = target_data['Close'].head(1).values[0]
        last_cost = 0.0
        stop_loss_price = 0
        position = False
        pnl = []
        
        for _, data in target_data.iterrows():
            
            close_price = data['Close']
            # decide to buy, hold, or do nothing
            if not position and (close_price > stop_loss_price):
                position = True
            else :
                pass

            # calculate profit
            if position:
                profit = close_price - last_cost
                drawdown = self.calculate_drawdown(pnl=pnl, first_day_price=first_day_price, close_price=close_price, last_cost=last_cost)
                # stop loss
                if (drawdown) < STOP_LOSS_PCT:
                    position = False
                    stop_loss_price = close_price
                    last_cost = stop_loss_price         
                # hold
                else :
                    last_cost = close_price
            else :
                profit = 0
            
            pnl.append(profit)
            
        target_data['cumsum'] = np.cumsum(pnl)
        target_data['advanced_updn(%)'] = self.calculate_updn_pct(target_value=target_data['cumsum'], baseline_value=first_day_price)
        return target_data[['Date', 'advanced_updn(%)']]
    
    def calculate_drawdown(self, pnl:list[float], first_day_price:float, close_price:float, last_cost:float)-> float:
        peaks = pd.Series(np.cumsum(pnl)).expanding().max()
        if not peaks.empty:
            last_peak = peaks.tail(1).values[0]
            last_peak_updn_pct = self.calculate_updn_pct(target_value=last_peak, baseline_value=first_day_price)
            cumsum = np.cumsum(pnl)[-1] + (close_price - last_cost)
            cumsum_pct = self.calculate_updn_pct(target_value=cumsum, baseline_value=first_day_price)
            return cumsum_pct - last_peak_updn_pct
        else: 
            return 0.0
    
    def calculate_updn_pct(self, target_value, baseline_value):
        return round((target_value - baseline_value)/baseline_value*100, 2)
    
    def select_good_stock(self, performance:pd.DataFrame) -> list[str]:    
        portfolio_filter = (performance['net_income(%)_slope'] > 0) & (performance['gross_profit(%)_slope'] > 0) & (performance['revenue(%)_slope'] > 0)
        performance = performance[portfolio_filter]   
        return list(performance['stk_id'])
    
    def generate_portfolio(self) -> list[str]:
        result = {}
        for backtest_year, data in self.performance.items():
            portfolio_filter = (data['net_income(%)_slope'] > 0) & (data['gross_profit(%)_slope'] > 0) & (data['revenue(%)_slope'] > 0)
            data = data[portfolio_filter]
            result[backtest_year] = self.select_top_n(data=copy.deepcopy(data))
        return result
    
    def select_top_n(self, data):
        data['sum_slope'] = data['net_income(%)_slope'] + data['gross_profit(%)_slope'] + data['revenue(%)_slope']
        data['sum_mae'] = data['net_income(%)_mae'] + data['gross_profit(%)_mae'] + data['revenue(%)_mae']
        data = data[['stk_id', 'sum_slope', 'sum_mae']]
        fonts = self.non_dominated_sort(df=data)
        return fonts[0]
    
    def non_dominated_sort(self, df):
        dominating_count = {stk_id: 0 for stk_id in df['stk_id']}
        dominated_solutions = {stk_id: [] for stk_id in df['stk_id']}

        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                # Check if i dominates j
                is_dominated = df.iloc[i]['sum_slope'] >= df.iloc[j]['sum_slope'] and df.iloc[i]['sum_mae'] <= df.iloc[j]['sum_mae']
                # Check if j dominates i
                is_dominating = df.iloc[i]['sum_slope'] <= df.iloc[j]['sum_slope'] and df.iloc[i]['sum_mae'] >= df.iloc[j]['sum_mae']

                if is_dominated:
                    dominating_count[df.iloc[j]['stk_id']] += 1
                    dominated_solutions[df.iloc[i]['stk_id']].append(df.iloc[j]['stk_id'])
                elif is_dominating:
                    dominating_count[df.iloc[i]['stk_id']] += 1
                    dominated_solutions[df.iloc[j]['stk_id']].append(df.iloc[i]['stk_id'])

        fronts = []
        current_front = [stk_id for stk_id, count in dominating_count.items() if count == 0]

        while current_front:
            fronts.append(current_front)
            next_front = []
            for stk_id in current_front:
                for dominated_stk_id in dominated_solutions[stk_id]:
                    dominating_count[dominated_stk_id] -= 1
                    if dominating_count[dominated_stk_id] == 0:
                        next_front.append(dominated_stk_id)
            current_front = next_front

        return fronts
    
    
    def dynamic_portfolio_buy_and_hold(self, dynamic_portfolio) -> pd.DataFrame:
        
        adjust_portfolio_year = [2012, 2017, 2022]
        portfolios = {}
        cumsum_profit = pd.DataFrame()
        advanced_cumsum_profit = pd.DataFrame()
        last_period_cumsum = 0
        last_advanced_period_cumsum = 0
        
        for backtest_start_year in adjust_portfolio_year :
            period_cumsum_profit = pd.DataFrame()
            period_advanced_cumsum_profit = pd.DataFrame()
            portfolio = dynamic_portfolio[backtest_start_year]
            portfolios[backtest_start_year] = portfolio
            
            period_performance_path = os.path.join(self.dynamic_portfolio_path, f'{backtest_start_year}')
            os.makedirs(period_performance_path, exist_ok=True)
            print(portfolio)
            
            benchmark_data = self.process_data(stk_id='0050', backtest_start=f'{backtest_start_year}-04-01', backtest_end=f'{backtest_start_year+5}-03-31')
            benchmark_data = benchmark_data[['Date', 'updn(%)']]
            benchmark_data.columns = ['Date','benchmark_updn(%)']
            
            for stk_id in portfolio:
                target_data = self.process_data(stk_id=stk_id, backtest_start=f'{backtest_start_year}-04-01', backtest_end=f'{backtest_start_year+5}-03-31')
                
                updn = target_data['updn(%)']
                advanced_updn = self.advanced_buy_and_hold(target_data=target_data)['advanced_updn(%)']
                period_cumsum_profit[stk_id] = updn
                period_advanced_cumsum_profit[stk_id] = advanced_updn
                
                # plot stock performance
                period_stock_performance = pd.DataFrame()
                period_stock_performance['updn(%)'] = updn
                period_stock_performance['advanced_updn(%)'] = advanced_updn
                period_stock_performance['Date'] = target_data['Date']
                period_stock_performance = pd.merge(period_stock_performance, benchmark_data, how='left', on=['Date']).dropna()
                self.plot_performance(data=period_stock_performance, columns=['updn(%)' , 'advanced_updn(%)', 'benchmark_updn(%)'], title=f'{stk_id}', path=period_performance_path)
            
            period_cumsum_profit['portfolio'] = period_cumsum_profit.sum(axis=1) / len(portfolio) + last_period_cumsum
            period_cumsum_profit['advanced_portfolio'] = period_advanced_cumsum_profit.sum(axis=1) / len(portfolio) + last_advanced_period_cumsum
            period_cumsum_profit["Date"] = target_data['Date']
            period_cumsum_profit = pd.merge(period_cumsum_profit, benchmark_data, how='left', on=['Date']).dropna()
            
            # plot period performance
            plot_data = copy.deepcopy(period_cumsum_profit)
            plot_data['portfolio'] = plot_data['portfolio'] - last_period_cumsum
            plot_data['advanced_portfolio'] = plot_data['advanced_portfolio'] - last_advanced_period_cumsum
            self.plot_performance(data=plot_data, columns=['portfolio' , 'advanced_portfolio', 'benchmark_updn(%)'], title='period_portfolio', path=period_performance_path)
            
            cumsum_profit = pd.concat([cumsum_profit, period_cumsum_profit[['Date', 'portfolio']]])
            last_period_cumsum = cumsum_profit['portfolio'].tail(1).values[0]
            advanced_cumsum_profit = pd.concat([advanced_cumsum_profit, period_cumsum_profit[['Date', 'advanced_portfolio']]])
            last_advanced_period_cumsum = advanced_cumsum_profit['advanced_portfolio'].tail(1).values[0]
        cumsum_profit = cumsum_profit.reset_index(drop=True)
        advanced_cumsum_profit = advanced_cumsum_profit.reset_index(drop=True)
        
        portfolio_json_path = os.path.join(self.dynamic_portfolio_path, 'portfolios.json')
        with open(portfolio_json_path, 'w') as json_file:
            json.dump(portfolios, json_file)
        
        result = pd.merge(cumsum_profit, advanced_cumsum_profit, how='left', on=['Date']).dropna()
        result = pd.merge(result, self.benchmark_data, how='left', on=['Date']).dropna()
        return result
    
    
    def load_performance(self) -> dict[int, pd.DataFrame]:
        
        performance = {}
        for filename in os.listdir(self.performance_path):
            key = int(filename.split('.')[0].split('-')[1]) + 1
            performance[key] = pd.read_csv(os.path.join(self.performance_path, filename))
        return performance
    
    
    def run_dynamic_portfolio(self):
        dynamic_portfolio = self.generate_portfolio()
        result = self.dynamic_portfolio_buy_and_hold(dynamic_portfolio=dynamic_portfolio)
        self.plot_performance(data=result, columns=['portfolio', 'advanced_portfolio','benchmark_updn(%)'], title='portfolio', path=self.dynamic_portfolio_path)
    
    def run_fixed_portfolio(self):
        stk_list = self.select_good_stock(list(self.performance.values())[0])
        original_portfolio_profit = pd.DataFrame()
        advanced_portfolio_profit = pd.DataFrame()
        result_path = os.path.join(self.backtest_result_path, 'fixed_portfolio')
        os.makedirs(result_path, exist_ok=True)
        
        for stk_id in stk_list:
            target_data = self.process_data(stk_id=stk_id, backtest_start=BACKTEST_START_DATE, backtest_end=BACKTEST_END_DATE)
            buy_and_hold_result = target_data[['Date', 'updn(%)']]
            advanced_result = self.advanced_buy_and_hold(target_data=target_data)
            
            result_data = pd.merge(buy_and_hold_result, advanced_result, how='left', on=['Date'])
            result_data = pd.merge(result_data, self.benchmark_data, how='left', on=['Date'])
            self.plot_performance(data=result_data, columns=['updn(%)', 'benchmark_updn(%)', 'advanced_updn(%)'], title=stk_id, path=result_path)
            
            original_portfolio_profit = self.calculate_portfolio_profit(portfolio_profit=original_portfolio_profit, result_data=result_data, profit_column='updn(%)')
            advanced_portfolio_profit = self.calculate_portfolio_profit(portfolio_profit=advanced_portfolio_profit, result_data=result_data, profit_column='advanced_updn(%)')
        
        self.plot_portfolio_performance(data=original_portfolio_profit, title='original_portfolio', num_stocks=len(stk_list), path=result_path)
        self.plot_portfolio_performance(data=advanced_portfolio_profit, title='advanced_portfolio', num_stocks=len(stk_list), path=result_path)
    
    def plot_portfolio_performance(self, data, title, num_stocks, path):
        data['updn(%)'] = data['updn(%)'] / num_stocks
        self.plot_performance(data=data, columns=['updn(%)', 'benchmark_updn(%)'], title=title, path=path)
    
    def calculate_portfolio_profit(self, portfolio_profit, result_data, profit_column):
        if portfolio_profit.empty:
            portfolio_profit['Date'] = result_data['Date']
            portfolio_profit['updn(%)'] = result_data[profit_column]
            portfolio_profit['benchmark_updn(%)'] = result_data['benchmark_updn(%)']
        else:
            portfolio_profit['updn(%)'] = portfolio_profit['updn(%)'] + result_data[profit_column]
        return portfolio_profit

    def plot_performance(self, data:pd.DataFrame, columns:list[str], path, title:str):
        ax = data.plot(x='Date', y = columns, rot=45, figsize=(50,30), linewidth=3)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
        ax.grid(True)
        ax.set_title(f"{title}",fontsize=42)
        ax.set_xlabel("Time",fontsize=38)
        ax.set_ylabel("Profit(%)",fontsize=38)
        # plt.yticks(range(0, 800, 50))
        plt.ticklabel_format(style='plain', axis='y')
        plt.setp(ax.get_xticklabels(), fontsize=30)
        plt.setp(ax.get_yticklabels(), fontsize=30)
        plt.legend(columns, fontsize="40", loc ="upper left")
        plt.savefig(os.path.join(path, f"{title}"))
        plt.clf()
        plt.close('all')


    def run_backtest(self):
        self.init_benchmark_data()
        self.run_fixed_portfolio()
        self.run_dynamic_portfolio()

if __name__ == '__main__':
    backtester = Backtester()
    backtester.run_backtest()