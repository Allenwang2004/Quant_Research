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
Data_ROC = ROC(KBar,timeperiod=10)
Data_ROCP = ROCP(KBar,timeperiod=10)
Data_ROCR = ROCR(KBar,timeperiod=10)
Data_ROCR100 = ROCR100(KBar,timeperiod=10)

print('--------------ROC--------------')
print(Data_ROC)
print('--------------ROCP--------------')
print(Data_ROCP)
print('--------------ROCR--------------')
print(Data_ROCR)
print('--------------ROCR100--------------')
print(Data_ROCR100)
