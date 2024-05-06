from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)

#查詢委託
#必填
#symbol = 'BTCUSDT' 交易對
#可選
#orderId = 12345 訂單ID
#origClientOrderId = 'myOrder1' 自訂訂單ID
#recvWindow = 5000 API回報時間
#timestamp = int(time.time()*1000) API回報時間
client.futures_get_order
(

)