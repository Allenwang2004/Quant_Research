# 載入套件
from talib.abstract import *
import sys,Function,numpy

# 資料參數 (可自行調整)
SDate = sys.argv[1] # 資料起始日
EDate = sys.argv[2] # 資料結束日
Prod = sys.argv[3]  # 商品代碼
Kind = sys.argv[4]  # 商品種類
Cycle = sys.argv[5] # K棒週期

# 取得K棒資料
KBar = Function.GetKBar(SDate,EDate,Prod,Kind,Cycle)

# 收盤價陣列 及 自定義週期
Close = KBar['close']
Period = [2,3,3,2,2,3,2,4,2,3,2,3,3,2,2,3,2,4,2,3,2,3] 

# 將陣列轉為 numpy 的浮點位數型態
Close = numpy.array(Close,dtype=float)
Period = numpy.array(Period,dtype=float)

# 計算技術指標
Data = MAVP(Close, Period, minperiod=2, maxperiod=4, matype=0)
print(Data)

# 定義圖片物件
Picture = Function.DrawKBar(KBar)

# 將指標新增至圖片物件
Picture.Add(Data,panel=0,type='line',color='black')

# 顯示圖片
Picture.Show()
