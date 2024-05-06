from binance.client import Client
from config import api_key, api_secert

client = Client(api_key, api_secert)

futures_position = client.futures_position_information()

for i in futures_position:
    if i['symbol'] == 'BTCUSDT':
        print(i)
    if i['symbol'] == 'CRVUSDT':
        print(i)