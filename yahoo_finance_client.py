import os
import time
import yfinance as yf
import tw_stock_id


class YahooFinanceClient:
    
    def __init__(self):
        self.data_folder = os.path.abspath("./data")
        os.makedirs(self.data_folder, exist_ok=True)
    
    def get_raw_daily_close(self, stk_id):
        df = yf.download(f'{stk_id}.TW')
        df = df['Close']
        df = df.reset_index()
        
        daily_close_folder = os.path.join(self.data_folder, 'daily_close')
        if not os.path.exists(daily_close_folder):
            os.makedirs(daily_close_folder)
        
        df.to_csv(os.path.join(daily_close_folder, f'{stk_id}.csv'), index=False)
        
    def get_raw_data(self, stk_list):
        for stk_id in stk_list:
            self.get_raw_daily_close(stk_id=stk_id)
            time.sleep(1)


if __name__ == '__main__':
    stk_list = tw_stock_id.SEMICONDUCTOR
    client = YahooFinanceClient()
    client.get_raw_data(stk_list=stk_list)