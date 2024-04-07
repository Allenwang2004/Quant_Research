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
KBar = KBar.join( BBANDS(KBar, timeperiod=5, nbdevup=2.0, nbdevdn=2.0, matype=0) )
print('-----------------布林上軌-----------------')
print(KBar['upperband'])
print('-----------------布林中軌-----------------')
print(KBar['middleband'])
print('-----------------布林下軌-----------------')
print(KBar['lowerband'])

# 定義圖片物件
Picture = Function.DrawKBar(KBar)

# 將指標新增至圖片物件
Picture.Add(KBar['upperband'],panel=0,type='line',color='blue')
Picture.Add(KBar['middleband'],panel=0,type='line',color='black')
Picture.Add(KBar['lowerband'],panel=0,type='line',color='blue')

# 顯示圖片
Picture.Show()
