import sys
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np 

import warnings
warnings.filterwarnings('ignore')

data_processing_dir = os.path.dirname(os.path.abspath('data_processing_new.py'))

'''
utils_dir = os.path.join(data_processing_dir, '..', 'utils')
sys.path.append(utils_dir)
'''
sys.path.insert(0, "D:\\allen_trading_crypto\\utils")

from utils.path_helper import * 

symbol_pool = {'1000SATSUSDT', 'MAVUSDT', 'LPTUSDT', 'LOOMUSDT', 'LRCUSDT',
       'LSKUSDT', 'LQTYUSDT', 'LTCUSDT', 'MATICUSDT', 'MEMEUSDT',
       'MANAUSDT', '1INCHUSDT', 'AGLDUSDT', 'MAGICUSDT', 'ALGOUSDT',
       'METISUSDT', 'MKRUSDT', 'MANTAUSDT', 'MASKUSDT', 'AIUSDT',
       'MINAUSDT', 'MOVRUSDT', 'ACHUSDT', 'MTLUSDT', 'AEVOUSDT',
       'NEARUSDT', 'NEOUSDT', 'NFPUSDT', 'AMBUSDT', 'ACEUSDT', 'BANDUSDT',
       'ARBUSDT', 'ARUSDT', 'BCHUSDT', 'API3USDT', 'NOTUSDT', 'ALTUSDT',
       'AUCTIONUSDT', 'NKNUSDT', 'APTUSDT', 'BELUSDT', 'BLZUSDT',
       'NMRUSDT', 'AXLUSDT', 'BALUSDT', 'OMGUSDT', 'ALICEUSDT', 'CKBUSDT',
       'BLURUSDT', 'OGNUSDT', 'ARKMUSDT', 'ARPAUSDT', 'BADGERUSDT',
       'BNBUSDT', 'OMNIUSDT', 'DARUSDT', 'COMPUSDT', 'ADAUSDT',
       'NTRNUSDT', 'OMUSDT', 'AXSUSDT', 'ASTRUSDT', 'BATUSDT', 'AVAXUSDT',
       'C98USDT', 'CFXUSDT', 'ANKRUSDT', 'CHZUSDT', 'ENAUSDT', 'ETCUSDT',
       'ARKUSDT', 'ONEUSDT', 'DUSKUSDT', 'BICOUSDT', 'ALPHAUSDT',
       'BTCUSDT', 'CELRUSDT', 'BNTUSDT', 'ENJUSDT', 'CAKEUSDT', 'DOTUSDT',
       'EGLDUSDT', 'FETUSDT', 'AAVEUSDT', 'BOMEUSDT', 'FLOWUSDT',
       'ETHUSDT', 'BONDUSDT', 'GMXUSDT', 'ONGUSDT', 'COTIUSDT', 'CHRUSDT',
       'ORDIUSDT', 'BNXUSDT', 'ATOMUSDT', 'BAKEUSDT', 'DYDXUSDT',
       'DYMUSDT', 'FILUSDT', 'ETHFIUSDT', 'GRTUSDT', 'HFTUSDT', 'ONTUSDT',
       'EDUUSDT', 'EOSUSDT', 'BEAMXUSDT', 'POLYXUSDT', 'PYTHUSDT',
       'DENTUSDT', 'ATAUSDT', 'LITUSDT', 'DOGEUSDT', 'GLMUSDT', 'OXTUSDT',
       'BBUSDT', 'GMTUSDT', 'PENDLEUSDT', 'COMBOUSDT', 'APEUSDT',
       'PERPUSDT', 'PHBUSDT', 'PIXELUSDT', 'RENDERUSDT', 'PEOPLEUSDT',
       'FTMUSDT', 'OPUSDT', 'CELOUSDT', 'SUSHIUSDT', 'RSRUSDT',
       'REEFUSDT', 'PORTALUSDT', 'STXUSDT', 'SAGAUSDT', 'SFPUSDT',
       'CRVUSDT', 'RVNUSDT', 'RIFUSDT', 'RLCUSDT', 'QTUMUSDT',
       'STORJUSDT', 'RONINUSDT', 'POWRUSDT', 'STRKUSDT', 'SANDUSDT',
       'RDNTUSDT', 'TONUSDT', 'STEEMUSDT', 'SNXUSDT', 'REZUSDT',
       'SKLUSDT', 'QNTUSDT', 'SOLUSDT', 'SUPERUSDT', 'TAOUSDT',
       'STMXUSDT', 'RUNEUSDT', 'ROSEUSDT', 'SEIUSDT', 'SPELLUSDT',
       'RENUSDT', 'USDCUSDT', 'SUIUSDT', 'THETAUSDT', 'SSVUSDT',
       'STGUSDT', 'TIAUSDT', 'TNSRUSDT', 'SXPUSDT', 'UNFIUSDT', 'TWTUSDT',
       'UNIUSDT', 'WAXPUSDT', 'TLMUSDT', 'XMRUSDT', 'TRUUSDT', 'WLDUSDT',
       'TRXUSDT', 'TUSDT', 'TRBUSDT', 'UMAUSDT', 'WOOUSDT', 'YGGUSDT',
       'VETUSDT', 'ZENUSDT', 'XVGUSDT', 'ZRXUSDT', 'XEMUSDT', 'VANRYUSDT',
       'XAIUSDT', 'XTZUSDT', 'YFIUSDT', 'WIFUSDT', 'ZROUSDT', 'FXSUSDT',
       'CYBERUSDT', 'GASUSDT', 'XLMUSDT', 'FLMUSDT', 'ZILUSDT', 'ZKUSDT',
       'USTCUSDT', 'CTSIUSDT', 'GTCUSDT', 'LINKUSDT', 'LINAUSDT',
       'GALAUSDT', 'LISTAUSDT', 'WUSDT', 'HBARUSDT', 'DASHUSDT',
       'FRONTUSDT', 'ZECUSDT', 'XVSUSDT', 'HIFIUSDT', 'XRPUSDT',
       'ENSUSDT'}

