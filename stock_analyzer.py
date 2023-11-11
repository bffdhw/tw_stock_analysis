import pandas as pd
import numpy as np
import os
import tw_stock_id
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class StockAnalizer :
    
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.plot_folder = os.path.abspath("./plot")
        os.makedirs(self.data_folder, exist_ok=True)
        self.evaluate = {}
    
    def plot_line(self, data, x_label, y_label):
        plt.figure(figsize=(10,10))  # dpi=100, 
        plt.plot(data[x_label], data[y_label])
        plt.xlabel(x_label)
        plt.ylabel(f"{y_label}")
        plt.gca().set_xticks(data[x_label].unique())
    
    def predict(self, data, x_label, y_label, stk_id):
    
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        plt.scatter(x, y)
        
        x = x.reshape(-1, 1)
        model = LinearRegression(fit_intercept=True)
        model.fit(x, y)
        
        w_0 = model.intercept_
        w_1 = model.coef_
        
        print('Interception : ', w_0)
        print('Coeficient : ', w_1)
        
        score = model.score(x, y)
        print('Score: ', score)
        print('Accuracy: ' + str(score*100) + '%')
        
        prediction = model.predict(x)
        error = prediction - y
        rmse = (error**2).mean()**0.5
        mae = abs(error).mean()
        self.evaluate[f'{stk_id}'] = {'mae' : mae, 'rmse' : rmse}
        
        '''
        plot
        '''
        plt.plot(x, prediction, color = 'red')
        
        
    def save_fig(self, indicator_name, stk_id):
        
        filepath = os.path.join(self.plot_folder, f"{stk_id}")
        os.makedirs(filepath, exist_ok=True)
        
        plt.title(f'{indicator_name} Indicator({stk_id})')
        plt.savefig(os.path.join(filepath, f"{indicator_name}_Indicator"))
        
        plt.clf()
    
    def process_balance_sheet(self, balance_sheet, stk_id):
        
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
    
    
    def process_profit_indicator(self, profit_indicator):
        
        for column in profit_indicator.columns:
            profit_indicator.drop(profit_indicator[profit_indicator[column] == "-"].index, inplace = True)
        
        profit_indicator = profit_indicator[["years", "revenue(E)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]].astype(float)
        
        # sort data by year in descending order
        profit_indicator = profit_indicator[::-1]
        profit_indicator.reset_index(drop=True, inplace=True)
        
        return profit_indicator
        
    def process_dividend_history(self, dividend_history):
    
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)

        return dividend_history
    
    def analyze_data(self, stk_list):
        
        profit_features = ["revenue(E)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)"]
        balance_features = ["current_ratio(%)", "quick_ratio(%)"]

        for stk_id in stk_list :
        
            dividend_history, profit_indicator, balance_sheet = self.load_data(stk_id=stk_id)
            
            # dividend_history = self.process_dividend_history(dividend_history=dividend_history)
            profit_indicator = self.process_profit_indicator(profit_indicator=profit_indicator)
            balance_sheet = self.process_balance_sheet(balance_sheet=balance_sheet, stk_id=stk_id)
            
            self.plot_trend_line(stk_id=stk_id, data=profit_indicator, features=profit_features)
            self.plot_trend_line(stk_id=stk_id, data=balance_sheet, features=balance_features)

    def plot_trend_line(self, stk_id, data, features):
        
        for feature in features :
            self.plot_line(data=data, x_label="years", y_label=feature)
            self.predict(data=data, x_label="years", y_label=feature, stk_id=stk_id)
            self.save_fig(indicator_name=feature, stk_id=stk_id)
                
        # for feature in balance_features :
        #     self.plot_line(data=balance_sheet, x_label="years", y_label=feature)
        #     self.predict(data=balance_sheet, x_label="years", y_label=feature, stk_id=stk_id)
        #     self.save_fig(indicator_name=feature, stk_id=stk_id)
    
    def load_data(self, stk_id):
        
        result = []
        
        for data_type in ['dividend_history', 'profit_indicator', 'balance_sheet']:
            
            data_path = os.path.join(self.data_folder, data_type, f'{stk_id}.csv')
            data_exist = os.path.exists(data_path)
            
            if data_exist :
                data = pd.read_csv(data_path)
            
            result.append(data)
        
        return result
    
if __name__ == '__main__':
    
    stk_list = tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list) 