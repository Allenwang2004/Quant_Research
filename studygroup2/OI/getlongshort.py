#get the SOLUSDT OI data
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

base_url = 'https://fapi.binance.com'

# Symbol to fetch
symbol = 'SOLUSDT'

# Function to convert datetime to timestamp in milliseconds
def timestamp_to_int(dt):
    return int(datetime.timestamp(dt) * 1000)

# Get the current time only with yyyy-mm-dd
current_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
current_time = current_time - timedelta(minutes=current_time.minute % 15)
end_time = current_time - timedelta(days=1)
start_time = end_time
end_time = end_time.replace(hour=23, minute=45)
start_time = timestamp_to_int(start_time)
end_time = timestamp_to_int(end_time)

# Function to get historical OI and append to DataFrame
def get_historical_OI(df, start_time):
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
        OI_df = pd.DataFrame(data, columns=['timestamp', 'sumOpenInterest', 'sumOpenInterestValue'])
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
    df = get_historical_OI(df, start_time)
    start_time += 15 * 60 * 1000  # Move to next 15 minutes

# Print or process the DataFrame as needed
print(df)

# Attach to MongoDB
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['binance']
collection = db['SOLopenInterestlongshort']

# Convert DataFrame to dictionary
data_dict = df.to_dict(orient='records')

# Insert data to MongoDB
collection.insert_many(data_dict)