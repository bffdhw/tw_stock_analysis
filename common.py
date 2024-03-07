import pandas as pd
import numpy as np
import tw_stock_id
import time
import json
import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup

TREND_START_YEAR = 2002
TREND_END_YEAR = 2011
BACKTEST_START_DATE = f'{TREND_END_YEAR+1}-04-01'
BACKTEST_END_DATE = '2023-10-30'
STOP_LOSS_PCT = -20
RE_ENTRY_BUFFER_PCT = 5
SLIPPAGE_PCT = 0
ADJUST_PORTFOLIO_YEAR = [2012, 2017, 2022]
BUSINESS_CYCLE = 5

Y_FINANCE_INDUSTRIES_BASE_URL =  'https://tw.stock.yahoo.com/class-quote?sectorId='

INDUSTRIES = {'semiconductor' : 40, 'computer_peripherals' : 41, 'electronic_components' : 44, 'communication_network' : 43, 
              'other_electronics' : 47, 'plastic' : 3, 'shipping' : 20, 'optoelectronics' : 42, 'electromechanical' : 6}

STK_LIST = {
    'semiconductor' : tw_stock_id.SEMICONDUCTOR,
    'computer_peripherals' : tw_stock_id.COMPUTER_PERIPHERALS,
    'electronic_components' : tw_stock_id.ELECTRONIC_COMPONENTS,
    'food' : tw_stock_id.FOOD,
}


BALANCE_FEATURES = ["current_ratio(%)", "quick_ratio(%)"]
PROFIT_FEATURES = ["revenue(%)", "gross_profit(%)", "net_income(%)"]


PROFIT_RAW_DATA_COLUMNS = ["years", "revenue(100B)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]
BALANCE_RAW_DATA_COLUMNS = ["years", "stock" , "current_assets", "current_liabilities"]

class DataType:
    dividend_history = 'dividend_history'
    profit_indicator = 'profit_indicator'
    balance_sheet = 'balance_sheet'
    daily_close = 'daily_close'
    

class LoadedData:
    def __init__(self,  profit_indicator:pd.DataFrame):
        self.profit_indicator = profit_indicator

class ProfitIndicatorColumn:
    years = 'years'
    revenue = 'revenue(100B)'
    revenue_pct = 'revenue(%)'

class BalanceSheetColumn:
    years = 'years'
    current_ratio_pct = "current_ratio(%)"
    current_assets = "current_assets"
    current_liabilities = "current_liabilities"
    quick_ratio_pct = "quick_ratio(%)"
    stock = "stock"

class TrendPrediction:
    def __init__(self, slope, mae, prediction:np.ndarray, p_value):
        self.slope = slope
        self.mae = mae
        self.prediction = prediction
        self.p_value = p_value

class TransactionCostsPct:
    commission_pct =  0.001425 * 2
    tax_pct = 0.001
    
    
def get_stock_ids():
        
    file_name = 'stk_list_by_industries.json'
    stk_list_by_industries = {}
    file_path = os.path.join('data', file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            stk_list_by_industries = json.load(json_file)
    else:
        for industry, page_index in INDUSTRIES.items():
            url = f'{Y_FINANCE_INDUSTRIES_BASE_URL}{page_index}&exchange=TAI'
            driver = webdriver.Chrome()
            driver.get(url)
            
            # simulate scrolling the webpage to retrieve all stocks.
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            stk_list = soup.find_all(string=lambda text: '.TW' in text)[:-1]
            stk_list = [stk_id.split('.')[0] for stk_id in stk_list if stk_id.split('.')[0].isdigit()]
            stk_list_by_industries[industry] = stk_list
        
        with open(file_path, "w") as json_file:
            json.dump(stk_list_by_industries, json_file)
        
    return stk_list_by_industries

if __name__ ==  "__main__" :
    stk_list_by_industries = get_stock_ids()