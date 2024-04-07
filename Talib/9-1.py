# 載入套件
import sys,Function,Indicator

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

# 印出前15筆資料
print(KBar[:15])

# 印出後15筆資料
#print(KBar[-15:])   
 