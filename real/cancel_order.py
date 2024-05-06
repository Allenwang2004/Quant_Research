from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)
#取消委託
#必填
#symbol = 'BTCUSDT' 交易對
#orderId = 12345 訂單ID
#可選
#origClientOrderId = 'myOrder1' 自訂訂單ID
#newClientOrderId = 'myOrder1' 自訂訂單ID
#recvWindow = 5000 API回報時間
#timestamp = int(time.time()*1000) API回報時間
client.futures_cancel_order
(

)