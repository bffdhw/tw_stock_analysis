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

    
    def advanced_buy_and_hold(self, stk_id, rolling_trend):
        
        rolling_trend = rolling_trend[stk_id]
        filter = (rolling_trend['revenue(%)_coef'] > 0) & (rolling_trend['net_income(%)_coef'] > 0) & (rolling_trend['gross_profit(%)_coef'] > 0)
        filter = (rolling_trend['net_income(%)_coef'] > 0) & (rolling_trend['gross_profit(%)_coef'] > 0)
        signal = rolling_trend[filter]
        signal = list(signal['period_end']+1)
        
        target_data = self.load_data(stk_id)
        target_data = target_data[target_data['Date'] > BACKTEST_START_DATE].reset_index(drop=True)
        target_data['Date'] = pd.to_datetime(target_data['Date']).dt.date
        target_data['year'] = pd.to_datetime(target_data['Date']).dt.year
        grouped_data = list(target_data.groupby("year"))
        
        
        # strategy
        cumsum_pnl = pd.DataFrame()
        position = False
        first_day_price = grouped_data[0][1]['Close'].head(1).values[0]
        buy_price = 0
        realized_profit = 0
        realized = False
        for year, data in grouped_data:
            data = data.reset_index(drop=True)
            
            if year == 2019:
                pass
            
            if year in signal: 
                # buy
                if not position :
                    buy_price = data['Close'].head(1).values[0]
                    position = True
                # hold
                else:
                   pass
                
                data['cumsum_pnl'] = data['Close'] - buy_price 
                if realized:
                    data['cumsum_pnl'] = data['cumsum_pnl'] + realized_profit
            
            # no signal, do nothing
            else:
                if not position :
                    data['cumsum_pnl'] = cumsum_pnl['cumsum_pnl'].tail(1).values[0]
                    
                else :
                    data['cumsum_pnl'] = data['Close'] - buy_price 
                    if realized:
                        data['cumsum_pnl'] = data['cumsum_pnl'] + realized_profit
            
            
            ''' ############################################################ '''
            # stop loss logic
            if position:
                # stop loss
                period_first_price = data.head(1)['Close'].values[0]
                
                data['last_cumsum_pnl'] = data['cumsum_pnl'].shift(1)
                # cumsum_pnl = data.loc[data['last_cumsum_pnl'] != 0]['cumsum_pnl']
                # last_cumsum_pnl = data.loc[data['last_cumsum_pnl'] != 0]['last_cumsum_pnl']
                
                # data.loc[data['last_cumsum_pnl'] == 0, 'updn(%)'] = 0
                # data.loc[data['last_cumsum_pnl'] != 0, 'updn(%)'] = round((cumsum_pnl - last_cumsum_pnl) / last_cumsum_pnl *100, 2)
                
                data['updn(%)'] = round((data['Close'] - period_first_price) / period_first_price*100, 2)
                data = data.fillna(0)
                stop_loss_signal = data[data['updn(%)'] < STOP_LOSS_PCT]
                
                if not stop_loss_signal.empty:
                    stop_loss_date_index = stop_loss_signal.head(1).index[0]
                    
                    before_stop_loss_condition = data.index < stop_loss_date_index
                    after_stop_loss_condition = data.index >= stop_loss_date_index
                    
                    stop_loss_profit = data.loc[stop_loss_date_index]['Close'] - buy_price
                    data.loc[before_stop_loss_condition, 'cumsum_pnl'] = data.loc[before_stop_loss_condition]['Close'] - buy_price
                    data.loc[after_stop_loss_condition, 'cumsum_pnl'] = stop_loss_profit
                    
                    if realized:
                        data['cumsum_pnl'] = data['cumsum_pnl'] + realized_profit
                    
                    realized_profit += stop_loss_profit
                    
                    realized = True
                    position = False
                
                data = data.drop(['updn(%)'], axis=1)
            # else:
            #     data['cumsum_pnl'] = cumsum_pnl['cumsum_pnl'].tail(1).values[0]

            ''' ############################################################ '''
            
            cumsum_pnl = pd.concat([cumsum_pnl, data])
            cumsum_pnl['updn(%)'] = round(cumsum_pnl['cumsum_pnl'] / first_day_price * 100, 2)
        cumsum_pnl.to_csv('./aaa.csv')
        return cumsum_pnl
    
    
    def select_good_stock(self, performance):
        good_stock_filter = (performance['net_income(%)_coef'] > 0) & (performance['gross_profit(%)_coef'] > 0)
        return performance[good_stock_filter].index
        
    def run_backtest(self, performance, rolling_trend):
        self.init_benchmark_data()
        stk_list = self.select_good_stock(performance=performance)
        portfolio_profit = pd.DataFrame()
        
        for stk_id in stk_list:
            testing_data = self.buy_and_hold(stk_id=stk_id)
            advanced_result = self.advanced_buy_and_hold(stk_id=stk_id, rolling_trend=rolling_trend)
            testing_data['advanced_updn(%)'] = list(advanced_result['updn(%)'])
            
            if portfolio_profit.empty:
                portfolio_profit['Date'] = testing_data['Date']
                portfolio_profit['updn(%)'] = testing_data['updn(%)']
                portfolio_profit['benchmark_updn(%)'] = testing_data['benchmark_updn(%)']
            else:
                portfolio_profit['updn(%)'] = portfolio_profit['updn(%)'] + testing_data['updn(%)']
            
            self.plot_performance(data=testing_data, columns=['updn(%)', 'benchmark_updn(%)', 'advanced_updn(%)'], title=stk_id)
        
        portfolio_profit['updn(%)'] = portfolio_profit['updn(%)']/ len(stk_list)
        self.plot_performance(data=portfolio_profit, columns=['updn(%)', 'benchmark_updn(%)'], title='portfolio(without 3041)')
    
    def plot_performance(self, data:pd.DataFrame, columns:list[str], title:str):
        ax = data.plot(x='Date', y = columns, rot=45, figsize=(30,20), linewidth=3)
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
    
    stk_list = ['2302', '2329', '2330', '2340', '6202', '8271', '6271'] #tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list)
    performance = analyzer.get_performance()
    rolling_trend = analyzer.get_rolling_trend()
    
    backtester = Backtester()
    backtester.run_backtest(performance=performance, rolling_trend=rolling_trend)