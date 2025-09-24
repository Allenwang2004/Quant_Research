import os
from datetime import time
from datetime import datetime
import numpy as np
import pandas as pd
from deap_r import base, creator, tools, gp, algorithms
#from operators import *
from operators_v3 import *
import operators_v3
from fitness import *
#import pyarrow.feather as feather
import gc
import argparse
import random
import json
import warnings
import pathlib
import pickle
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

def creat_pop_from_str_list(pop_fun_str_list:list,pset)->list:
    return [creator.Individual.from_string(ind_fun_str, pset) for ind_fun_str in pop_fun_str_list]#直接定義因子式

#old_GPfactor_names_list = [
#                           'TW_weekily_GPfactor_in50_1',
#                           'TW_weekily_GPfactor_in50_2',
#                           'TW_weekily_GPfactor_in50_3',
#                           ]
old_GPfactor_names_list = []
old_good_pop_numbers = None
old_good_expression_list = []
if old_GPfactor_names_list:
    old_good_expression_list = pd.concat([pd.read_excel(f'./Results/{old_GPfactor_name}.xlsx') \
                                          for old_GPfactor_name in old_GPfactor_names_list]).cal.to_list()
old_good_expression_list = list(set(old_good_expression_list))
if not old_good_pop_numbers:
    old_good_expression_list = list(np.random.choice(old_good_expression_list,size=len(old_good_expression_list),replace=False))
else:
    old_good_expression_list = list(np.random.choice(old_good_expression_list,size=old_good_pop_numbers,replace=False))
#添加股池塞選
股池_bool = None

All_merge_factor_ret_dict = dict()
#做出 marge_ret_Se
#將新的因子目標設定成，(marge_ret_Se+新因子_ret)/2 的夏普最大化
#自動每輪得出新的expression_list並計算新的marge_ret_Se
#自動每輪輸出val的marge_ret_Se夏普以做觀察
def turn_expression_to_factors_dict(expressions_list,stack = False)->dict:
    with np.errstate(divide='ignore', invalid='ignore'):
        alpha_dict = dict()
        count = 0
        for fun_str in expressions_list:
            count+=1
            print(f'\r{count}/{len(expressions_list)}',end = '')
            alpha_dict[fun_str] = eval(fun_str)
            if stack:
                alpha_dict[fun_str] = alpha_dict[fun_str].stack(dropna = False)
        print()
    return alpha_dict
    
