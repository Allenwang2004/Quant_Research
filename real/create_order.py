from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)

#委託下單
#symbol = 'BTCUSDT' 交易對
#side = 'BUY' or 'SELL' 買賣方向
#type = 'LIMIT' or 'MARKET' 訂單類型
#timeInForce = 'GTC' or 'IOC' or 'FOK' 委託類型
#quantity = 0.001 下單數量
#price = 10000 委託價格
#可選
#newClientOrderId = 'myOrder1' 自訂訂單ID
#stopPrice = 11000 觸發價格
#icebergQty = 10 委託數量
#newOrderRespType = 'ACK' or 'RESULT' 訂單回報類型
#recvWindow = 5000 API回報時間
#timestamp = int(time.time()*1000) API回報時間
client.futures_create_order
(

)
