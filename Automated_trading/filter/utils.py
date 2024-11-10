#寫需要用到的function
from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)



def create_order(symbol, side, type, timeInForce, quantity, price):
    return client.futures_create_order(symbol='BTCUSDT', side='BUY', type='LIMIT', timeInForce='GTC', quantity=0.001, price=10000)

def get_order(symbol, orderId):
    return client.futures_get_order(symbol='BTCUSDT', orderId=12345)

def cancel_order(symbol, orderId):
    return client.futures_cancel_order(symbol='BTCUSDT', orderId=12345)

def change_leverage(symbol, leverage):
    return client.futures_change_leverage(symbol='ETHUSDT', leverage=10)