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
KBar = KBar.join( AROON(KBar,timeperiod=25) )
AROON_UP = KBar['aroonup']
AROON_DN = KBar['aroondown']
print('-----------------AROON_UP-----------------')
print(AROON_UP)
print('-----------------AROON_DN-----------------')
print(AROON_DN)

# 定義圖片物件
Picture = Function.DrawKBar(KBar)

# 將指標新增至圖片物件
Picture.Add(AROON_UP,panel=2,type='line',color='red',ylabel='AROON')
Picture.Add(AROON_DN,panel=2,type='line',color='blue',ylabel='AROON')

# 顯示圖片
Picture.Show()
