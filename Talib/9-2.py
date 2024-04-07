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
KBar = Indicator.Signal_02(KBar) # <-----請自行修改
Signal = KBar['Signal_02']       # <-----請自行修改

# 判斷訊號觸發後，1日、5日、20日的上漲下跌機率
L = len(Signal)-20
B_DIF_1,B_DIF_5,B_DIF_20 = [],[],[]
S_DIF_1,S_DIF_5,S_DIF_20 = [],[],[]
for i in range(0,L):
    if Signal[i] == 100:
        B_DIF_1.append( KBar['close'][i+1] - KBar['close'][i] )
        B_DIF_5.append( KBar['close'][i+5] - KBar['close'][i] )
        B_DIF_20.append( KBar['close'][i+20] - KBar['close'][i] )
    elif Signal[i] == -100:
        S_DIF_1.append( KBar['close'][i+1] - KBar['close'][i] )
        S_DIF_5.append( KBar['close'][i+5] - KBar['close'][i] )
        S_DIF_20.append( KBar['close'][i+20] - KBar['close'][i] )

# 統計多方訊號的上漲下跌機率
B_Times = len(B_DIF_1)
if B_Times == 0:
    B_Up_1,B_Up_5,B_Up_20,B_Dn_1,B_Dn_5,B_Dn_20,B_No_1,B_No_5,B_No_20 = 0,0,0,0,0,0,0,0,0
else:
    B_Up_1 = round(len([ i for i in B_DIF_1 if i > 0 ]) / B_Times *100 ,2)
    B_Up_5 = round(len([ i for i in B_DIF_5 if i > 0 ]) / B_Times *100 ,2)
    B_Up_20 = round(len([ i for i in B_DIF_20 if i > 0 ]) / B_Times *100 ,2)
    B_Dn_1 = round(len([ i for i in B_DIF_1 if i < 0 ]) / B_Times *100 ,2)
    B_Dn_5 = round(len([ i for i in B_DIF_5 if i < 0 ]) / B_Times *100 ,2)
    B_Dn_20 = round(len([ i for i in B_DIF_20 if i < 0 ]) / B_Times *100 ,2)
    B_No_1 = round(100-B_Up_1-B_Dn_1 ,2)
    B_No_5 = round(100-B_Up_5-B_Dn_5 ,2)
    B_No_20 = round(100-B_Up_20-B_Dn_20 ,2)
print()
print(f'觸發多方訊號次數:{B_Times}次')
print(f'觸發後1日 上漲機率:{B_Up_1}% 下跌機率:{B_Dn_1}% 不漲不跌機率:{B_No_1}%')
print(f'觸發後5日 上漲機率:{B_Up_5}% 下跌機率:{B_Dn_5}% 不漲不跌機率:{B_No_5}%')
print(f'觸發後20日 上漲機率:{B_Up_20}% 下跌機率:{B_Dn_20}% 不漲不跌機率:{B_No_20}%')

# 統計空方訊號的上漲下跌機率
S_Times = len(S_DIF_1)
if S_Times == 0:
    S_Up_1,S_Up_5,S_Up_20,S_Dn_1,S_Dn_5,S_Dn_20,S_No_1,S_No_5,S_No_20 = 0,0,0,0,0,0,0,0,0
else:
    S_Up_1 = round(len([ i for i in S_DIF_1 if i > 0 ]) / S_Times *100 ,2)
    S_Up_5 = round(len([ i for i in S_DIF_5 if i > 0 ]) / S_Times *100 ,2)
    S_Up_20 = round(len([ i for i in S_DIF_20 if i > 0 ]) / S_Times *100 ,2)
    S_Dn_1 = round(len([ i for i in S_DIF_1 if i < 0 ]) / S_Times *100 ,2)
    S_Dn_5 = round(len([ i for i in S_DIF_5 if i < 0 ]) / S_Times *100 ,2)
    S_Dn_20 = round(len([ i for i in S_DIF_20 if i < 0 ]) / S_Times *100 ,2)
    S_No_1 = round(100-S_Up_1-S_Dn_1 ,2)
    S_No_5 = round(100-S_Up_5-S_Dn_5 ,2)
    S_No_20 = round(100-S_Up_20-S_Dn_20 ,2)
print()
print(f'觸發空方訊號次數:{S_Times}次')
print(f'觸發後1日 上漲機率:{S_Up_1}% 下跌機率:{S_Dn_1}% 不漲不跌機率:{S_No_1}%')
print(f'觸發後5日 上漲機率:{S_Up_5}% 下跌機率:{S_Dn_5}% 不漲不跌機率:{S_No_5}%')
print(f'觸發後20日 上漲機率:{S_Up_20}% 下跌機率:{S_Dn_20}% 不漲不跌機率:{S_No_20}%')
