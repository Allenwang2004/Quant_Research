# 載入套件
import sys,Function,Indicator
import pandas as pd

# 資料參數 (可自行調整)
SDate = sys.argv[1] # 資料起始日
EDate = sys.argv[2] # 資料結束日
Prod = sys.argv[3]  # 商品代碼
Kind = sys.argv[4]  # 商品種類
Cycle = sys.argv[5] # K棒週期

# 取得K棒資料
KBar = Function.GetKBar(SDate,EDate,Prod,Kind,Cycle)

# 取得交易訊號
KBar = Indicator.Signal_01(KBar) # <-----請自行修改

BS = None
Record = pd.DataFrame(columns=['BS','OrderDate','OrderPrice','CoverDate','CoverPrice','Profit'])

for i in KBar.index:
    if BS == None and KBar['Signal_01'][i] == 100:
        BS = 'B'
        OrderDate = i.strftime('%Y-%m-%d')
        OrderPrice = KBar['close'][i]
    elif BS == 'B' and KBar['Signal_01'][i] == -100:
        CoverDate = i.strftime('%Y-%m-%d')
        CoverPrice = KBar['close'][i]
        Profit = round(CoverPrice - OrderPrice,2)
        Record = Record.append({
            'BS':BS,
            'OrderDate':OrderDate,
            'OrderPrice':OrderPrice,
            'CoverDate':CoverDate,
            'CoverPrice':CoverPrice,
            'Profit':Profit
            },ignore_index=True)
        BS = None        

print(Record)
Function.GetKPI(Record.Profit)
