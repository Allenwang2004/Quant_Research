import time
import requests
import hmac
from hashlib import sha256

APIURL = "https://open-api-vst.bingx.com"
APIKEY = "6ObCKI8eYl1EwZYVZ7SiasNN5TCDBHK9lmbDpMUGDTwz1WRdbeBkRVVRWivyB9xLqm0J05pIFGEuNw4TQ"
SECRETKEY = "CJ6zzTfQ60wgcVyFAzlyPjAKiHqXNhCDwiD7UFFNz0veSJNG85RHdVxlGQT0qnu4eou8Wus3HK3FkXF5VjR1hA"

def get_sign(api_secret, payload):
    signature = hmac.new(api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256).hexdigest()
    print("sign=" + signature)
    return signature


def send_request(method, path, urlpa, payload):
    url = "%s%s?%s&signature=%s" % (APIURL, path, urlpa, get_sign(SECRETKEY, urlpa))
    print(url)
    headers = {
        'X-BX-APIKEY': APIKEY,
    }
    response = requests.request(method, url, headers=headers, data=payload)
    return response.text


def parseParam(paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    if paramsStr != "": 
        return paramsStr+"&timestamp="+str(int(time.time() * 1000))
    else:
        return paramsStr+"timestamp="+str(int(time.time() * 1000))

# ------------------------------- #
# ------------------------------- #
# --------- Our Function -------- #
# ------------ Below ------------ #
# ------------------------------- #

# open_order_demo 跟 open_market_order 是一樣的功能，只是 open_order_demo 有多一個 positionSide 的參數 用來指定是 LONG 還是 SHORT
def open_order_demo(symbol="BTC-USDT", action="BUY", quantity=1) :

    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    
    positionSide = ""
    if action == "BUY" :
        positionSide = "LONG"
    else :
        positionSide = "SHORT"

    paramsMap = {
        "symbol": symbol,
        "type": "MARKET",
        "side": action,
        "positionSide": positionSide,
        "quantity": quantity,
        "stopPrice": 0,
        "recvWindow": 0,
        "timeInForce": ""
    } # paramsMap

    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def open_market_order(symbol="BTC-USDT", action="BUY", quantity=1):
    positionSide = ""
    if action == "BUY" :
        positionSide = "LONG"
    else :
        positionSide = "SHORT"
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    paramsMap = {
    "symbol": symbol,
    "type": "MARKET",
    "side": action,
    "positionSide": positionSide,
    "quantity": quantity,
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def BingX_trade_marginType(symbol="BTC-USDT", marginType="", recvWindow=0) :

    payload = {}
    path = '/openApi/swap/v2/trade/marginType'
    method = "POST"

    paramsMap = {
    "symbol": symbol,
    "marginType": marginType, # ISOLATED, CROSSED
    "recvWindow": 0
    }   # paramsMap

    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def close_order(symbol="BTC-USDT", action="BUY", quantity=1):
    positionSide = ""
    if action == "BUY" :
        positionSide = "LONG"
    else :
        positionSide = "SHORT"
    payload = {}
    path = '/openApi/swap/v2/trade/order'
    method = "POST"
    paramsMap = {
    "symbol": symbol,
    "type": "MARKET",
    "side": "SELL",
    "positionSide": positionSide,
    "quantity": quantity,
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def BingX_get_market_openInterest():
    payload = {}
    path = '/openApi/swap/v2/quote/openInterest'
    method = "GET"
    paramsMap = {
    "symbol": "BTC-USDT"
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

def BingX_get_position_info():
    payload = {}
    path = '/openApi/swap/v2/user/positions'
    method = "GET"
    paramsMap = {
    "symbol": "BTC-USDT",
    "recvWindow": 0
}
    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)


def BingX_close_all_position() :
    payload = {}
    path = '/openApi/swap/v2/trade/closeAllPositions'
    method = "POST"
    paramsMap = {
        "recvWindow": 0
    } # paramsMap

    paramsStr = parseParam(paramsMap)
    return send_request(method, path, paramsStr, payload)

if __name__ == '__main__':

    print("Hi")
