import pandas as pd
import os
import tw_stock_id
import datetime
import matplotlib.pyplot as plt
from stock_analyzer import StockAnalizer
from common import DATA_START_YEAR, DATA_END_YEAR

class Backtester:
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        self.backtest_start_date = f'{DATA_START_YEAR + 10}-01-01'


    def init_benchmark_data(self):
        self.benchmark_data = self.load_data('0050')
        self.benchmark_data = self.benchmark_data[self.benchmark_data['Date'] > self.backtest_start_date].reset_index(drop=True)
        self.benchmark_data['Date'] = pd.to_datetime(self.benchmark_data['Date']).dt.date
        
        first_day_price = self.benchmark_data['Close'].head(1).values[0]
        self.benchmark_data['benchmark_updn(%)'] = round((self.benchmark_data['Close'] - first_day_price) /first_day_price*100  , 2)
        self.benchmark_data = self.benchmark_data[['Date', 'benchmark_updn(%)']]

    def load_data(self, stk_id):
        data_path = os.path.join(self.data_folder, 'daily_close', f'{stk_id}.csv')
        return pd.read_csv(data_path)
    
    
    def backtest(self, stk_id):
        
        target_data = self.load_data(stk_id)
        target_data = target_data[target_data['Date'] > self.backtest_start_date].reset_index(drop=True)
        target_data['Date'] = pd.to_datetime(target_data['Date']).dt.date
        first_day_price = target_data['Close'].head(1).values[0]
        target_data['updn(%)'] = round((target_data['Close'] - first_day_price) /first_day_price*100  , 2)
        
        testing_data = pd.merge(target_data, self.benchmark_data, how='left', on=['Date'])
        
        #plot   
        ax = testing_data.plot(x='Date', y = ['updn(%)', 'benchmark_updn(%)'], rot=45, figsize=(30,20), linewidth=3)

        plt.ticklabel_format(style='plain', axis='y')
        ax.set_title(f"{stk_id}",fontsize=32)
        ax.set_xlabel("Time",fontsize=30)
        ax.set_ylabel("Profit(%)",fontsize=30)
        plt.setp(ax.get_xticklabels(), fontsize=26)
        plt.setp(ax.get_yticklabels(), fontsize=26)
        
        filepath = os.path.join('./backtest')
        os.makedirs(filepath, exist_ok=True)
        
        # plt.title(f'{stk_id}')
        plt.savefig(os.path.join(filepath, f"{stk_id}"))
        plt.clf()
        plt.close('all')

    def select_good_stock(self, performance):
        good_stock_filter = (performance['net_income(%)_coef'] > 0) & (performance['gross_profit(%)_coef'] > 0)
        return performance[good_stock_filter].index
        
    def run_backtest(self, performance):
        self.init_benchmark_data()
        
        stk_list = self.select_good_stock(performance=performance)
        for stk_id in stk_list:
            self.backtest(stk_id=stk_id)

if __name__ == '__main__':
    
    stk_list = tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list)
    performance = analyzer.get_performance()
    
    backtester = Backtester()
    backtester.run_backtest(performance=performance)