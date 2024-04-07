from binance.client import Client
api_key = 'm43EzMoIShOmUJNGIJBmaHgucVLMFPtf5fyczog2s5NgWpPU8bWt8qzfeUKttLrr'
api_secert = 'pA8KbEHgolMl4PcUswLoO1HpOLG9CfEcM3McveQDlbnGpmEXVcNmhhWDRLUfHO2i'
client = Client(api_key, api_secert)

#委託下單
#必填
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
