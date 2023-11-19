import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import tw_stock_id
from sklearn.linear_model import LinearRegression
from common import DATA_START_YEAR, DATA_END_YEAR

class StockAnalizer :
    
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.plot_folder = os.path.abspath("./plot")
        os.makedirs(self.data_folder, exist_ok=True)
        self.performance = pd.DataFrame()
        self.rolling_trend = {}
    
    def plot_line(self, data, x_label, y_label):
        plt.figure(figsize=(10,10))  # dpi=100, 
        plt.plot(data[x_label], data[y_label])
        plt.xlabel(x_label)
        plt.ylabel(f"{y_label}")
        plt.gca().set_xticks(data[x_label].unique())
    
    def predict(self, data, x_label, y_label):
    
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        plt.scatter(x, y)
        
        x = x.reshape(-1, 1)
        model = LinearRegression(fit_intercept=True)
        model.fit(x, y)
        
        # Interception
        w_0 = model.intercept_
        # Coeficient
        w_1 = round(model.coef_[0], 2)
        
        
        
        prediction = model.predict(x)
        error = prediction - y
        rmse = (error**2).mean()**0.5
        mae = round(abs(error).mean(), 2)
        
        '''
        plot
        '''
        plt.plot(x, prediction, color = 'red')
        
        return w_1, mae
        
        
    def save_fig(self, indicator_name, stk_id, ):
        
        filepath = os.path.join(self.plot_folder, f"{stk_id}")
        os.makedirs(filepath, exist_ok=True)
        
        plt.title(f'{indicator_name} Indicator({stk_id})')
        plt.savefig(os.path.join(filepath, f"{indicator_name}_Indicator"))
        
        plt.clf()
    
    def process_balance_sheet(self, balance_sheet):
        
        balance_sheet = balance_sheet[["years", "stock" , "current_assets", "current_liabilities"]]
        
        for column in balance_sheet.columns:
            # special condition
            balance_sheet.drop(balance_sheet[balance_sheet[column] == "-"].index, inplace = True)
        balance_sheet = balance_sheet.astype(float)
        
        # sort data by year in descending order
        balance_sheet = balance_sheet[::-1]
        balance_sheet.reset_index(drop=True, inplace=True)
        
        balance_sheet["current_ratio(%)"] = (balance_sheet["current_assets"] / balance_sheet["current_liabilities"] * 100).round(2)
        balance_sheet["quick_ratio(%)"]   = ((balance_sheet["current_assets"] - balance_sheet["stock"]) / balance_sheet["current_liabilities"] * 100).round(2)
        
        return balance_sheet
    
    
    def process_profit_indicator(self, profit_indicator, stk_id):
        
        profit_indicator = profit_indicator[["years", "revenue(E)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]]
        
        for column in profit_indicator.columns:
            profit_indicator.drop(profit_indicator[profit_indicator[column] == "-"].index, inplace = True)
        
        profit_indicator = profit_indicator.astype(float)
        
        # sort data by year in descending order
        profit_indicator = profit_indicator[::-1]
        profit_indicator.reset_index(drop=True, inplace=True)
        profit_indicator['revenue(%)'] = round(profit_indicator['revenue(E)'] / profit_indicator['revenue(E)'].head(1)[0], 2)
        
        return profit_indicator
        
    def process_dividend_history(self, dividend_history):
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)
        return dividend_history
    
    def analyze_data(self, stk_list):
        
        # profit_features = ["revenue(%)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)"]
        # balance_features = ["current_ratio(%)", "quick_ratio(%)"]
        profit_features = ["revenue(%)", "gross_profit(%)", "net_income(%)"]

        for stk_id in stk_list :     
            print(stk_id)
            dividend_history, profit_indicator, balance_sheet, daily_close = self.load_data(stk_id=stk_id)
            
            # dividend_history = self.process_dividend_history(dividend_history=dividend_history)
            profit_indicator = self.process_profit_indicator(profit_indicator=profit_indicator.copy(), stk_id=stk_id)
            balance_sheet = self.process_balance_sheet(balance_sheet=balance_sheet.copy())
            
            filted_profit_indicator = profit_indicator[(DATA_START_YEAR<=profit_indicator['years']) & (profit_indicator['years'] <= DATA_END_YEAR) ].reset_index(drop=True)
            filted_balance_sheet = balance_sheet[(DATA_START_YEAR<=balance_sheet['years']) & (balance_sheet['years'] <= DATA_END_YEAR)].reset_index(drop=True)
            
            if not filted_profit_indicator.empty:
                if (filted_profit_indicator['years'][0] == DATA_START_YEAR) &  (filted_balance_sheet['years'][0] == DATA_START_YEAR):
                    # profit_features_mae = self.plot_trend_line(stk_id=stk_id, data=profit_indicator, features=profit_features)
                    # balance_features_mae = self.plot_trend_line(stk_id=stk_id, data=balance_sheet, features=balance_features)
                    # self.performance = pd.concat([self.performance, pd.DataFrame({**profit_features_mae, **balance_features_mae}, index=[stk_id])])
                    profit_features_mae = self.plot_trend_line(stk_id=stk_id, data=filted_profit_indicator, features=profit_features)
                    self.performance = pd.concat([self.performance, pd.DataFrame({**profit_features_mae}, index=[stk_id])])
                    self.gen_rolling_trend_line(stk_id=stk_id, data=profit_indicator, features=profit_features)
                    
                
        performance_folder = os.path.join(self.data_folder, 'performance')
        if not os.path.exists(performance_folder):
            os.makedirs(performance_folder)
            
        self.performance.to_csv(os.path.join(performance_folder, 'performance.csv'))

    def gen_rolling_trend_line(self, stk_id, data, features):
        
        data = data[(DATA_START_YEAR<=data['years'])].reset_index(drop=True)
        
        rolling_data = list(data.rolling(window=10))[9:]
        
        rolling_trend = pd.DataFrame()
        
        for data in rolling_data:
            
            data = data.reset_index(drop=True)
            
            rolling_result = {}
            for feature in features :
                coef, mae = self.predict(data=data, x_label="years", y_label=feature)
                rolling_result.update({f'{feature}_coef' : coef, f'{feature}_mae' : mae})
    
            start = int(data["years"].head(1).values[0])
            end = int(data["years"].tail(1).values[0])
            rolling_result.update({'period_start':start, 'period_end':end})
            rolling_trend = pd.concat([rolling_trend, pd.DataFrame(rolling_result, index=[0])])
            
        self.rolling_trend[stk_id] = rolling_trend
    
    def plot_trend_line(self, stk_id, data, features):
        
        result = {}
        for feature in features :
            self.plot_line(data=data, x_label="years", y_label=feature)
            coef, mae = self.predict(data=data, x_label="years", y_label=feature)
            self.save_fig(indicator_name=feature, stk_id=stk_id)
            plt.close('all')
            result.update({f'{feature}_coef' : coef, f'{feature}_mae' : mae})
        
        return result
    
    def load_data(self, stk_id):
        
        result = []
        
        for data_type in ['dividend_history', 'profit_indicator', 'balance_sheet', 'daily_close']:
            
            data_path = os.path.join(self.data_folder, data_type, f'{stk_id}.csv')
            data_exist = os.path.exists(data_path)
            
            if data_exist :
                data = pd.read_csv(data_path)
            
            result.append(data)
        
        return result
    
    def get_performance(self):
        return self.performance
    
    def get_rolling_trend(self):
        return self.rolling_trend
    
if __name__ == '__main__':
    
    stk_list = ['2330']#tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list)
    