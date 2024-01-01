from goodinfo_client import GoodinfoClient
from yahoo_finance_client import YahooFinanceClient
from stock_analyzer import StockAnalyzer
from backtester import Backtester

if __name__ == '__main__':
    
    import time
    start_time = time.time()
    
    industry = 'electronic_components' # semiconductor, computer_peripherals, electronic_components, food 
    goodimfo_client = GoodinfoClient(industry=industry)
    yfinance_client = YahooFinanceClient(industry=industry)
    analyzer = StockAnalyzer(industry=industry)
    backtester = Backtester(industry=industry)
    
    goodimfo_client.get_raw_data()
    yfinance_client.get_raw_data()
    analyzer.run_analysis()
    backtester.run_backtest()
    
    end_time = time.time()
    print(f"{end_time - start_time} seconds")