if __name__ == "__main__":
    start_time = datetime.now()
    print("Init variables.")
    args = json.load(open("./config.json", encoding="utf-8"))
    if args['OUTPUT_DATA_PATH'][:2] == './':
        args['OUTPUT_DATA_PATH'] = str(pathlib.Path().absolute())+args['OUTPUT_DATA_PATH'][1:]

    # Data preprocessing
    print("Load Data")
    if '.pkl' in args['TARGET_DATA_PATH']:
        target = pd.read_pickle(args['TARGET_DATA_PATH'])
    elif '.parquet' in args['TARGET_DATA_PATH']:
        target = pd.read_parquet(args['TARGET_DATA_PATH'])
    feature_path = args['PIVOT_DATA_PATH']
    Load_Data_pool = list(filter(lambda x:x[-4:] == '.pkl',os.listdir(feature_path)))
    feature_dict = {filename[:-4]:pd.read_pickle(os.path.join(feature_path ,filename)) for filename in Load_Data_pool}
    require_cols = list(feature_dict.keys())
    print(require_cols)
    
    target = target[(target.index >= args['DATE_FROM'])
                         & (target.index <= args['DATE_TO'])]
    for col in require_cols:
        
        locals()[col] = feature_dict[col][(feature_dict[col].index >= args['DATE_FROM'])
                                      & (feature_dict[col].index <= args['DATE_TO'])]
    target = target.replace([np.inf, -np.inf], np.nan)
    target = target.fillna(0)

    del feature_dict
    gc.collect()

    df_result = pd.DataFrame(columns=['cal', 'fitness'])
    df_ts_result = pd.DataFrame()
    #ind_result = pd.Series()
    count = 0
    if args['AMT']=="None" or args['AMT']=="inf": args['AMT'] = np.inf
    while len(df_result) < args['AMT']:
        random.seed(count+datetime.timestamp(start_time))#使用當下時間建立隨機種子
        print("Initialize Algorithm")
        time_constraint_from = args['DATE_FROM']
        time_constraint_to = args['DATE_TO']

        df_type = pd.core.frame.DataFrame
        pset = gp.PrimitiveSetTyped(
            "MAIN", [df_type] * len(require_cols), df_type, require_cols)
        Alpha_F = {"abs": operators_v3.abs,
                    "correlation": operators_v3.ts_corr_bn,
                    "covariance": operators_v3.covariance,
                    "cs_rank": operators_v3.cs_rank,
                    "cs_scale": operators_v3.cs_scale,
                    "delay": operators_v3.delay,
                    "log": operators_v3.log,
                    "max": operators_v3.max,
                    "min": operators_v3.min,
                    "sign": operators_v3.sign,
                    "signedpower": operators_v3.signedpower,
                    "ts_argmax": operators_v3.ts_argmax_bn,
                    "ts_argmin": operators_v3.ts_argmin_bn,
                    "ts_decay_linear": operators_v3.ts_decay_linear,
                    "ts_delta": operators_v3.ts_delta,
                    "ts_max": operators_v3.ts_max_bn,
                    "ts_min": operators_v3.ts_min_bn,
                    "ts_product": operators_v3.ts_product,
                    "ts_rank": operators_v3.ts_rank,
                    "ts_stddev": operators_v3.ts_std_bn,
                    "ts_sum": operators_v3.ts_sum_bn,
                    "where": operators_v3.where,
                    "ts_mean": operators_v3.ts_mean_bn}
        for Fun_name,Fun_object in Alpha_F.items():
            Fun_object.__name__ = Fun_name
            locals()[Fun_name] = Fun_object
        # normal operator
        pset.addPrimitive(abs, [df_type], df_type)
        pset.addPrimitive(log, [df_type], df_type)
        pset.addPrimitive(sign, [df_type], df_type)
        pset.addPrimitive(cs_rank, [df_type], df_type)
        pset.addPrimitive(delay, [df_type, int], df_type)
        pset.addPrimitive(correlation, [df_type, df_type, int], df_type)
        pset.addPrimitive(covariance, [df_type, df_type, int], df_type)
        pset.addPrimitive(cs_scale, [df_type, int], df_type)
        pset.addPrimitive(ts_delta, [df_type, int], df_type)
        pset.addPrimitive(signedpower, [df_type, int], df_type)
        pset.addPrimitive(ts_decay_linear, [df_type, int], df_type)
        pset.addPrimitive(ts_min, [df_type, int], df_type)
        pset.addPrimitive(ts_max, [df_type, int], df_type)
        pset.addPrimitive(ts_argmin, [df_type, int], df_type)
        pset.addPrimitive(ts_argmax, [df_type, int], df_type)
        pset.addPrimitive(ts_rank, [df_type, int], df_type)
        pset.addPrimitive(min, [df_type, df_type], df_type)
        pset.addPrimitive(max, [df_type, df_type], df_type)
        pset.addPrimitive(ts_sum, [df_type, int], df_type)
        pset.addPrimitive(ts_product, [df_type, int], df_type)
        pset.addPrimitive(ts_stddev, [df_type, int], df_type)
        #pset.addPrimitive(where, [df_type, df_type,df_type], df_type)
        pset.addPrimitive(ts_mean, [df_type, int], df_type)
        
        
        # terminals
        pset.addTerminal(1, int)
        pset.addTerminal(2, int)
        pset.addTerminal(3, int)
        pset.addTerminal(5, int)
        pset.addTerminal(10, int)
        pset.addTerminal(15, int)
        pset.addTerminal(20, int)
        pset.addTerminal(30, int)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree,
                       fitness=creator.FitnessMax)

        scope = {k: v for k, v in locals().items() if k in require_cols}
        scope["multiple_factors_data"] = args['multiple_factors_data']
        if type(股池_bool) == pd.DataFrame:
            scope['股池_bool'] = 股池_bool
        #scope["merge_strategy_ret_nofee"] = merge_strategy_ret_nofee
        toolbox = base.Toolbox()
        int_terminal_types = [int]
        toolbox.register("expr", gp.genHalfAndHalf, pset=pset,
                         min_=0, max_=3, terminal_types=int_terminal_types)
        toolbox.register("individual", tools.initIterate,
                         creator.Individual, toolbox.expr)
        toolbox.register("population", tools.initRepeat,
                         list, toolbox.individual)
        toolbox.register("compile", gp.compile, pset=pset)
        toolbox.register("evaluate", eval(args['FIT_FUNC']), toolbox_compile=toolbox.compile,
                         target=target, time_constraint_from=time_constraint_from, time_constraint_to=time_constraint_to, scope=scope, require_cols=require_cols)
        toolbox.register("select", tools.selTournament, tournsize=10)
        toolbox.register("mate", gp.cxOnePoint)
        toolbox.register("expr_mut", gp.genFull, min_=0, max_=1,
                         terminal_types=int_terminal_types)
        toolbox.register("mutate", gp.mutUniform,
                         expr=toolbox.expr_mut, pset=pset)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.nanmean)
        stats.register("std", np.nanstd)
        stats.register("min", np.nanmin)
        stats.register("max", np.nanmax)

        print("Start training")
        pop = toolbox.population(n=args['POP'])
        
        hof = tools.HallOfFame(args['POP'])

        population, logbook = algorithms.revise(
            pop, toolbox, 0.4, 0.2, n_generations=args['GEN'], n_elites=args['POP']//10, stats=stats, hall_of_fame=hof)
        #塞選hof
        corr_threshold = args['CORR_threshold']#-0.05
        if df_result.shape[0] < 100 and args['CORR_threshold']<0.9:corr_threshold = 0.9
        print('corr_threshold:',corr_threshold)
        Se_result = df_result.set_index('cal').fitness
        hof_fitness_Se = pd.Series(map(lambda x:x.fitness.values[0],hof.items))
        hof_fit_thres_Se = hof_fitness_Se[hof_fitness_Se>args['FIT_THRES']]
        print(f"Find {len(hof_fit_thres_Se)} survivors")
        old_cal = set(df_result.cal)
        if len(hof_fit_thres_Se):
            for index_name in hof_fit_thres_Se.index:
                ind = hof.items[index_name]
                name = str(ind)
                df_result = pd.concat([df_result,
                                      pd.DataFrame([[name,ind.fitness.values[0]]],columns = ['cal','fitness'])],
                                      ignore_index=True)
                df_ts_result[name] = ind.ts_result
                #ind_result[name] = ind
            df_result = df_result.drop_duplicates(subset=['cal'], keep='first')
            Se_result = df_result.set_index('cal').fitness
            Se_result = Se_result.sort_values(ascending=False)

            df_ts_result = df_ts_result.T
            df_ts_result['date'] = df_ts_result.index
            df_ts_result = df_ts_result.drop_duplicates(subset=['date'], keep='first').drop(columns = 'date').T
            df_ts_result = df_ts_result[Se_result.index]
            
            corr_df = df_ts_result.corr().abs()
            delete_factor_name_list = list()
            for index in df_ts_result.columns.to_list():
                for columns in df_ts_result.columns.to_list():
                    corr_ = corr_df.loc[index,columns]
                    if all([corr_>corr_threshold,
                             index!=columns,
                             Se_result[index]>=Se_result[columns],
                             columns not in delete_factor_name_list,
                             index not in delete_factor_name_list]):
                        #print(f'刪除編號:{columns}因子')
                        delete_factor_name_list.append(columns)
            survive_name_list = sorted(set(df_ts_result.columns.to_list())-set(delete_factor_name_list))
            df_ts_result = df_ts_result[survive_name_list]
            Se_result = Se_result[survive_name_list]
            #ind_result = ind_result[survive_name_list]
            df_result = Se_result.reset_index()
            #二度檢查
            df_result = df_result.drop_duplicates(subset=['cal'], keep='first')
            df_result = df_result[df_result['fitness'] > args['FIT_THRES']].sort_values(
                'fitness', ascending=False).reset_index(drop=True)
            df_ts_result = df_ts_result[df_result.cal]
            #檢查相關度是否有誤
            corr_df = df_ts_result.corr().abs()
            bool_index = pd.DataFrame(np.eye(corr_df.shape[0]),index = corr_df.index,columns = corr_df.columns) == 0
            if (corr_df[bool_index]>corr_threshold).sum().sum():
                import sys
                sys.exit("發現相關度有錯誤!!!!!!!!!!!")
        print(f'update {len(set(df_result.cal)-old_cal)} survivors')
        print(f'total find {len(df_result)} survivors')
        if len(df_result) < args['AMT']:
            print(f"{args['AMT'] - len(df_result)} more survivors needed")
        count += 1
        df_result.to_csv(args['OUTPUT_DATA_PATH'], index=False)
        args['Operation worlds'] = f'spend {count} worlds'
        args['Operation times'] = f'Use {datetime.now()-start_time}'
        args['random seed start by'] = datetime.timestamp(start_time)
        save_path = '/'.join(args['OUTPUT_DATA_PATH'].split('/')[:-1])+'/'
        with pd.ExcelWriter(save_path+args['OUTPUT_DATA_PATH'].split('/')[-1].split('.')[0]+'.xlsx') as writer:  
            df_result.to_excel(writer, sheet_name='factor')
            pd.DataFrame.from_dict(args,orient='index').rename(columns={0:'Info'}).to_excel(writer, sheet_name='Info')
        print('='*20)
    
    print(df_result)
    print(f'start_by:{start_time}')
    print(f'end_by:{datetime.now()}')
    print(f'spend {count} worlds')
    print(f'Use {datetime.now()-start_time}')