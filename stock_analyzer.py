import pandas as pd
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import concurrent.futures
import statsmodels.api as sm
from common import (
    TREND_START_YEAR, TREND_END_YEAR, DataType, LoadedData, 
    PROFIT_FEATURES, PROFIT_RAW_DATA_COLUMNS, BALANCE_RAW_DATA_COLUMNS, ProfitIndicatorColumn,
    BalanceSheetColumn, TrendPrediction, get_stock_ids
)

DATA_LIST = [DataType.profit_indicator]
ROLLING_WINDOW_SIZE = 10

class StockAnalyzer :
    
    def __init__(self, industry, stk_list):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.performance = {}
        self.performance_path = os.path.join(self.data_folder, 'performance', industry)
        os.makedirs(self.performance_path, exist_ok=True)
        self.stk_list = stk_list
    
    def plot_trend(self, data:pd.DataFrame, x_label:str, y_label:str, trend_prediction:TrendPrediction, stk_id:str, filename:str='_'):
        
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
        plt.title(f'{y_label}_({stk_id})')
        
        filepath = os.path.join(self.trend_folder, f'{y_label}')
        os.makedirs(filepath, exist_ok=True)
        plt.savefig(os.path.join(filepath, f"{filename}"))
        plt.clf()
        plt.close('all')
    
    def predict_trend(self, data: pd.DataFrame, x_label: str, y_label: str) -> TrendPrediction:
    
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        
        # Intercept
        w_0 = model.params[0]
        # Coefficient
        slope = round(model.params[1], 2)
        
        prediction = model.predict(x)
        error = prediction - y
        rmse = (error**2).mean()**0.5
        mae = round(abs(error).mean(), 2)
        
        p_value = round(model.pvalues[1], 3)
        
        return TrendPrediction(slope=slope, mae=mae, prediction=prediction, p_value=p_value)
    
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
        
        if not profit_indicator.empty:
            # sort data by year in descending order
            profit_indicator = profit_indicator[::-1]
            profit_indicator.reset_index(drop=True, inplace=True)
            profit_indicator[ProfitIndicatorColumn.revenue_pct] = round(profit_indicator[ProfitIndicatorColumn.revenue] / profit_indicator[ProfitIndicatorColumn.revenue].head(1)[0], 2)
            profit_indicator = profit_indicator[(TREND_START_YEAR<=profit_indicator[ProfitIndicatorColumn.years])].reset_index(drop=True)
            return profit_indicator
        else:
            return pd.DataFrame()
        
    def process_dividend_history(self, dividend_history):
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)
        return dividend_history

    def gen_rolling_trends_line(self, stk_id:str, data:pd.DataFrame, features:list[str]):
        
        rolling_data = list(data.rolling(window=ROLLING_WINDOW_SIZE))[ROLLING_WINDOW_SIZE-1:]
        rolling_trends = pd.DataFrame()
        
        for data in rolling_data:
            data = data.reset_index(drop=True)
            start = int(data["years"].head(1).values[0])
            end = int(data["years"].tail(1).values[0])
            start_end = f'{start}-{end}'
            trend_result = {'stk_id':stk_id}
            
            for feature in features :
                trend_prediction = self.predict_trend(data=data, x_label="years", y_label=feature)
                trend_result.update({f'{feature}_slope' : trend_prediction.slope, f'{feature}_mae' : trend_prediction.mae, f'{feature}_p_value' : trend_prediction.p_value})
                self.plot_trend(data=data, x_label="years", y_label=feature, trend_prediction=trend_prediction, stk_id=stk_id, filename=start_end )    
            
            rolling_trends = pd.concat([rolling_trends, pd.DataFrame({**trend_result}, index=[start_end])])
            
        rolling_trends.to_csv(os.path.join(self.trend_folder, 'rolling_trend.csv'))
        return rolling_trends
    
    def load_data(self, stk_id:str) -> LoadedData:
        
        result = {}
        
        for data_type in DATA_LIST:
            data_path = os.path.join(self.data_folder, data_type, f'{stk_id}.csv')
            data_exist = os.path.exists(data_path)
            
            if data_exist :
                data = pd.read_csv(data_path)
            
            result[data_type] = data     
        return LoadedData(**result)
    
    
    def process_stk(self, stk_id):
        print(stk_id)
        loaded_data = self.load_data(stk_id=stk_id)
        profit_indicator = self.process_profit_indicator(profit_indicator=loaded_data.profit_indicator.copy())
        
        if not profit_indicator.empty:
            self.trend_folder = os.path.abspath(f"./trend_result/{stk_id}")
            os.makedirs(self.trend_folder, exist_ok=True)
            rolling_trends = self.gen_rolling_trends_line(stk_id=stk_id, data=profit_indicator, features=PROFIT_FEATURES)
            return rolling_trends
        else:
            return pd.DataFrame()

    def run_analysis_for_stk_list(self, stk_list):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # submit tasks for each stk_id
            futures = [executor.submit(self.process_stk, stk_id) for stk_id in stk_list]

        # wait for all tasks to complete
        concurrent.futures.wait(futures)
        return futures

    def parse_performance(self, futures):
        
        performance = {}
        # collect the results
        for future in futures:
            rolling_trends = future.result()
            for start_end, data in rolling_trends.iterrows():
                period_performance = performance.get(start_end, pd.DataFrame())
                stk_performance = pd.DataFrame({**data}, index=[0])
                performance[start_end] = pd.concat([period_performance, stk_performance])
        return performance
        
    def save_performance(self, performance):
        for key, data in performance.items():
            file_path = os.path.join(self.performance_path, f'{key}.csv')
            data.to_csv(file_path, index=False)

    
    def run_analysis(self):
        if not os.listdir(self.performance_path):
            stk_list = self.stk_list
            futures = self.run_analysis_for_stk_list(stk_list)
            performance = self.parse_performance(futures=futures)
            self.save_performance(performance=performance)

if __name__ == '__main__':
  
    stk_list_by_industries = get_stock_ids()
        
    for industry, stk_list in stk_list_by_industries.items():
        print(industry)
        analyzer = StockAnalyzer(industry=industry, stk_list=stk_list)
        analyzer.run_analysis()
    