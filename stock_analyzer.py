import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import tw_stock_id
from sklearn.linear_model import LinearRegression
from common import (
    TREND_START_YEAR, TREND_END_YEAR, DataType, LoadedData, BALANCE_FEATURES, 
    PROFIT_FEATURES, PROFIT_RAW_DATA_COLUMNS, BALANCE_RAW_DATA_COLUMNS, ProfitIndicatorColumn,
    BalanceSheetColumn, TrendPrediction
)

DATA_LIST = [DataType.dividend_history, DataType.profit_indicator, DataType.balance_sheet, DataType.daily_close]

class StockAnalizer :
    
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.plot_folder = os.path.abspath("./plot")
        os.makedirs(self.data_folder, exist_ok=True)
        self.performance = pd.DataFrame()
        self.rolling_trends = {}
        self.performance_folder = os.path.join(self.data_folder, 'performance')
        if not os.path.exists(self.performance_folder):
            os.makedirs(self.performance_folder)
    
    def plot_trend(self, data:pd.DataFrame, x_label:str, y_label:str, trend_prediction:TrendPrediction, stk_id:str):
        
        plt.figure(figsize=(10,10))  # dpi=100
        
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        x = x.reshape(-1, 1)
        
        # plot data line, data scatter and trend line
        plt.plot(data[x_label], data[y_label])
        plt.scatter(x, y)
        plt.plot(x, trend_prediction.prediction, color = 'red')

        plt.xlabel(x_label)
        plt.ylabel(f"{y_label}")
        plt.gca().set_xticks(data[x_label].unique())
        plt.title(f'{y_label} Indicator({stk_id})')
        
        filepath = os.path.join(self.plot_folder, f"{stk_id}")
        os.makedirs(filepath, exist_ok=True)
        plt.savefig(os.path.join(filepath, f"{y_label}_Indicator"))
        plt.clf()
        plt.close('all')
    
    def predict_trend(self, data:pd.DataFrame, x_label:str, y_label:str) -> TrendPrediction:
    
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        x = x.reshape(-1, 1)
        model = LinearRegression(fit_intercept=True)
        model.fit(x, y)
        
        # Interception
        w_0 = model.intercept_
        # Coeficient
        slope = round(model.coef_[0], 2)
        
        prediction = model.predict(x)
        error = prediction - y
        rmse = (error**2).mean()**0.5
        mae = round(abs(error).mean(), 2)
        
        return TrendPrediction(slope=slope, mae=mae, prediction=prediction)
    
    def process_balance_sheet(self, balance_sheet:pd.DataFrame) -> pd.DataFrame:
        
        balance_sheet = balance_sheet[BALANCE_RAW_DATA_COLUMNS]
        balance_sheet = self.drop_no_value_rows(data=balance_sheet)
        
        # sort data by year in descending order
        balance_sheet = balance_sheet[::-1]
        balance_sheet.reset_index(drop=True, inplace=True)
        
        balance_sheet[BalanceSheetColumn.current_ratio_pct] = (balance_sheet[BalanceSheetColumn.current_assets] / balance_sheet[BalanceSheetColumn.current_liabilities] * 100).round(2)
        balance_sheet[BalanceSheetColumn.quick_ratio_pct]   = ((balance_sheet[BalanceSheetColumn.current_assets] - balance_sheet[BalanceSheetColumn.stock]) / balance_sheet[BalanceSheetColumn.current_liabilities] * 100).round(2)
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
        profit_indicator[ProfitIndicatorColumn.revenue_pct] = round(profit_indicator[ProfitIndicatorColumn.revenue] / profit_indicator[ProfitIndicatorColumn.revenue].head(1)[0], 2)
        
        profit_indicator = profit_indicator[(TREND_START_YEAR<=profit_indicator[ProfitIndicatorColumn.years]) & (profit_indicator[ProfitIndicatorColumn.years] <= TREND_END_YEAR) ].reset_index(drop=True)
        
        return profit_indicator
        
    def process_dividend_history(self, dividend_history):
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)
        return dividend_history
    
    def run_analysis(self, stk_list:list[str]):

        for stk_id in stk_list :     
            print(stk_id)
            loaded_data = self.load_data(stk_id=stk_id)
            profit_indicator = self.process_profit_indicator(profit_indicator=loaded_data.profit_indicator.copy())
            
            if not profit_indicator.empty:
                profit_trends = self.gen_trends(data=profit_indicator, features=PROFIT_FEATURES, stk_id=stk_id)
                self.performance = pd.concat([self.performance, pd.DataFrame({**profit_trends}, index=[stk_id])])
                self.gen_rolling_trends_line(stk_id=stk_id, data=profit_indicator, features=PROFIT_FEATURES)
                
        self.performance.to_csv(os.path.join(self.performance_folder, 'performance.csv'))

    def gen_trends(self, data:pd.DataFrame, features:list[str], stk_id:str) -> dict[str, float]:
        trend_result = {}
        for feature in features :
            trend_prediction = self.predict_trend(data=data, x_label="years", y_label=feature)
            trend_result.update({f'{feature}_slope' : trend_prediction.slope, f'{feature}_mae' : trend_prediction.mae})
            self.plot_trend(data=data, x_label="years", y_label=feature, trend_prediction=trend_prediction, stk_id=stk_id)
        return trend_result

    def gen_rolling_trends_line(self, stk_id:str, data:pd.DataFrame, features:list[str]):
        
        data = data[(TREND_START_YEAR<=data['years'])].reset_index(drop=True)
        rolling_data = list(data.rolling(window=10))[9:]
        
        rolling_trends = pd.DataFrame()
        
        for data in rolling_data:
            data = data.reset_index(drop=True)
            rolling_result = {}
            for feature in features :
                trend_prediction = self.predict_trend(data=data, x_label="years", y_label=feature)
                rolling_result.update({f'{feature}_slope' : trend_prediction.slope, f'{feature}_mae' : trend_prediction.mae})
    
            start = int(data["years"].head(1).values[0])
            end = int(data["years"].tail(1).values[0])
            rolling_result.update({'period_start':start, 'period_end':end})
            rolling_trends = pd.concat([rolling_trends, pd.DataFrame(rolling_result, index=[0])])
            
        self.rolling_trends[stk_id] = rolling_trends
    
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
    analyzer.run_analysis(stk_list=stk_list)
    