'''
for symbol in symbol_pool:
    print(f"Processing 5m{symbol}...")
    file_path = os.path.join(PRICE_DATA_PATH, f"{symbol}_UPERP_1m.csv")
    if os.path.exists(file_path):
        df1 = pd.read_csv(file_path)
        df2 = df1.iloc[::5, :]
        df2['price_change'] = df2['close']-df2['open']
        df2['price_pct_change'] = df2['price_change']/df2['open']
        df2.to_csv(os.path.join(PRICE_SAVE_PATH, f"{symbol}_UPERP_5m.csv"), index=False)
    else:
        print(f"File not found: {file_path}")
    print('finished')
'''

for symbol in symbol_pool:
    print(f"Processing signal{symbol}...")
    file_path1 = os.path.join(OPEN_INTEREST_PATH, f"{symbol}_open_interest.csv")
    file_path2 = os.path.join(PRICE_DATA_PATH, f"{symbol}_UPERP_1m.csv")
    if os.path.exists(file_path1) and os.path.exists(file_path2):
        df1 = pd.read_csv(file_path1).sort_values(by=['datetime','symbol']).drop_duplicates(subset=['datetime','symbol'], keep='last')
        df2 = pd.read_csv(file_path2).sort_values(by=['datetime']).drop_duplicates(subset=['datetime'], keep='last')
        df2['symbol'] = symbol
        df1.set_index(['datetime','symbol'], inplace=True)
        df2.set_index(['datetime','symbol'], inplace=True)
        #merge by datetime
        df = pd.merge(df1, df2, left_index=True, right_index=True, how='inner')
        df.to_csv(os.path.join(SIGNAL_PATH, f"{symbol}_signal.csv"))

'''
file_path = SIGNAL_PATH
df_all = pd.DataFrame()
for file in os.listdir(file_path):
    df = pd.read_csv(os.path.join(file_path, file))
    print(f"Processing all{file}...")
    #select the columns that we need
    df = df[['datetime', 'symbol','long_OI_pct_change', 'price_pct_change', 'price_pct_change', 'open','close']]
    df_all = pd.concat([df_all, df], axis=0)

df_all.sort_values(by=['datetime','symbol'], inplace=True)


df_all['sum'] = df_all['long_OI_pct_change'] + df_all['price_pct_change']
top_5 = df_all.loc[df_all.index.get_level_values('datetime').max()].nlargest(5, 'sum')
print(top_5)
'''