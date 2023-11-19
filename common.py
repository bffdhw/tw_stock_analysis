import pandas as pd

TREND_START_YEAR = 2002
TREND_END_YEAR = 2011
BACKTEST_START_YEAR = TREND_END_YEAR + 1
STOP_LOSS_PCT = -20


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
    def __init__(self, dividend_history:pd.DataFrame(), profit_indicator:pd.DataFrame(), balance_sheet:pd.DataFrame(), daily_close:pd.DataFrame()):
        self.dividend_history = dividend_history
        self.profit_indicator = profit_indicator
        self.balance_sheet = balance_sheet
        self.daily_close = daily_close
    