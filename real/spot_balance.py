from binance.client import Client
from config import api_key, api_secert
client = Client(api_key, api_secert)

def get_all_wallet_balances():
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        
        for balance in balances:
            asset = balance['asset']
            free_balance = float(balance['free'])
            locked_balance = float(balance['locked'])
            
            total_balance = free_balance + locked_balance
            
            if total_balance > 0:
                print(f"{asset}: Free={free_balance}, Locked={locked_balance}, Total={total_balance}")
    except Exception as e:
        print(f"Error getting wallet balances: {e}")
        
get_all_wallet_balances()