from goodinfo_client import GoodinfoClient
from yahoo_finance_client import YahooFinanceClient
from stock_analyzer import StockAnalyzer
from backtester import Backtester

industry = 'semiconductor' # semiconductor, computer_peripherals, electronic_components, food 
goodimfo_client = GoodinfoClient(industry=industry)
yfinance_client = YahooFinanceClient(industry=industry)
analyzer = StockAnalyzer(industry=industry)
backtester = Backtester(industry=industry)

if __name__ == '__main__':
    goodimfo_client.get_raw_data()
    yfinance_client.get_raw_data()
    analyzer.run_analysis()
    backtester.run_backtest()