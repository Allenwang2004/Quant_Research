# 載入套件
from talib.abstract import *
import sys,Function

# 資料參數 (可自行調整)
SDate = sys.argv[1] # 資料起始日
EDate = sys.argv[2] # 資料結束日
Prod = sys.argv[3]  # 商品代碼
Kind = sys.argv[4]  # 商品種類
Cycle = sys.argv[5] # K棒週期

# 取得K棒資料
KBar = Function.GetKBar(SDate,EDate,Prod,Kind,Cycle)

# 計算技術指標
KBar = KBar.join( MACD(KBar,fastperiod=12,slowperiod=26,signalperiod=9) )
DIF_Value = KBar['macd']
MACD_Value = KBar['macdsignal']
OSC_Value = KBar['macdhist']
print('-----------------DIF-----------------')
print(DIF_Value)
print('-----------------MACD-----------------')
print(MACD_Value)
print('-----------------OSC-----------------')
print(OSC_Value)

# 定義圖片物件
Picture = Function.DrawKBar(KBar)

# 將指標新增至圖片物件
Picture.Add(DIF_Value,panel=2,type='line',color='red',ylabel='DIF & MACD')
Picture.Add(MACD_Value,panel=2,type='line',color='green',ylabel='DIF & MACD')
Picture.Add(OSC_Value,panel=2,type='bar',color='blue',ylabel='OSC')

# 顯示圖片
Picture.Show()
