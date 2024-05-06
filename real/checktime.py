import requests
import time

def get_binance_server_time():
    response = requests.get('https://api.binance.com/api/v3/time')
    server_time = response.json()['serverTime']
    return server_time

def get_local_system_time():
    return int(time.time() * 1000)  # Convert to milliseconds

def check_time_sync():
    binance_time = get_binance_server_time()
    local_time = get_local_system_time()
    time_diff = abs(binance_time - local_time)
    print("Binance Server Time:", binance_time)
    print("Local System Time:", local_time)
    print("Time Difference (milliseconds):", time_diff)
    if time_diff > 10000:  # Adjust threshold as needed
        print("System time and Binance server time are not in sync.")
    else:
        print("System time and Binance server time are in sync.")

check_time_sync()
