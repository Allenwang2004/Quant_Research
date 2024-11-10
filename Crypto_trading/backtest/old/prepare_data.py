import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

def getcryptoprice(symbol, start_time, end_time, interval, limit, path):
    
    base_url = 'https://fapi.binance.com'
    symbol = symbol
    limit = limit
    interval = interval
    def timestamp_to_int(dt):
        return int(datetime.timestamp(dt) * 1000)

    start_time = timestamp_to_int(start_time)
    end_time = timestamp_to_int(end_time)

    def get_historical_klines(df, start_time):
        endpoint = '/fapi/v1/klines'
        Interval = interval
        params = {
            'symbol': symbol,
            'interval': Interval,
            'startTime': start_time,
            'endTime': start_time + limit * 60 * 1000 - 1,
            'limit': 1000
        }
        url = base_url + endpoint
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            klines_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            klines_df['timestamp'] = pd.to_datetime(klines_df['timestamp'], unit='ms')
            df = pd.concat([df, klines_df], ignore_index=True)
            print(f'Symbol: {symbol}, Fetched {len(klines_df)} klines from {klines_df["timestamp"].min()} to {klines_df["timestamp"].max()}')
        else:
            print(f'Error: {response.status_code}')

        return df
    
    df = pd.DataFrame()

    # Fetch data in loop
    while start_time < end_time:
        df = get_historical_klines(df, start_time)
        start_time += limit * 60 * 1000

    print(df)
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)

def getcryptoOI(symbol, start_time, end_time, interval, limit, path):
    
    base_url = 'https://fapi.binance.com'
    symbol = symbol
    limit = limit
    interval = interval
    def timestamp_to_int(dt):
        return int(datetime.timestamp(dt) * 1000)

    start_time = timestamp_to_int(start_time)
    end_time = timestamp_to_int(end_time)

    def get_historical_OI(df, start_time):
        endpoint = '/fuctures/data/openInterestHist'
        Interval = interval
        params = {
            'symbol': symbol,
            'interval': Interval,
            'startTime': start_time,
            'endTime': start_time + limit * 60 * 1000 - 1,
            'limit': 1000
        }
        url = base_url + endpoint
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            OI_df = pd.DataFrame(data, columns=['timestamp', 'sumOpenInterest', 'sumOpenInterestValue'])
            OI_df['timestamp'] = pd.to_datetime(OI_df['timestamp'], unit='ms')
            df = pd.concat([df, OI_df], ignore_index=True)
            print(f'Symbol: {symbol}, Fetched {len(OI_df)} OI from {OI_df["timestamp"].min()} to {OI_df["timestamp"].max()}')
        else:
            print(f'Error: {response.status_code}')

        return df
    
    df = pd.DataFrame()

    # Fetch data in loop
    while start_time < end_time:
        df = get_historical_OI(df, start_time)
        start_time += limit * 60 * 1000

    print(df)
    filepath = Path(path)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath)     

def getpricechangeratio(filepath_to_get, file_path_to_save):
    df = pd.read_csv(filepath_to_get)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df['price_change'] = df['close'].diff()
    df['price_pct_change'] = df['close'].pct_change()
    df['price_change_ratio'] = df['price_change']/df['close']
    df.to_csv(file_path_to_save)

def getOIchangeratio(filepath_to_get,file_path_to_save):
    df = pd.read_csv(filepath_to_get)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df['long_OI_change'] = df['long_OI'].diff()
    df['sum_OI_change'] = df['sumOpenInterest'].diff()
    df['long_OI_pct_change'] = df['long_OI'].pct_change()
    df['sum_OI_pct_change'] = df['sumOpenInterest'].pct_change()
    df.to_csv(file_path_to_save)

def overheattime(price,OI):
    return price/OI

def checkERM(list,ERM):
    for i in list:
        if i>ERM:
            return False
    return True

# 繪製蠟燭圖
def ChartCandle(data,addp=[]):
    mcolor=mpf.make_marketcolors(up='r', down='g', inherit=True)
    mstyle=mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
    mpf.plot(data,addplot=addp,style=mstyle,type='candle',volume=True)
    
def plotCandle(filepath):
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    ChartCandle(df)