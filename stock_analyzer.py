import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import tw_stock_id
from sklearn.linear_model import LinearRegression
from common import TREND_START_YEAR, TREND_END_YEAR, DataType, LoadedData, BALANCE_FEATURES, PROFIT_FEATURES, PROFIT_RAW_DATA_COLUMNS, BALANCE_RAW_DATA_COLUMNS

DATA_LIST = [DataType.dividend_history, DataType.profit_indicator, DataType.balance_sheet, DataType.daily_close]

class StockAnalizer :
    
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.plot_folder = os.path.abspath("./plot")
        os.makedirs(self.data_folder, exist_ok=True)
        self.performance = pd.DataFrame()
        self.rolling_trends = {}
    
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
    
    def process_balance_sheet(self, balance_sheet:pd.DataFrame) -> pd.DataFrame:
        
        balance_sheet = balance_sheet[BALANCE_RAW_DATA_COLUMNS]
        balance_sheet = self.drop_no_value_rows(data=balance_sheet)
        
        # sort data by year in descending order
        balance_sheet = balance_sheet[::-1]
        balance_sheet.reset_index(drop=True, inplace=True)
        
        balance_sheet["current_ratio(%)"] = (balance_sheet["current_assets"] / balance_sheet["current_liabilities"] * 100).round(2)
        balance_sheet["quick_ratio(%)"]   = ((balance_sheet["current_assets"] - balance_sheet["stock"]) / balance_sheet["current_liabilities"] * 100).round(2)
        balance_sheet = balance_sheet[(TREND_START_YEAR<=balance_sheet['years']) & (balance_sheet['years'] <= TREND_END_YEAR) ].reset_index(drop=True)
        
        return balance_sheet
    
    def drop_no_value_rows(self, data:pd.DataFrame) -> pd.DataFrame:
        
        for column in data.columns:
            data.drop(data[data[column] == "-"].index, inplace = True)
        
        return data.astype(float)
    
    def process_profit_indicator(self, profit_indicator:pd.DataFrame) -> pd.DataFrame:
        
        profit_indicator = profit_indicator[PROFIT_RAW_DATA_COLUMNS]
        profit_indicator = self.drop_no_value_rows(data=profit_indicator)
        
        # sort data by year in descending order
        profit_indicator = profit_indicator[::-1]
        profit_indicator.reset_index(drop=True, inplace=True)
        profit_indicator['revenue(%)'] = round(profit_indicator['revenue(100B)'] / profit_indicator['revenue(100B)'].head(1)[0], 2)
        
        profit_indicator = profit_indicator[(TREND_START_YEAR<=profit_indicator['years']) & (profit_indicator['years'] <= TREND_END_YEAR) ].reset_index(drop=True)
        
        return profit_indicator
        
    def process_dividend_history(self, dividend_history):
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)
        return dividend_history
    
    def analyze_data(self, stk_list:list[str]):

        for stk_id in stk_list :     
            print(stk_id)
            loaded_data = self.load_data(stk_id=stk_id)
            profit_indicator = self.process_profit_indicator(profit_indicator=loaded_data.profit_indicator.copy())
            balance_sheet = self.process_balance_sheet(balance_sheet=loaded_data.balance_sheet.copy())
            
            if not profit_indicator.empty and not balance_sheet.empty and ((profit_indicator['years'][0] == TREND_START_YEAR) & (balance_sheet['years'][0] == TREND_START_YEAR)):
                # balance_features_mae = self.plot_trend_line(stk_id=stk_id, data=balance_sheet, features=BALANCE_FEATURES)
                profit_features_mae = self.gen_trend(data=profit_indicator, features=PROFIT_FEATURES)
                self.plot_trend_line(stk_id=stk_id, data=profit_indicator, features=PROFIT_FEATURES)
                # self.performance = pd.concat([self.performance, pd.DataFrame({**profit_features_mae, **balance_features_mae}, index=[stk_id])])
                self.performance = pd.concat([self.performance, pd.DataFrame({**profit_features_mae}, index=[stk_id])])
                self.gen_rolling_trends_line(stk_id=stk_id, data=profit_indicator, features=PROFIT_FEATURES)
                
        performance_folder = os.path.join(self.data_folder, 'performance')
        if not os.path.exists(performance_folder):
            os.makedirs(performance_folder)
            
        self.performance.to_csv(os.path.join(performance_folder, 'performance.csv'))

    def gen_rolling_trends_line(self, stk_id:str, data:pd.DataFrame, features:list[str]):
        
        data = data[(TREND_START_YEAR<=data['years'])].reset_index(drop=True)
        rolling_data = list(data.rolling(window=10))[9:]
        
        rolling_trends = pd.DataFrame()
        
        for data in rolling_data:
            data = data.reset_index(drop=True)
            rolling_result = {}
            for feature in features :
                coef, mae = self.predict(data=data, x_label="years", y_label=feature)
                rolling_result.update({f'{feature}_coef' : coef, f'{feature}_mae' : mae})
    
            start = int(data["years"].head(1).values[0])
            end = int(data["years"].tail(1).values[0])
            rolling_result.update({'period_start':start, 'period_end':end})
            rolling_trends = pd.concat([rolling_trends, pd.DataFrame(rolling_result, index=[0])])
            
        self.rolling_trends[stk_id] = rolling_trends
    
    def gen_trend(self, data:pd.DataFrame, features:list[str]) -> dict[str, float]:
        
        result = {}
        for feature in features :
            coef, mae = self.predict(data=data, x_label="years", y_label=feature)
            result.update({f'{feature}_coef' : coef, f'{feature}_mae' : mae})
        
        return result

    def plot_trend_line(self, stk_id:str, data:pd.DataFrame, features:list[str]):
        for feature in features :
            self.plot_line(data=data, x_label="years", y_label=feature)
            _ , __ = self.predict(data=data, x_label="years", y_label=feature)
            self.save_fig(indicator_name=feature, stk_id=stk_id)
            plt.close('all')

    
    def load_data(self, stk_id:str) -> LoadedData:
        
        result = {}
        
        for data_type in DATA_LIST:
            data_path = os.path.join(self.data_folder, data_type, f'{stk_id}.csv')
            data_exist = os.path.exists(data_path)
            
            if data_exist :
                data = pd.read_csv(data_path)
            
            result[data_type] = data     
        return LoadedData(**result)
    
    def get_performance(self):
        return self.performance
    
    def get_rolling_trends(self):
        return self.rolling_trends
    
if __name__ == '__main__':
    
    stk_list = ['2330']#tw_stock_id.SEMICONDUCTOR
    analyzer = StockAnalizer()
    analyzer.analyze_data(stk_list=stk_list)
    