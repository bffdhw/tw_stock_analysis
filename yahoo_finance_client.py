import os
import time
import yfinance as yf
from common import get_stock_ids


class YahooFinanceClient:
    
    def __init__(self, stk_list):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.stk_list = stk_list
    
    def get_raw_daily_close(self, stk_id, daily_close_folder):
        df = yf.download(f'{stk_id}.TW')
        df = df['Close']
        df = df.reset_index()
        df.to_csv(os.path.join(daily_close_folder, f'{stk_id}.csv'), index=False)
        
    def get_raw_data(self):
        
        daily_close_folder = os.path.join(self.data_folder, 'daily_close')
        if not os.path.exists(daily_close_folder):
            os.makedirs(daily_close_folder)
        
        for stk_id in self.stk_list:
            file_exists = os.path.exists(os.path.join(daily_close_folder, f'{stk_id}.csv'))
            if not file_exists:
                self.get_raw_daily_close(stk_id=stk_id, daily_close_folder=daily_close_folder)
                time.sleep(1)

if __name__ == '__main__':
    
    stk_list_by_industries = get_stock_ids()
        
    for industry, stk_list in stk_list_by_industries.items():
        client = YahooFinanceClient(stk_list=stk_list)
        client.get_raw_data()