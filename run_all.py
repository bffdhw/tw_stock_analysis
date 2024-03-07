from goodinfo_client import GoodinfoClient
from yahoo_finance_client import YahooFinanceClient
from stock_analyzer import StockAnalyzer
from backtester import Backtester
from common import get_stock_ids

if __name__ == '__main__':
    
    stk_list_by_industries = get_stock_ids()
        
    for industry, stk_list in stk_list_by_industries.items():
        print(industry)
        
        goodinfo_client = GoodinfoClient(stk_list=stk_list)
        goodinfo_client.get_raw_data()
        
        yfinance_client = YahooFinanceClient(stk_list=stk_list)
        yfinance_client.get_raw_data()
        
        analyzer = StockAnalyzer(industry=industry, stk_list=stk_list)
        analyzer.run_analysis()
        
        backtester = Backtester(industry=industry)
        backtester.run_backtest()
    