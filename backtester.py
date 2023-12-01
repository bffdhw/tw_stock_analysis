import pandas as pd
import numpy as np
import os
import tw_stock_id
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from stock_analyzer import StockAnalizer
from common import BACKTEST_START_DATE, STOP_LOSS_PCT, BACKTEST_END_DATE

class Backtester:
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        self.backtest_result_path = os.path.join('./backtest')
        os.makedirs(self.backtest_result_path, exist_ok=True)


    def init_benchmark_data(self):
        self.benchmark_data = self.load_data('0050')
        self.benchmark_data = self.process_data(data=self.benchmark_data)
        
        first_day_price = self.benchmark_data['Close'].head(1).values[0]
        self.benchmark_data['benchmark_updn(%)'] = self.calculate_updn_pct(target_value=self.benchmark_data['Close'], baseline_value=first_day_price)
        self.benchmark_data = self.benchmark_data[['Date', 'benchmark_updn(%)']]

    def load_data(self, stk_id:str) -> pd.DataFrame:
        data_path = os.path.join(self.data_folder, 'daily_close', f'{stk_id}.csv')
        return pd.read_csv(data_path)
    
    def process_data(self, data:pd.DataFrame) -> pd.DataFrame:
        data = data[(BACKTEST_START_DATE <= data['Date']) & (data['Date'] <= BACKTEST_END_DATE)].reset_index(drop=True)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        return data
    
    def buy_and_hold(self, stk_id:str) -> pd.DataFrame:
        
        target_data = self.load_data(stk_id)
        target_data = self.process_data(data=target_data)
        first_day_price = target_data['Close'].head(1).values[0]
        target_data['updn(%)'] = self.calculate_updn_pct(target_value=target_data['Close'], baseline_value=first_day_price)
        
        testing_data = pd.merge(target_data, self.benchmark_data, how='left', on=['Date'])
        return testing_data
    
    def advanced_buy_and_hold(self, stk_id:str) -> pd.DataFrame:
        target_data = self.load_data(stk_id)
        target_data = self.process_data(data=target_data)
        
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
        target_data['updn(%)'] = self.calculate_updn_pct(target_value=target_data['cumsum'], baseline_value=first_day_price)
        testing_data = pd.merge(target_data, self.benchmark_data, how='left', on=['Date'])
        return testing_data
    
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
        good_stock_filter = (performance['net_income(%)_slope'] > 0) & (performance['gross_profit(%)_slope'] > 0) & (performance['revenue(%)_slope'] > 0)
        return list(performance[good_stock_filter].index)
        
    def run_backtest(self, performance:pd.DataFrame, rolling_trends:dict[pd.DataFrame]):
        self.init_benchmark_data()
        stk_list = self.select_good_stock(performance=performance)
        original_portfolio_profit = pd.DataFrame()
        advanced_portfolio_profit = pd.DataFrame()
        
        for stk_id in stk_list:
            buy_and_hold_result = self.buy_and_hold(stk_id=stk_id)
            advanced_result = self.advanced_buy_and_hold(stk_id=stk_id)
            
            result_data = buy_and_hold_result.copy()
            result_data['advanced_updn(%)'] = list(advanced_result['updn(%)'])
            
            original_portfolio_profit = self.calculate_portfolio_profit(portfolio_profit=original_portfolio_profit, result_data=result_data, profit_column='updn(%)')
            self.plot_performance(data=result_data, columns=['updn(%)', 'benchmark_updn(%)', 'advanced_updn(%)'], title=stk_id)
            advanced_portfolio_profit = self.calculate_portfolio_profit(portfolio_profit=advanced_portfolio_profit, result_data=result_data, profit_column='advanced_updn(%)')
        
        self.plot_portfolio_performance(data=original_portfolio_profit, title='original_portfolio')
        self.plot_portfolio_performance(data=advanced_portfolio_profit, title='advanced_portfolio')
    
    def plot_portfolio_performance(self, data, title):
        data['updn(%)'] = data['updn(%)'] / len(stk_list)
        self.plot_performance(data=data, columns=['updn(%)', 'benchmark_updn(%)'], title=title)
    
    def calculate_portfolio_profit(self, portfolio_profit, result_data, profit_column):
        if portfolio_profit.empty:
            portfolio_profit['Date'] = result_data['Date']
            portfolio_profit['updn(%)'] = result_data[profit_column]
            portfolio_profit['benchmark_updn(%)'] = result_data['benchmark_updn(%)']
        else:
            portfolio_profit['updn(%)'] = portfolio_profit['updn(%)'] + result_data['updn(%)']
        return portfolio_profit

    def plot_performance(self, data:pd.DataFrame, columns:list[str], title:str):
        ax = data.plot(x='Date', y = columns, rot=45, figsize=(50,30), linewidth=3)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
        ax.grid(True)
        ax.set_title(f"{title}",fontsize=42)
        ax.set_xlabel("Time",fontsize=38)
        ax.set_ylabel("Profit(%)",fontsize=38)
        plt.yticks(range(0, 800, 50))
        plt.ticklabel_format(style='plain', axis='y')
        plt.setp(ax.get_xticklabels(), fontsize=30)
        plt.setp(ax.get_yticklabels(), fontsize=30)
        plt.legend(columns, fontsize="40", loc ="upper left")
        plt.savefig(os.path.join(self.backtest_result_path, f"{title}"))
        plt.clf()
        plt.close('all')


if __name__ == '__main__':
    
    stk_list = ['2302', '2329', '2330', '2340', '6202', '8271', '6271', '3041'] #tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.run_analysis(stk_list=stk_list)
    performance = analyzer.get_performance()
    rolling_trends = analyzer.get_rolling_trends()
    
    backtester = Backtester()
    backtester.run_backtest(performance=performance, rolling_trends=rolling_trends)