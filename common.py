import pandas as pd
import numpy as np
import tw_stock_id

TREND_START_YEAR = 2002
TREND_END_YEAR = 2011
BACKTEST_START_DATE = f'{TREND_END_YEAR+1}-04-01'
BACKTEST_END_DATE = '2023-10-30'
STOP_LOSS_PCT = -20
RE_ENTRY_BUFFER_PCT = 5
SLIPPAGE_PCT = 3
ADJUST_PORTFOLIO_YEAR = [2012, 2017, 2022]
BUSINESS_CYCLE = 5

STK_LIST = {
    'semiconductor' : tw_stock_id.SEMICONDUCTOR,
    'computer_peripherals' : tw_stock_id.COMPUTER_PERIPHERALS,
    'electronic_components' : tw_stock_id.ELECTRONIC_COMPONENTS,
    'food' : tw_stock_id.FOOD,
}


BALANCE_FEATURES = ["current_ratio(%)", "quick_ratio(%)"]
PROFIT_FEATURES = ["revenue(%)", "gross_profit(%)", "net_income(%)"]  #["revenue(%)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)"]


PROFIT_RAW_DATA_COLUMNS = ["years", "revenue(100B)" ,"gross_profit(%)" , "operating_margin(%)" , "other_income(%)" , "net_income(%)" , "ROE(%)" , "ROA(%)", "EPS", "up(dolar)", "BPS"]
BALANCE_RAW_DATA_COLUMNS = ["years", "stock" , "current_assets", "current_liabilities"]

class DataType:
    dividend_history = 'dividend_history'
    profit_indicator = 'profit_indicator'
    balance_sheet = 'balance_sheet'
    daily_close = 'daily_close'
    

class LoadedData:
    def __init__(self,  profit_indicator:pd.DataFrame): #, dividend_history:pd.DataFrame,balance_sheet:pd.DataFrame, daily_close:pd.DataFrame):
        self.profit_indicator = profit_indicator
        # self.dividend_history = dividend_history
        # self.balance_sheet = balance_sheet
        # self.daily_close = daily_close

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