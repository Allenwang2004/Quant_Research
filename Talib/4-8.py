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
DMI_DX = DX(KBar,timeperiod=14)             # 趨向指數 (黑線)
DMI_PLUS_DI = PLUS_DI(KBar,timeperiod=14)   # 正趨向指數 (紅線)
DMI_MINUS_DI = MINUS_DI(KBar,timeperiod=14) # 負趨向指數 (藍線)
DMI_PLUS_DM = PLUS_DM(KBar,timeperiod=14)   # 正趨向變動值 (不繪圖)
DMI_MINUS_DM = MINUS_DM(KBar,timeperiod=14) # 負趨向變動值 (不繪圖)
print('-----------------DMI_DX-----------------')
print(DMI_DX)
print('-----------------DMI_PLUS_DI-----------------')
print(DMI_PLUS_DI)
print('-----------------DMI_MINUS_DI-----------------')
print(DMI_MINUS_DI)

# 定義圖片物件
Picture = Function.DrawKBar(KBar)

# 將指標新增至圖片物件
Picture.Add(DMI_DX,panel=2,type='line',color='black',ylabel='DMI')
Picture.Add(DMI_PLUS_DI,panel=2,type='line',color='red',ylabel='DMI')
Picture.Add(DMI_MINUS_DI,panel=2,type='line',color='blue',ylabel='DMI')

# 顯示圖片
Picture.Show()
