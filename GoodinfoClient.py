
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:19:14 2021

@author: Longer
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class GoodinfoClient:
    
    def __init__(self) -> None:
        
        self.saves_folder = os.path.abspath("./saves")
        os.makedirs(self.saves_folder, exist_ok=True)
        
        self.evaluate = {}

    def get_profit_indicator(self, stk_id):
        
        url = f"https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={stk_id}" 
        
        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[3]/table[4]/tbody/tr/td/table/tbody/tr/td[1]/nobr[1]/select")
        options = element.find_elements(By.TAG_NAME, "option")
        options[0].click()
        tables = pd.read_html(driver.page_source)

        # process data
        df = tables[18]
        df.columns = df.columns.droplevel()
        df.columns = ["years", "capital(E)" , "financial_score" , "close" , "avg_price" , "updn" , "updn(%)" , "revenue(E)" , "gross_profit" , "operating_margin" , "other_income" , "net_income" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]

        drop_index = []
        for index in df.index :
            if (not df.iloc[index]["years"].isnumeric()):
                drop_index.append(index)
                
        df.drop(drop_index, inplace=True)
        
        return df
        
    def get_dividend_history(self, stk_id):
        
        url = f"https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={stk_id}" 
        
        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr/td[3]/table[4]/tbody/tr/td/table/tbody/tr/td[1]/nobr[1]/select")
        options = element.find_elements(By.TAG_NAME, "option")
        
        options[3].click() 
        
        tables = pd.read_html(driver.page_source)
        tables = pd.read_html(driver.page_source)
        
        # process data
        df = tables[18]
        df.columns = df.columns.droplevel()
        df.columns = df.columns.droplevel()
        df.columns = df.columns.droplevel()
        df.columns = ["years", "earnings(cash)",  "apic(cash)",  "total(cash)",  "earnings(stock)",  "apic(stock)",  "total(stock)",  "total(all)",  "total_value(cash)", "total_value(stock)",  "days_to_fill_cash",  "days_to_fill_stock", "price_year",  "high",  "low",  "avg",  "cash_dividend_yield(%)",  "stock_dividend_yield(%)", "total_dividend_yield(%)",  "dividend_year",  "eps",  "payout_ratio(cash)",  "payout_ratio(stock)",  "payout_ratio(total)"]

        drop_index = []
        for index in df.index :
            if (not df.iloc[index]["years"].isnumeric()):
                drop_index.append(index)
                
        df.drop(drop_index, inplace=True)
        
        if not os.path.exists('./data/dividend_history/'):
            os.makedirs('./data/dividend_history/')
            
        df.to_csv(f'./data/dividend_history/{stk_id}.csv')
        return df
    
    def get_balance_sheet(self, stk_id):
        
        url = f"https://goodinfo.tw/tw/StockAssetsStatus.asp?STOCK_ID={stk_id}" 

        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.ID, "divAssetsDetail")
        options = element.find_elements(By.TAG_NAME, "option")
        options[1].click()
        tables = pd.read_html(driver.page_source)

        # process data
        df = tables[15] #22
        df.columns = df.columns.droplevel()
        df.columns = ["years", "capital(E)" , "financial_score " , "last_year_close" , "current_year_close" , "updn(dolar)" , "updn(%)" , "cash" , "accounts_receivable" , "stock" , "current_assets" , "fund_investment" ,"fixed_asset" , "intangible_assets" , "other_assets" , "accounts_payable" , "current_liabilities" , "long_term_liabilities", "other_liabilities", "total_liabilities", "shareholder_equity(%)", "BPS(dolar)"]

        drop_index = []
        for index in df.index :
            if (not df.iloc[index]["years"].isnumeric()):
                drop_index.append(index)
                
        df.drop(drop_index, inplace=True)
        
        if not os.path.exists('./data/balance_sheet/'):
            os.makedirs('./data/balance_sheet/')
            
        df.to_csv(f'./data/balance_sheet/{stk_id}.csv')
        
        return df
    
    def process_balance_sheet(self, balance_sheet, stk_id):
        for column in balance_sheet.columns:
            
            # special condition
            if (stk_id == 6281) & (column == "long_term_liabilities") :
                pass
            else :
                balance_sheet.drop(balance_sheet[balance_sheet[column] == "-"].index, inplace = True)
            
        balance_sheet = balance_sheet[["years", "stock" , "current_assets", "current_liabilities"]].astype(float)
        
        # sort data by year in descending order
        balance_sheet = balance_sheet[::-1]
        balance_sheet.reset_index(drop=True, inplace=True)
        
        balance_sheet["current_ratio(%)"] = (balance_sheet["current_assets"] / balance_sheet["current_liabilities"] * 100).round(2)
        balance_sheet["quick_ratio(%)"]   = ((balance_sheet["current_assets"] - balance_sheet["stock"]) / balance_sheet["current_liabilities"] * 100).round(2)
        
        return balance_sheet
    
    
    def process_profit_data(self, profit_data):
        
        for column in profit_data.columns:
            profit_data.drop(profit_data[profit_data[column] == "-"].index, inplace = True)
        
        profit_data = profit_data[["years", "revenue(E)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]].astype(float)
        
        # sort data by year in descending order
        profit_data = profit_data[::-1]
        profit_data.reset_index(drop=True, inplace=True)
        
        return profit_data
        
    def process_dividend_history(self, dividend_history):
    
        dividend_history.drop(dividend_history[dividend_history["cash_dividend_yield(%)"] == "-"].index, inplace = True)
        dividend_history = dividend_history[["years","cash_dividend_yield(%)"]].astype(float).round(2)

        return dividend_history
    
    
    def analyze_profit_data(self):
        
        stk_list = [6281]   #3005, 8112, 1537, 2414, 4938, 
        profit_features = ["revenue(E)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)"]
        balance_features = ["current_ratio(%)", "quick_ratio(%)"]
        
        dividend_history_exists = os.path.exists('./data/dividend')
        balance_sheet_exists = os.path.exists('./data/balance_sheet')
        
        if not dividend_history_exists or not balance_sheet_exists:
        
            for stk_id in stk_list :
            
                dividend_history = self.get_dividend_history(stk_id=stk_id)
                dividend_history = self.process_dividend_history(dividend_history=dividend_history)
            
                profit_data = self.get_profit_indicator(stk_id=stk_id)
                profit_data = self.process_profit_data(profit_data=profit_data)
                
                for feature in profit_features :
                    self.plot_line(data=profit_data, x_label="years", y_label=feature)
                    self.predict(data=profit_data, x_label="years", y_label=feature, stk_id=stk_id)
                    self.save_fig(indicator_name=feature, stk_id=stk_id)
                    
                    
                balance_sheet = self.get_balance_sheet(stk_id=stk_id)
                balance_sheet = self.process_balance_sheet(balance_sheet=balance_sheet, stk_id=stk_id)
                
                for feature in balance_features :
                    self.plot_line(data=balance_sheet, x_label="years", y_label=feature)
                    self.predict(data=balance_sheet, x_label="years", y_label=feature, stk_id=stk_id)
                    self.save_fig(indicator_name=feature, stk_id=stk_id)
                    
                time.sleep(10)
        pass
            
    
    
    def plot_line(self, data, x_label, y_label):
        
        plt.figure(figsize=(10,10))  # dpi=100, 
        plt.plot(data[x_label], data[y_label])
        plt.xlabel(x_label)
        plt.ylabel(f"{y_label}")
        plt.gca().set_xticks(data[x_label].unique())
        
        pass
    
    def predict(self, data, x_label, y_label, stk_id):
    
        x = np.array(data[x_label])
        y = np.array(data[y_label])
        
        plt.scatter(x, y)
        
        x = x.reshape(-1, 1)
        
        '''
        ## 將數據集拆成訓練集與測試集
        # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 0)
        # model = LinearRegression(fit_intercept=True)
        # model.fit(X_train, y_train)
        
        
        # w_0 = model.intercept_
        # w_1 = model.coef_
        
        # print('Interception : ', w_0)
        # print('Coeficient : ', w_1)
        
        
        # score = model.score(X_test, y_test)
        # print('Score: ', score)
        # print('Accuracy: ' + str(score*100) + '%')
        '''
        
        ### new version
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
        
        filepath = os.path.join(self.saves_folder, f"{stk_id}")
        os.makedirs(filepath, exist_ok=True)
        
        plt.title(f'{indicator_name} Indicator({stk_id})')
        plt.savefig(os.path.join(filepath, f"{indicator_name}_Indicator"))
        
        plt.clf()
        
        
        


if __name__ ==  "__main__" :
    
    client = GoodinfoClient()
    client.analyze_profit_data()
    pass
