import pandas as pd
import numpy as np
import os
import tw_stock_id
import datetime
import matplotlib.pyplot as plt
from stock_analyzer import StockAnalizer
from common import BACKTEST_START_DATE, STOP_LOSS_PCT

class Backtester:
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        self.backtest_result_path = os.path.join('./backtest')
        os.makedirs(self.backtest_result_path, exist_ok=True)


    def init_benchmark_data(self):
        self.benchmark_data = self.load_data('0050')
        self.benchmark_data = self.benchmark_data[self.benchmark_data['Date'] > BACKTEST_START_DATE].reset_index(drop=True)
        self.benchmark_data['Date'] = pd.to_datetime(self.benchmark_data['Date']).dt.date
        
        first_day_price = self.benchmark_data['Close'].head(1).values[0]
        self.benchmark_data['benchmark_updn(%)'] = round((self.benchmark_data['Close'] - first_day_price) /first_day_price*100  , 2)
        self.benchmark_data = self.benchmark_data[['Date', 'benchmark_updn(%)']]

    def load_data(self, stk_id):
        data_path = os.path.join(self.data_folder, 'daily_close', f'{stk_id}.csv')
        return pd.read_csv(data_path)
    
    
    def buy_and_hold(self, stk_id):
        
        target_data = self.load_data(stk_id)
        target_data = target_data[target_data['Date'] >= BACKTEST_START_DATE].reset_index(drop=True)
        target_data['Date'] = pd.to_datetime(target_data['Date']).dt.date
        first_day_price = target_data['Close'].head(1).values[0]
        target_data['updn(%)'] = round((target_data['Close'] - first_day_price) /first_day_price*100  , 2)
        
        testing_data = pd.merge(target_data, self.benchmark_data, how='left', on=['Date'])
        
        return testing_data
    
    def advanced_buy_and_hold(self, stk_id):
        target_data = self.load_data(stk_id)
        target_data = target_data[target_data['Date'] >= BACKTEST_START_DATE].reset_index(drop=True)
        target_data['Date'] = pd.to_datetime(target_data['Date']).dt.date
        
        # strategy
        first_day_price = target_data['Close'].head(1).values[0]
        last_close = 0
        position = False
        pnl = []
        
        last_peak_updn = 0
        cumsum_updn = 0
        stop_loss_price = 0
        
        for index, data in target_data.iterrows():
            
            # buy
            if not position and (data['Close'] > stop_loss_price): #*0.02
                position = True
            #hold
            else :
                pass
    
            if position:

                peaks = pd.Series(np.cumsum(pnl)).expanding().max()
                if not peaks.empty:
                    last_peak = peaks[index-1]
                    cumsum = np.cumsum(pnl)[-1] + (data['Close'] - last_close)
                    last_peak_updn = round((last_peak - first_day_price) /first_day_price*100, 2)
                    cumsum_updn = round((cumsum - first_day_price)/first_day_price*100, 2)

                # stop loss
                if (cumsum_updn - last_peak_updn) < -20:
                    position = False
                    stop_loss_price = data['Close']
                    profit = data['Close'] - last_close
                    last_close = stop_loss_price
                            
                # hold
                else :
                    profit = data['Close'] - last_close
                    last_close = data['Close'] 
            else :
                profit = 0
            
            pnl.append(profit)
            
        target_data['cumsum'] = np.cumsum(pnl)
        target_data['updn(%)'] = round((target_data['cumsum'] - first_day_price) /first_day_price*100, 2)
        testing_data = pd.merge(target_data, self.benchmark_data, how='left', on=['Date'])
        return testing_data
    
    def select_good_stock(self, performance):
        good_stock_filter = (performance['net_income(%)_coef'] > 0) & (performance['gross_profit(%)_coef'] > 0) & (performance['revenue(%)_coef'] > 0)
        return performance[good_stock_filter].index
        
    def run_backtest(self, performance, rolling_trends:dict[pd.DataFrame]):
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
        
        original_portfolio_profit['updn(%)'] = original_portfolio_profit['updn(%)']/ len(stk_list)
        self.plot_performance(data=original_portfolio_profit, columns=['updn(%)', 'benchmark_updn(%)'], title='original_portfolio')
        
        advanced_portfolio_profit['updn(%)'] = advanced_portfolio_profit['updn(%)']/ len(stk_list)
        self.plot_performance(data=advanced_portfolio_profit, columns=['updn(%)', 'benchmark_updn(%)'], title='advanced_portfolio')
    
    def calculate_portfolio_profit(self, portfolio_profit, result_data, profit_column):
        if portfolio_profit.empty:
            portfolio_profit['Date'] = result_data['Date']
            portfolio_profit['updn(%)'] = result_data[profit_column]
            portfolio_profit['benchmark_updn(%)'] = result_data['benchmark_updn(%)']
        else:
            portfolio_profit['updn(%)'] = portfolio_profit['updn(%)'] + result_data['updn(%)']
        return portfolio_profit

    def plot_performance(self, data:pd.DataFrame, columns:list[str], title:str):
        ax = data.plot(x='Date', y = columns, rot=45, figsize=(60,40), linewidth=3)
        plt.ticklabel_format(style='plain', axis='y')
        ax.set_title(f"{title}",fontsize=32)
        ax.set_xlabel("Time",fontsize=30)
        ax.set_ylabel("Profit(%)",fontsize=30)
        plt.setp(ax.get_xticklabels(), fontsize=26)
        plt.setp(ax.get_yticklabels(), fontsize=26)
        plt.savefig(os.path.join(self.backtest_result_path, f"{title}"))
        plt.clf()
        plt.close('all')


if __name__ == '__main__':
    
    stk_list = ['2302', '2329', '2330', '2340', '6202', '8271', '6271', '3041'] #tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list)
    performance = analyzer.get_performance()
    rolling_trends = analyzer.get_rolling_trends()
    
    backtester = Backtester()
    backtester.run_backtest(performance=performance, rolling_trends=rolling_trends)