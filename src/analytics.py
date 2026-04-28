import pandas as pd
import numpy as np
from scipy import stats

def monthly_anova(df, start_year=2014, end_year=2024):
    d = df[(df.date.dt.year >= start_year) & (df.date.dt.year <= end_year)].dropna(subset=['daily_return','month'])
    groups = [g.daily_return.values for _, g in d.groupby('month')]
    f_stat, p_value = stats.f_oneway(*groups)
    return {'f_statistic': float(f_stat), 'p_value': float(p_value), 'n': int(len(d))}

def create_crossover_events(df):
    out = df.copy()
    out['signal'] = (out['ma_50'] > out['ma_200']).astype(int)
    out['crossover'] = out['signal'].diff()
    out['crossover_type'] = pd.Series(pd.NA, index=out.index, dtype='object')
    out.loc[out.crossover == 1, 'crossover_type'] = 'Bullish'
    out.loc[out.crossover == -1, 'crossover_type'] = 'Bearish'
    for h in [3, 5, 10]:
        out[f'return_{h}d'] = out['close'].shift(-h) / out['close'] - 1
    return out[out['crossover_type'].notna()].copy()

def msft_qqq_correlation(msft, qqq):
    q = qqq[['date','close']].copy()
    q['qqq_return'] = q.close.pct_change()
    merged = msft[['date','daily_return']].rename(columns={'daily_return':'msft_return'}).merge(q[['date','qqq_return']], on='date').dropna()
    r, p = stats.pearsonr(merged.msft_return, merged.qqq_return)
    return {'correlation': float(r), 'p_value': float(p), 'n': int(len(merged))}
