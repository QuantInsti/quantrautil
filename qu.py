import pandas as pd
import traceback

import fix_yahoo_finance as yf
import iexfinance.stocks as iex
import nsepy

def get_quantinsti_api_key(key='None'):
    if key=='None':
        message = "You need to either pass the API key as parameter to this function (get_quantinsti_api_key(key='<<Your API Key>>') or replace the function call with your API key. To get your API key, sign up for a free Quandl account (https://docs.quandl.com/docs#section-authentication). Then, you can find your API key on Quandl account settings page"
        print(message)

    return key

def get_alpha_vantage_api_key(key='None'):
    if key=='None':
        message = "You need to either pass the API key as parameter to this function (get_alpha_vantage_api_key(key='<<Your API Key>>') or replace the function call with your API key. To get your API key, sign up for a free Alpha vantage account (https://www.alphavantage.co/support/#api-key)."
        print(message)

    return key

def get_binance_api_key(key='None'):
    if key=='None':
        message = "You need to either pass the API key as parameter to this function (get_binance_api_key(key='<<Your API Key>>') or replace the function call with your API key. To get your API key, sign up for a free binance account."
        print(message)

    return key

def get_data(ticker, start_date='2016-01-01', end_date='2017-01-01'):
    """
        This function fetches the data from different web source such as Quandl, Yahoo finance and NSEPy
    """
    try:
        df = yf.download(ticker, start_date, end_date)
        df['Source'] = 'Yahoo'        
        return df[['Open','High','Low','Close','Adj Close','Volume','Source']]
    except:
        try:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            df = iex.stocks.get_historical_data(ticker, start=start_date, end=end_date, output_format='pandas')
            df.index.name = 'Date'
            df = df.rename(columns={'open': 'Open',
                                    'high': 'High',
                                    'low': 'Low',
                                    'close': 'Close',
                                    'volume': 'Volume',
                                   })
            df['Source'] = 'IEX'                
            return df[['Open','High','Low','Close','Volume','Source']]
        except:
            try:                    
                df = nsepy.get_history(symbol=ticker, start=start_date, end=end_date)                    
                df['Source'] = 'nsepy'
                return df[['Open','High','Low','Close','Volume','Source']]
            except:                                                           
                print(traceback.print_exc())
                    