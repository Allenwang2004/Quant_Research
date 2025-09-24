import numpy as np
import pandas as pd
#from scipy import stats
import re 
import warnings
warnings.filterwarnings('ignore')
def LS_cv(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    #前處理
    pp_dict = preprocessing(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols)
    punish = pp_dict['punish']
    if punish:return punish,None
    yp = pp_dict['yp']
    target = pp_dict['target']
    factor_returns_long_short = LS_return_fast(yp,target)
    factor_returns_long_short_mean = factor_returns_long_short.mean()
    factor_returns_long_short_std = factor_returns_long_short.std()
    if factor_returns_long_short_std == 0 or np.isnan(factor_returns_long_short_std):
        return -10,None
    else:
        #index = yp.index
        #total_days = ((index[-1] - index[0])/ pd.Timedelta('1 hour'))/24
        #daily_frequency_fix = len(index) / total_days
        #factor_returns_long_short_cv = factor_returns_long_short_mean/factor_returns_long_short_std*(daily_frequency_fix**0.5)
        factor_returns_long_short_cv = factor_returns_long_short_mean/factor_returns_long_short_std * (252**0.5)
    if scope['multiple_factors_data']:
        ###處理雜湊問題
        ind_cols_count = how_many_did_individual_use_by_cols(individual,require_cols)
        #假如資料無產生雜湊，fitness打八折(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if ind_cols_count<2:factor_returns_long_short_cv *= 0.8
        
        #計算因子與其使用之原始資料相關性
        mean_corr = yp_cols_corr(yp,target,individual, toolbox_compile,scope,require_cols)
        #假如資料與因子相關性過高(雜湊不足)，觸發懲罰(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if mean_corr>0.2:
            return abs(factor_returns_long_short_cv)*(1-mean_corr),factor_returns_long_short
        else:
            return abs(factor_returns_long_short_cv),factor_returns_long_short
    else:
        #return abs(factor_returns_long_short_cv),factor_returns_long_short
        return factor_returns_long_short_cv,factor_returns_long_short
def Debag(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    return individual,scope['DividendYield_TSE'],None

def LS_Fitness(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    #計算因子表達式長度
    expr_length = parse_expression(individual,only_get_length=True)
    if expr_length >= 6:
        return -5,None#假如資料表達式過長，fitness直接給成逞罰項
    #前處理
    pp_dict = preprocessing(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols)
    punish = pp_dict['punish']
    if punish:return punish,None
    yp = pp_dict['yp']
    target = pp_dict['target']
    factor_returns_long_short,Turnover = LS_return_fast(factor = yp,
                                                           ret = target,
                                                           buy_fee = 0.001,#0.001425*0.3,
                                                           sell_fee = 0.001,#0.001425*0.3+0.003,
                                                           get_Turnover = True)
    if Turnover < 0.01 or Turnover > 0.7:
        return -5,None#假如資料周轉率太高或太低，fitness直接給成逞罰項
    factor_returns_long_short_mean = factor_returns_long_short.mean()
    factor_returns_long_short_std = factor_returns_long_short.std()
    
    if factor_returns_long_short_std == 0 or np.isnan(factor_returns_long_short_std):
        return -10,None
    factor_returns_long_short_cv = factor_returns_long_short_mean/factor_returns_long_short_std * (252**0.5)
    if factor_returns_long_short_cv < 0.8:
        return -5,None#假如資料夏普超爛，fitness直接給成逞罰項
    
    factor_returns_long_short_cagr = (factor_returns_long_short+1).prod()**(1/(factor_returns_long_short.shape[0]/252)) - 1
    Fitness = factor_returns_long_short_cv * (abs(factor_returns_long_short_cagr)/max(Turnover,0.125))**(1/2)
    
    if factor_returns_long_short_cagr < 0.05:
        return -5,None#假如資料年化報酬超爛，fitness直接給成逞罰項
    
    if factor_returns_long_short_cagr <= 0.1:
        Fitness *= 0.8#假如資料年化報酬不夠，fitness打八折
        
    if factor_returns_long_short_cagr <= 0.15:
        Fitness *= 0.6#假如資料年化報酬不夠，fitness打六折
        
    if factor_returns_long_short_cv < 1:
        Fitness *= 0.8#假如資料夏普不夠，fitness打八折
    
    if scope['multiple_factors_data']:
        ###處理雜湊問題
        ind_cols_count = how_many_did_individual_use_by_cols(individual,require_cols)
        #假如資料無產生雜湊，fitness打八折(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if ind_cols_count<2:factor_returns_long_short_cagr *= 0.8
        
        #計算因子與其使用之原始資料相關性
        mean_corr = yp_cols_corr(yp,target,individual, toolbox_compile,scope,require_cols)
        #假如資料與因子相關性過高(雜湊不足)，觸發懲罰(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if mean_corr>0.2:
            return abs(factor_returns_long_short_cagr)*(1-mean_corr),factor_returns_long_short
        else:
            return abs(factor_returns_long_short_cagr),factor_returns_long_short
    else:
        return Fitness,factor_returns_long_short
    
def LS_cagr(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    #前處理
    pp_dict = preprocessing(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols)
    punish = pp_dict['punish']
    if punish:return punish,None
    yp = pp_dict['yp']
    target = pp_dict['target']
    factor_returns_long_short = LS_return_fast(yp,target)
    factor_returns_long_short_mean = factor_returns_long_short.mean()
    factor_returns_long_short_std = factor_returns_long_short.std()
    if factor_returns_long_short_std == 0 or np.isnan(factor_returns_long_short_std):
        return -10,None
    factor_returns_long_short_cv = factor_returns_long_short_mean/factor_returns_long_short_std * (252**0.5)
    if factor_returns_long_short_cv < 0.8:
        return -5,None#假如資料夏普超爛，fitness直接給成逞罰項
    
    factor_returns_long_short_cagr = (factor_returns_long_short+1).prod()**(1/(factor_returns_long_short.shape[0]/252)) - 1
    if factor_returns_long_short_cv < 1.5:
        factor_returns_long_short_cagr *= 0.8#假如資料夏普不夠，fitness打八折
        
    if scope['multiple_factors_data']:
        ###處理雜湊問題
        ind_cols_count = how_many_did_individual_use_by_cols(individual,require_cols)
        #假如資料無產生雜湊，fitness打八折(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if ind_cols_count<2:factor_returns_long_short_cagr *= 0.8
        
        #計算因子與其使用之原始資料相關性
        mean_corr = yp_cols_corr(yp,target,individual, toolbox_compile,scope,require_cols)
        #假如資料與因子相關性過高(雜湊不足)，觸發懲罰(適用於資訊間本身具有良好效果，希望雜湊出更好的因子時)
        if mean_corr>0.2:
            return abs(factor_returns_long_short_cagr)*(1-mean_corr),factor_returns_long_short
        else:
            return abs(factor_returns_long_short_cagr),factor_returns_long_short
    else:
        #return abs(factor_returns_long_short_cv),factor_returns_long_short
        return factor_returns_long_short_cagr,factor_returns_long_short
    
def LS_return_fast(factor,ret, buy_fee:float = 0.001425*0.3, sell_fee:float = 0.001425*0.3+0.003,get_Turnover = False):
    ret = ret.reindex_like(factor)
    LS_ret,Turnover = LS_ret_np(factor.values,ret.values,buy_fee,sell_fee)
    LS_ret_Se = pd.Series(LS_ret,index = ret.index)
    if get_Turnover:
        return LS_ret_Se,Turnover
    else:
        return LS_ret_Se
def get_fee_se_np(signal_W:np.array, buy_fee:float = 0.001425*0.3, sell_fee:float = 0.001425*0.3+0.003) -> np.array:
    def ts_delta_np(x:np.array, d:int) -> np.array:
        diff_arr = np.full_like(x, fill_value=np.nan, dtype=float)  # 創建一個與原始數組同形狀且所有元素都為nan的數組
        diff_arr[d:] = x[d:] - x[:-d]
        return diff_arr
    """
    輸入整個投組時間序列上的各標的權重DataFrame
    輸出每個時間序列上應支付的轉倉成本
    """
    # 計算 signal_W 的差
    signal_W[np.isnan(signal_W)] = 0
    signal_W_diff = ts_delta_np(signal_W,1)
    Turnover = np.nanmean(np.nansum(np.abs(signal_W_diff),axis = 1))
    
    # 計算買入和賣出的手續費
    buy_fee_se = np.sum(np.where(signal_W_diff > 0, signal_W_diff * buy_fee, 0), axis=1)
    sell_fee_se = np.sum(np.where(signal_W_diff < 0, np.abs(signal_W_diff) * sell_fee, 0), axis=1)

    # 總交易成本
    transaction_cost = buy_fee_se + sell_fee_se

    return transaction_cost,Turnover

def LS_ret_np(alpha_array:np.array,ret_array:np.array, buy_fee:float = 0.001425*0.3, sell_fee:float = 0.001425*0.3+0.003,only_long = False) -> np.array:
    demeaned = alpha_array - np.nanmean(alpha_array,axis = 1)[:, None]
    weights = demeaned / np.nansum(np.abs(demeaned),axis = 1)[:, None]
    
    weights[np.isnan(weights)] = 0
    weights[np.abs(np.nansum(weights,axis = 1))>0.1,:] = 0
    if only_long:
        weights[weights<0] = 0
        weights*=2
    #計算交易成本與周轉率
    fee_se_np,Turnover = get_fee_se_np(weights,buy_fee,sell_fee)

    weighted_returns = ret_array*weights
    #calculate LS_return
    alpha_returns_long_short = np.nansum(weighted_returns,axis = 1) - fee_se_np

    return alpha_returns_long_short,Turnover

def how_many_did_individual_use_by_cols(individual:str,require_cols:list[str])->int:
    ind_list = individual.replace(')',',').replace('(',',').replace(' ','').split(',')
    ind_cols_count = len(list(filter(lambda ind_str:ind_str in require_cols,ind_list)))
    return ind_cols_count
def yp_cols_corr(yp,target,individual, toolbox_compile,scope,require_cols):
    ts_ic_list = []
    func = toolbox_compile(expr=individual)
    scope['func'] = func
    ts_ic_list.append(yp.corrwith(target, axis = 1, method = "spearman"))
    
    ind_list = individual.replace(')',',').replace('(',',').replace(' ','').split(',')
    ind_cols = list(filter(lambda ind_str:ind_str in require_cols,ind_list))
    for _ in ind_cols:
        col = eval( _ , scope)
        #factor = col.stack(dropna = False)
        ts_ic_list.append(col.corrwith(target, axis = 1, method = "spearman"))
    if len(ts_ic_list) == 1:return 1
    corr_df = pd.concat(ts_ic_list,axis = 1).corr().abs()
    bool_index = pd.DataFrame(np.eye(corr_df.shape[0]),index = corr_df.index,columns = corr_df.columns) == 0
    mean_corr = np.nanmean(corr_df[bool_index])
    return mean_corr

import bottleneck as bn

def preprocessing(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    use_data_names = list(set(parse_expression(individual,False)[1]))
    for name_ in use_data_names:
        scope[name_] = pd.DataFrame(np.array(scope[name_]),index = target.index, columns = target.columns)
    func = toolbox_compile(expr=individual)
    scope['func'] = func
    yp = eval('func({})'.format(', '.join(require_cols)), scope)
    yp = yp[(yp.index >= time_constraint_from)
            & (yp.index <= time_constraint_to)]
    target = target[(target.index >= time_constraint_from)
                         & (target.index <= time_constraint_to)]

    #持倉塞選
    punish = 0
    factor_trade = yp.notna().sum(axis=1)
    average_tradeing_days_ratio = factor_trade.astype(bool).mean()
    average_number_of_trading_companies = factor_trade.mean()
    
    if average_tradeing_days_ratio < 0.5:
        punish-=10
    if average_number_of_trading_companies < 10:
        punish-=10
    #數據清洗
    #yp = yp.dropna(how='all', axis='columns')
    #yp = yp.dropna(how='all', axis='index')
    #target = target.reindex_like(yp).fillna(0)
    #yp = yp[np.isfinite(yp)].dropna(how='all',axis=1)

    return {'yp':yp,'target':target,'punish':punish}

def _IC_IR(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols):
    pp_dict = preprocessing(individual, toolbox_compile, target, time_constraint_from, time_constraint_to, scope, require_cols)
    punish = pp_dict['punish']
    yp = pp_dict['yp']
    target = pp_dict['target']
    #清洗資料
    target = target + yp*0
    yp = yp + target*0
    
    #normal_IC = yp.corrwith(target, axis = 1, method = "pearson")
    rank_IC = yp.corrwith(target, axis = 1, method = "spearman")
    ic = rank_IC
    ic_mean = ic.mean()
    ic_std = ic.std()
    if ic_std == 0:
        punish -= 10
        icir = np.nan
    else:
        icir = ic_mean / ic_std
    return {'ic_mean':ic_mean,'icir':icir,'punish':punish,'ts_ic':ic,'yp':yp,'target':target}

def parse_expression(expr,only_get_length = True):
    functions = list()
    data = list()
    params = list()
    def dfs(sub_expr):
        if '(' in sub_expr: 
            # Extract the function name
            function_name = re.search(r'(\w+)\(', sub_expr).group(1)
            functions.append(function_name)
            
            # Remove function name and outer parenthesis
            sub_expr = sub_expr[len(function_name)+1:-1]
            
            # Recursively parse arguments
            depth = 0
            arg_start = 0
            for i, char in enumerate(sub_expr):
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                elif char == ',' and depth == 0:
                    dfs(sub_expr[arg_start:i].strip())
                    arg_start = i+1
            dfs(sub_expr[arg_start:].strip())
        else:
            if re.match(r'^\d+$', sub_expr):  # Check if sub_expr is a number
                params.append(sub_expr)
            else:
                data.append(sub_expr)
    dfs(expr)
    total_length = len(functions+data)
    if only_get_length:
        return total_length
    return functions,data,params,total_length