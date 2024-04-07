from binance.client import Client
api_key = 'm43EzMoIShOmUJNGIJBmaHgucVLMFPtf5fyczog2s5NgWpPU8bWt8qzfeUKttLrr'
api_secert = 'pA8KbEHgolMl4PcUswLoO1HpOLG9CfEcM3McveQDlbnGpmEXVcNmhhWDRLUfHO2i'
client = Client(api_key, api_secert)
#合約帳戶餘額
client.futures_account_balance()
#合約帳戶當前部位
futures_position = client.futures_position_information()