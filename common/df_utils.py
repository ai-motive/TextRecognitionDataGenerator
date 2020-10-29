#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def get_min_max(x):
    return pd.Series(index=['min','max'],data=[x.min(),x.max()])

def conditional_sum(x):
    d = {}
    try:
        x = x.loc[x['CX01_CONV1_BLOW_FERCENT'] <= x['Dy. 시점'].unique()[0]]
        # print('CH_NO : {}, Dy. 시점 : {}'.format(x['CHARGE_NO'].unique()[0],x['Dy. 시점'].unique()[0]))
    except:
        pass
    columns = ['CX01_CONV1_CO_GAS', 'CX01_CONV1_CO2_GAS', 'CX01_CONV1_O2_GAS', 'CX01_CONV1_N2_FLOW', 'Dy. 시점']
    for col in columns:
        if col == 'Dy. 시점':
            d[col] = x[col].iloc[0]
        else:
            d[col] = x[col].sum()
    return pd.Series(d, index=columns)

def gen_new_col(row, tar_col):
    try:
        blow_percent = str(int(row['DYN_PERCNT']))
        result = row[tar_col + blow_percent]
        return result
    except (KeyError, ValueError):
        return None

def convert_data_type(series, tar_type):
    if tar_type == int:
        convert_series = pd.to_numeric(series, errors='coerce')
    elif tar_type == float:
        convert_series = pd.to_numeric(series, errors='coerce').astype(float)
    elif tar_type == str:
        convert_series = series.astype(str)
    return convert_series

def merge_values_in_series(series):
    merge_series = series.apply(pd.Series).stack().reset_index(drop=True)
    return merge_series