import pandas as pd
import os
import time
import tw_stock_id
from selenium import webdriver
from selenium.webdriver.common.by import By

class GoodinfoClient:
    
    def __init__(self) -> None:
        
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        

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
        df.columns = ["years", "capital(100B)" , "financial_score" , "close" , "avg_price" , "updn" , "updn(%)" , "revenue(100B)" , "gross_profit" , "operating_margin" , "other_income" , "net_income" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]

        drop_index = []
        for index in df.index :
            if (not df.iloc[index]["years"].isnumeric()):
                drop_index.append(index)
                
        df.drop(drop_index, inplace=True)
        
        profit_indicator_folder = os.path.join(self.data_folder, 'profit_indicator')
        if not os.path.exists(profit_indicator_folder):
            os.makedirs(profit_indicator_folder)
            
        df.to_csv(os.path.join(profit_indicator_folder, f'{stk_id}.csv'), index=False)
        
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
        
        dividend_history_folder = os.path.join(self.data_folder, 'dividend_history')
        if not os.path.exists(dividend_history_folder):
            os.makedirs(dividend_history_folder)
            
        df.to_csv(os.path.join(dividend_history_folder, f'{stk_id}.csv'), index=False)
    
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
        df.columns = ["years", "capital(100B)" , "financial_score " , "last_year_close" , "current_year_close" , "updn(dolar)" , "updn(%)" , "cash" , "accounts_receivable" , "stock" , "current_assets" , "fund_investment" ,"fixed_asset" , "intangible_assets" , "other_assets" , "accounts_payable" , "current_liabilities" , "long_term_liabilities", "other_liabilities", "total_liabilities", "shareholder_equity(%)", "BPS(dolar)"]

        drop_index = []
        for index in df.index :
            if (not df.iloc[index]["years"].isnumeric()):
                drop_index.append(index)
                
        df.drop(drop_index, inplace=True)
        
        balance_sheet_folder = os.path.join(self.data_folder, 'balance_sheet')
        if not os.path.exists(balance_sheet_folder):
            os.makedirs(balance_sheet_folder)
            
        df.to_csv(os.path.join(balance_sheet_folder, f'{stk_id}.csv'), index=False)
        
    
    def get_raw_data(self, stk_list):
        
        for stk_id in stk_list : 
            dividend_history_exists = os.path.exists(os.path.join(self.data_folder, 'dividend_history', f'{stk_id}.csv'))
            balance_sheet_exists = os.path.exists(os.path.join(self.data_folder, 'balance_sheet', f'{stk_id}.csv'))
            profit_indicator_exists = os.path.exists(os.path.join(self.data_folder, 'profit_indicator', f'{stk_id}.csv'))
            
            if dividend_history_exists and balance_sheet_exists and profit_indicator_exists:
                continue
            else:
                self.get_dividend_history(stk_id=stk_id)
                time.sleep(3)
                self.get_balance_sheet(stk_id=stk_id)
                time.sleep(3)
                self.get_profit_indicator(stk_id=stk_id)
                time.sleep(3)
            
            # time.sleep(5)
                
               
if __name__ ==  "__main__" :
    
    try:
        stk_list = tw_stock_id.SEMICONDUCTOR
        client = GoodinfoClient()
        client.get_raw_data(stk_list=stk_list)
    except:
        pass
