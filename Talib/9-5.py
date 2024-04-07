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
KBar = Indicator.Signal_03(KBar) # <-----請自行修改

# 設定停利停損條件 (單位:%)
TakeProfit = 0.05 # 停利百分比 <-----請自行修改
StopLoss = 0.05   # 停損百分比 <-----請自行修改

BS = None  # None代表空手 B代表持有多單部位 S代表持有空單
Record = pd.DataFrame(columns=['BS','OrderDate','OrderPrice','CoverDate','CoverPrice','Profit'])

for i in KBar.index:
    Condition1 = KBar['Signal_01'][i] == 100  # 均線黃金交叉
    Condition2 = KBar['Signal_01'][i] == -100 # 均線死亡交叉
    Condition3 = KBar['Signal_03'][i] == 100  # RSI指標>=55
    Condition4 = KBar['Signal_03'][i] == -100 # RSI指標<=45
    # 空手
    if BS == None:
        if Condition1 and Condition3:
            BS = 'B'
            OrderDate = i.strftime('%Y-%m-%d')
            OrderPrice = KBar['close'][i]
        elif Condition2 and Condition4:
            BS = 'S'
            OrderDate = i.strftime('%Y-%m-%d')
            OrderPrice = KBar['close'][i]
    # 持有多單
    elif BS == 'B':
        # 多單的停利及停損
        Condition5 = ( KBar['close'][i] >= OrderPrice*(1+TakeProfit) )
        Condition6 = ( KBar['close'][i] <= OrderPrice*(1-StopLoss) )
        # 觸發其一就出場
        if Condition5 or Condition6:
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
    # 持有空單
    elif BS == 'S':
        # 空單的停利及停損
        Condition5 = ( KBar['close'][i] <= OrderPrice*(1-TakeProfit) )
        Condition6 = ( KBar['close'][i] >= OrderPrice*(1+StopLoss) )
        # 觸發其一就出場
        if Condition5 or Condition6:
            CoverDate = i.strftime('%Y-%m-%d')
            CoverPrice = KBar['close'][i]
            Profit = round(OrderPrice - CoverPrice,2)
            Record = Record.append({
                'BS':BS,
                'OrderDate':OrderDate,
                'OrderPrice':OrderPrice,
                'CoverDate':CoverDate,
                'CoverPrice':CoverPrice,
                'Profit':Profit
                },ignore_index=True)
            BS = None 

# 印出交易紀錄
print(Record)
# 計算績效KPI
Function.GetKPI(Record.Profit)
