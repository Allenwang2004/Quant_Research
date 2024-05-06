from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)
#合約帳戶餘額
client.futures_account_balance()
#只print出'balance'不為0的資料
for i in client.futures_account_balance():
    if i['balance'] != '0.00000000':
        print(i)