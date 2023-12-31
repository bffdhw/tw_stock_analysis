import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from common import STK_LIST


BZ_PERFORMANCE_URL = 'https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID='
STOCK_ASSETS_STATUS_URL = 'https://goodinfo.tw/tw/StockAssetsStatus.asp?STOCK_ID='

DIVIDEND_ELEMENT_XPATH = '/html/body/table[2]/tbody/tr/td[3]/table[4]/tbody/tr/td/table/tbody/tr/td[1]/nobr[1]/select'
PROFIT_ELEMENT_XPATH = "/html/body/table[2]/tbody/tr/td[3]/table[4]/tbody/tr/td/table/tbody/tr/td[1]/nobr[1]/select"
ASSET_DETAIL_ELEMENT_ID = "divAssetsDetail"
OPTION_ELEMENT_TAG_NAME = "option"

GOODINFO_DIVIDEND_COLUMNS = ["years", "earnings(cash)",  "apic(cash)",  "total(cash)",  "earnings(stock)",  "apic(stock)",  "total(stock)",  "total(all)",  "total_value(cash)", "total_value(stock)",  "days_to_fill_cash",  "days_to_fill_stock", "price_year",  "high",  "low",  "avg",  "cash_dividend_yield(%)",  "stock_dividend_yield(%)", "total_dividend_yield(%)",  "dividend_year",  "eps",  "payout_ratio(cash)",  "payout_ratio(stock)",  "payout_ratio(total)"]
GOODINFO_BALANCE_COLUMNS  = ["years", "capital(100B)" , "financial_score " , "last_year_close" , "current_year_close" , "updn(dolar)" , "updn(%)" , "cash" , "accounts_receivable" , "stock" , "current_assets" , "fund_investment" ,"fixed_asset" , "intangible_assets" , "other_assets" , "accounts_payable" , "current_liabilities" , "long_term_liabilities", "other_liabilities", "total_liabilities", "shareholder_equity(%)", "BPS(dolar)"]
GOODINFO_PROFIT_COLUMNS   = ["years", "capital(100B)" , "financial_score" , "close" , "avg_price" , "updn" , "updn(%)" , "revenue(100B)" , "gross_profit" , "operating_margin" , "other_income" , "net_income" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]

DIVIDEND_HISTORY = 'dividend_history'
BALANCE_SHEET = 'balance_sheet'
PROFIT_INDICATOR = 'profit_indicator'

class GoodinfoClient:
    
    def __init__(self, industry:str) -> None:
        
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        
        self.dividend_history_folder = os.path.join(self.data_folder, DIVIDEND_HISTORY)
        if not os.path.exists(self.dividend_history_folder):
            os.makedirs(self.dividend_history_folder)
        
        self.balance_sheet_folder = os.path.join(self.data_folder, BALANCE_SHEET)
        if not os.path.exists(self.balance_sheet_folder):
            os.makedirs(self.balance_sheet_folder)
        
        self.profit_indicator_folder = os.path.join(self.data_folder, PROFIT_INDICATOR)
        if not os.path.exists(self.profit_indicator_folder):
            os.makedirs(self.profit_indicator_folder)
            
        self.stk_list = STK_LIST[industry]
        

    def get_profit_indicator(self, stk_id):
        
        url = f"{BZ_PERFORMANCE_URL}{stk_id}" 
        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.XPATH, PROFIT_ELEMENT_XPATH)
        options = element.find_elements(By.TAG_NAME, OPTION_ELEMENT_TAG_NAME)
        options[0].click()
        tables = pd.read_html(driver.page_source)

        # process data
        df = tables[18]
        df.columns = df.columns.droplevel()
        df.columns = GOODINFO_PROFIT_COLUMNS
        df = df[df['years'].str.isnumeric()]
            
        df.to_csv(os.path.join(self.profit_indicator_folder, f'{stk_id}.csv'), index=False)
        time.sleep(15)
        
    def get_dividend_history(self, stk_id:list[str]):
        
        url = f"{BZ_PERFORMANCE_URL}{stk_id}" 
        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.XPATH, DIVIDEND_ELEMENT_XPATH)
        options = element.find_elements(By.TAG_NAME, OPTION_ELEMENT_TAG_NAME)
        options[3].click()
        
        tables = pd.read_html(driver.page_source)
        tables = pd.read_html(driver.page_source)
        
        # process data
        df = tables[18]
        df.columns = df.columns.droplevel()
        df.columns = df.columns.droplevel()
        df.columns = df.columns.droplevel()
        df.columns = GOODINFO_DIVIDEND_COLUMNS
        df = df[df['years'].str.isnumeric()]
        
        df.to_csv(os.path.join(self.dividend_history_folder, f'{stk_id}.csv'), index=False)
        time.sleep(8)
    
    def get_balance_sheet(self, stk_id):
        
        url = f"{STOCK_ASSETS_STATUS_URL}{stk_id}" 
        driver = webdriver.Chrome()
        driver.get(url)

        element = driver.find_element(By.ID, ASSET_DETAIL_ELEMENT_ID)
        options = element.find_elements(By.TAG_NAME, OPTION_ELEMENT_TAG_NAME)
        options[1].click()
        tables = pd.read_html(driver.page_source)

        # process data
        df = tables[15] #22
        df.columns = df.columns.droplevel()
        df.columns = GOODINFO_BALANCE_COLUMNS
        df = df[df['years'].str.isnumeric()]
            
        df.to_csv(os.path.join(self.balance_sheet_folder, f'{stk_id}.csv'), index=False)
        time.sleep(8)
    
    def get_raw_data(self):
        
        # self.count = 0
        
        for stk_id in self.stk_list : 
            # dividend_history_exists = os.path.exists(os.path.join(self.data_folder, DIVIDEND_HISTORY, f'{stk_id}.csv'))
            # balance_sheet_exists = os.path.exists(os.path.join(self.data_folder, BALANCE_SHEET, f'{stk_id}.csv'))
            profit_indicator_exists = os.path.exists(os.path.join(self.data_folder, PROFIT_INDICATOR, f'{stk_id}.csv'))
            
            # if not dividend_history_exists : self.get_dividend_history(stk_id=stk_id)
            # if not balance_sheet_exists : self.get_balance_sheet(stk_id=stk_id)
            if not profit_indicator_exists : self.get_profit_indicator(stk_id=stk_id)
            
            # if self.count == 10:
            #     time.sleep(300)
            #     self.count = 0
            # self.count += 1
                
               
if __name__ ==  "__main__" :
    industry = 'electronic_components'
    client = GoodinfoClient()
    client.get_raw_data(industry=industry)
