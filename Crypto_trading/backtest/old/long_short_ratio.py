import os, sys
import requests
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

from utils.path_helper import *
from datetime import datetime, timedelta
from pathlib import Path

base_url = 'https://fapi.binance.com'

# Symbol to fetch
symbol = 'SOLUSDT'

# Function to convert datetime to timestamp in milliseconds
def timestamp_to_int(dt):
    return int(datetime.timestamp(dt) * 1000)

# Get the current time only with yyyy-mm-dd
start_time = datetime(2024, 7, 1) 
end_time = datetime(2024, 7, 25)
start_time = timestamp_to_int(start_time)
end_time = timestamp_to_int(end_time)

# Function to get historical OI and append to DataFrame
def get_historical_OI_longshort(df, start_time):
    endpoint = '/futures/data/globalLongShortAccountRatio'
    period = '15m'  # 15 minutes interval
    params = {
        'symbol': symbol,
        'period': period,
        'startTime': start_time,
        'endTime': start_time + 15 * 60 * 1000 - 1, # 15 minutes interval
        'limit': 400
    }
    url = base_url + endpoint
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        OI_df = pd.DataFrame(data, columns=['timestamp', 'longAccount'])
        OI_df['timestamp'] = pd.to_datetime(OI_df['timestamp'], unit='ms')
        df = pd.concat([df, OI_df], ignore_index=True)
        print(f'Symbol: {symbol}, Fetched {len(OI_df)} OI from {OI_df["timestamp"].min()} to {OI_df["timestamp"].max()}')
    else:
        print(f'Error: {response.status_code}')

    return df

# Initialize DataFrame
df = pd.DataFrame()

# Fetch data in loop
while start_time < end_time:
    df = get_historical_OI_longshort(df, start_time)
    start_time += 15 * 60 * 1000  # Move to next 15 minutes

# Print or process the DataFrame as needed
print(df)

filepath = Path(f'{LS_DATA_PATH}/{symbol}_longshort.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath)