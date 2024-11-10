import os, sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PROJECT_ROOT)

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

# 計算交易績效指標
def Performance(
        trade=pd.DataFrame(),
        leverage=1.0,
        fee_rate=0.001,
        slip_rate=0.0001,
    ):
    # 如果沒有交易紀錄 則不做接下來的計算
    if trade.shape[0]==0:
        print('沒有交易紀錄')
        return False

    # -------------------純做空------------------- #
    trade1=trade.copy()
    # 給交易明細定義欄位名稱
    trade1.columns=['product','bs','order_time','order_price','cover_time','cover_price','order_unit']
    # 計算出每筆的報酬率
    trade1['ret']=(((trade1['order_price']-trade1['cover_price'])/trade1['order_price'])-fee_rate) *trade1['order_unit']*leverage
    
    days_in_year = 365
    period_days = 1
    period_rate = trade1['ret'].mean()
    periods_per_year = days_in_year / period_days
    annualized_return = (1 + period_rate) ** periods_per_year - 1

    # 1.	總報酬率：整個回測期間的總報酬率累加
    print('總績效 %s '%( round(trade1['ret'].sum(),4) ))
    # 2.	總交易次數：代表回測的交易筆數
    print('交易次數 %s '%( trade1.shape[0] ))
    # 3.	平均報酬率：簡單平均報酬率（扣除交易成本後）
    print('平均績效 %s '%( round(trade1['ret'].mean(),4) ))
    # 4.	年化報酬率：代表每年的平均報酬率
    print('年化報酬率 %s '%( round(annualized_return,4) ))
    # 5.	勝率
    earn_ratio=trade1[trade1['ret'] > 0].shape[0] / trade1.shape[0]
    print('勝率 %s '%( round(earn_ratio ,2) ))
    # 6.	平均獲利：代表平均每一次獲利的金額（扣除交易成本後）
    avg_earn=trade1[trade1['ret'] > 0]['ret'].mean()
    print('平均獲利 %s '%( round(avg_earn,4)))
    # 7.	平均虧損：代表平均每一次虧損的金額（扣除交易成本後）
    avg_loss=trade1[trade1['ret'] <= 0]['ret'].mean()
    print('平均虧損 %s '%( round(avg_loss,4) ))
    # 8.	賺賠比：代表平均獲利 / 平均虧損
    odds=abs(avg_earn/avg_loss)
    print('賺賠比 %s '%( round(odds,4) ))
    # 9.	期望值：代表每投入的金額，可能會回報的多少倍的金額
    print('期望值 %s '%( round(((earn_ratio*odds)-(1-earn_ratio)),4) ))
    # 10.	最大連續虧損：代表連續虧損的最大幅度
    tmp_accloss=1
    max_accloss=1
    for ret in trade1['ret'].values:
        if ret <= 0:
            tmp_accloss *= ret
            max_accloss= min(max_accloss,tmp_accloss)
        else:
            tmp_accloss = 1
    print('最大連續虧損',round(max_accloss ,4))

    # 優先計算累計報酬率 並將累計報酬率的初始值改為1 繪圖較容易閱讀
    trade1['acc_ret'] = (1+trade1['ret']).cumprod() 
    trade1.loc[-1,'acc_ret'] = 1 
    trade1.index = trade1.index + 1 
    trade1.sort_index(inplace=True) 

    # 13.	最大資金回落：代表資金從最高點回落至最低點的幅度
    trade1['acc_ret'] = (1+trade1['ret']).cumprod()
    trade1.loc[-1,'acc_ret'] = 1
    trade1.index = trade1.index + 1
    trade1.sort_index(inplace=True)
    trade1['acc_max_cap'] = trade1['acc_ret'].cummax()
    trade1['dd'] = (trade1['acc_ret'] / trade1['acc_max_cap'])
    trade1.loc[trade1['acc_ret'] == trade1['acc_max_cap'] , 'new_high'] = trade1['acc_ret']
    print('最大資金回落',round(1-trade1['dd'].min(),4))

    #14. 夏普比率
    #假設無風險利率為2%
    risk_free_rate = 0.02
    #計算年化波動率
    annual_volatility = trade1['ret'].std() * np.sqrt(periods_per_year)
    #計算夏普比率
    sharpe_ratio = (annualized_return - risk_free_rate) / annual_volatility
    print('夏普比率',round(sharpe_ratio,4))
    
    # 15.	繪製資金曲線圖(用幾何報酬計算)
    ax=plt.subplot(111)
    ax.plot( trade1['acc_ret'] , 'b-' ,label='Profit')
    ax.plot( trade1['dd'] , '-' ,color='#00A600',label='MDD')
    ax.plot( trade1['new_high'] , 'o' ,color='#FF0000',label='Equity high')
    ax.legend()
    plt.show()
    return trade1   


def Performance_hedged(
        trade=pd.DataFrame(),
        leverage=1.0,
        fee_rate=0.0002,
        slip_rate=0.0001,
    ):
    # 如果沒有交易紀錄 則不做接下來的計算
    if trade.shape[0]==0:
        print('沒有交易紀錄')
        return False
    # -------------------hedge------------------- #
    trade2=trade.copy()
    # 給交易明細定義欄位名稱
    trade2.columns=['product','bs','order_time','order_price','cover_time','cover_price','order_unit','hedge_product','hedge_bs','hedge_order_time','hedge_order_price','hedge_cover_time','hedge_cover_price','hedge_order_unit']
    # 計算出每筆的報酬率
    trade2['ret']=(((trade2['order_price']-trade2['cover_price'])/trade2['order_price'])-fee_rate) *trade2['order_unit']*leverage-(((trade2['hedge_order_price']-trade2['hedge_cover_price'])/trade2['hedge_order_price'])-fee_rate) *trade2['hedge_order_unit']*leverage
    
    days_in_year = 365
    period_days = 1
    period_rate = trade2['ret'].mean()
    periods_per_year = days_in_year / period_days
    annualized_return = (1 + period_rate) ** periods_per_year - 1

    # 1.	總報酬率：整個回測期間的總報酬率累加
    print('總績效 %s '%( round(trade2['ret'].sum(),4) ))
    # 2.	總交易次數：代表回測的交易筆數
    print('交易次數 %s '%( trade2.shape[0] ))
    # 3.	平均報酬率：簡單平均報酬率（扣除交易成本後）
    print('平均績效 %s '%( round(trade2['ret'].mean(),4) ))
    # 4.	年化報酬率：代表每年的平均報酬率
    print('年化報酬率 %s '%( round(annualized_return,4) ))
    # 5.	勝率
    earn_ratio=trade2[trade2['ret'] > 0].shape[0] / trade2.shape[0]
    print('勝率 %s '%( round(earn_ratio ,2) ))
    # 6.	平均獲利：代表平均每一次獲利的金額（扣除交易成本後）
    avg_earn=trade2[trade2['ret'] > 0]['ret'].mean()
    print('平均獲利 %s '%( round(avg_earn,4)))
    # 7.	平均虧損：代表平均每一次虧損的金額（扣除交易成本後）
    avg_loss=trade2[trade2['ret'] <= 0]['ret'].mean()
    print('平均虧損 %s '%( round(avg_loss,4) ))
    # 8.	賺賠比：代表平均獲利 / 平均虧損
    odds=abs(avg_earn/avg_loss)
    print('賺賠比 %s '%( round(odds,4) ))
    # 9.	期望值：代表每投入的金額，可能會回報的多少倍的金額
    print('期望值 %s '%( round(((earn_ratio*odds)-(1-earn_ratio)),4) ))
    # 10.	最大連續虧損：代表連續虧損的最大幅度
    tmp_accloss=1
    max_accloss=1
    for ret in trade2['ret'].values:
        if ret <= 0:
            tmp_accloss *= ret
            max_accloss= min(max_accloss,tmp_accloss)
        else:
            tmp_accloss = 1
    print('最大連續虧損',round(max_accloss ,4))

    # 優先計算累計報酬率 並將累計報酬率的初始值改為1 繪圖較容易閱讀
    trade2['acc_ret'] = (1+trade2['ret']).cumprod() 
    trade2.loc[-1,'acc_ret'] = 1 
    trade2.index = trade2.index + 1 
    trade2.sort_index(inplace=True) 

    # 13.	最大資金回落：代表資金從最高點回落至最低點的幅度
    trade2['acc_ret'] = (1+trade2['ret']).cumprod()
    trade2.loc[-1,'acc_ret'] = 1
    trade2.index = trade2.index + 1
    trade2.sort_index(inplace=True)
    trade2['acc_max_cap'] = trade2['acc_ret'].cummax()
    trade2['dd'] = (trade2['acc_ret'] / trade2['acc_max_cap'])
    trade2.loc[trade2['acc_ret'] == trade2['acc_max_cap'] , 'new_high'] = trade2['acc_ret']
    print('最大資金回落',round(1-trade2['dd'].min(),4))

    #14. 夏普比率
    #假設無風險利率為2%
    risk_free_rate = 0.02
    #計算年化波動率
    annual_volatility = trade2['ret'].std() * np.sqrt(periods_per_year)
    #計算夏普比率
    sharpe_ratio = (annualized_return - risk_free_rate) / annual_volatility
    print('夏普比率',round(sharpe_ratio,4))
    
    # 15.	繪製資金曲線圖(用幾何報酬計算)
    ax=plt.subplot(111)
    ax.plot( trade2['acc_ret'] , 'b-' ,label='Profit')
    ax.plot( trade2['dd'] , '-' ,color='#00A600',label='MDD')
    ax.plot( trade2['new_high'] , 'o' ,color='#FF0000',label='Equity high')
    ax.legend()
    plt.show()
    return trade2