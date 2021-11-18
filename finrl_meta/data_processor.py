from finrl_meta.data_processors.processor_alpaca import AlpacaProcessor as Alpaca
from finrl_meta.data_processors.processor_wrds import WrdsProcessor as Wrds
from finrl_meta.data_processors.processor_yahoofinance import YahooFinanceProcessor as YahooFinance
from finrl_meta.data_processors.processor_binance import BinanceProcessor as Binance
import pandas as pd
import numpy as np

class DataProcessor():
    def __init__(self, data_source, **kwargs):
        if data_source == 'alpaca':
            
            try:
                API_KEY= kwargs.get('API_KEY')
                API_SECRET= kwargs.get('API_SECRET')
                APCA_API_BASE_URL= kwargs.get('APCA_API_BASE_URL')
                self.processor = Alpaca(API_KEY, API_SECRET, APCA_API_BASE_URL)
                print('Alpaca successfully connected')
            except:
                raise ValueError('Please input correct account info for alpaca!')
                
        elif data_source == 'wrds':
            self.processor = Wrds()
            
        elif data_source == 'yahoofinance':
            self.processor = YahooFinance()
        
        elif data_source =='binance':
            self.processor = Binance()
            
        else:
            raise ValueError('Data source input is NOT supported yet.')
    
    def download_data(self, ticker_list, start_date, end_date, 
                      time_interval) -> pd.DataFrame:
        df = self.processor.download_data(ticker_list = ticker_list, 
                                          start_date = start_date, 
                                          end_date = end_date,
                                          time_interval = time_interval)
        return df
    
    def clean_data(self, df) -> pd.DataFrame:
        df = self.processor.clean_data(df)
        
        return df
    
    def add_technical_indicator(self, df, tech_indicator_list) -> pd.DataFrame:
        self.tech_indicator_list = tech_indicator_list
        df = self.processor.add_technical_indicator(df, tech_indicator_list)
        
        return df
    
    def add_turbulence(self, df) -> pd.DataFrame:
        df = self.processor.add_turbulence(df)
        
        return df
    
    def add_vix(self, df) -> pd.DataFrame:
        df = self.processor.add_vix(df)
        
        return df
    
    def df_to_array(self, df, if_vix) -> np.array:
        price_array,tech_array,turbulence_array = self.processor.df_to_array(df,
                                                self.tech_indicator_list,
                                                if_vix)
        #fill nan with 0 for technical indicators
        tech_nan_positions = np.isnan(tech_array)
        tech_array[tech_nan_positions] = 0
        
        return price_array, tech_array, turbulence_array
    
    def run(self, ticker_list, start_date, end_date, time_interval, 
            technical_indicator_list, if_vix):
        data = self.processor.download_data(ticker_list, start_date, end_date, time_interval)
        data = self.processor.clean_data(data)
        data = self.processor.add_technical_indicator(data, technical_indicator_list)
        if if_vix:
            data = self.processor.add_vix(data)
        price_array, tech_array, turbulence_array = self.processor.df_to_array(data, if_vix)
        tech_nan_positions = np.isnan(tech_array)
        tech_array[tech_nan_positions] = 0

        return price_array, tech_array, turbulence_array
