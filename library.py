import datetime
import pandas as pd
import numpy as np
import zipfile
import os

def convert_dt(row):
  dt_str = row['d'] + ' ' + row['t']
  date_time_obj = datetime.datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")
  return date_time_obj


def get_data(file_name, year_from=None):
  # file_name ==> 'eurusd-1h'
  file_path_zip = 'data/'+file_name+'.zip'
  file_path_csv = 'data/'+file_name+'.csv'

  with zipfile.ZipFile(file_path_zip, 'r') as zip_ref: # diszippo file
    zip_ref.extractall('data')
  
  df = pd.read_csv(file_path_csv, sep=';', names=['d','t','Open','High','Low','Close','Volume'])

  if os.path.exists(file_path_csv):
    os.remove(file_path_csv)

  df['Volume'] = df['Volume'].astype(np.float64)
  df['DateTime'] = df.apply(convert_dt, axis=1)
  df = df.set_index('DateTime')
  df.index = df.index + pd.Timedelta(hours=7)
  df.drop(columns=['d', 't'])
  if type(year_from) == int:
    df = df[df.index.date >= datetime.date(year_from,1,1)]
  return df



def get_df_from_v_backtests(v_ind_names, v_backtests):
  rows = ['# Trades', 'Return [%]', 'Win Rate [%]', 'Avg. Trade [%]', 'Return (Ann.) [%]', 'Volatility (Ann.) [%]', 'RR (Ann.)', 'Profit Factor', 'Sharpe Ratio', 'Sortino Ratio', 'Max. Drawdown [%]']
  df = pd.DataFrame(index = rows)
  for i,x in enumerate(v_backtests):
    v_stats = []
    for r in rows:
      if r == 'RR (Ann.)':
        metric = x.stats['Return (Ann.) [%]'] / x.stats['Volatility (Ann.) [%]']
      else:
        metric = x.stats[r]
      if type(metric) == float:
        metric = round(metric, 2)
      v_stats.append(metric)
    df[v_ind_names[i]] = v_stats
  return df



def print_pretty_table(df):
  from tabulate import tabulate
  #df = pd.DataFrame({'col_two' : [0.0001, 1e-005 , 1e-006, 1e-007], 'column_3' : ['ABCD', 'ABCD', 'long string', 'ABCD']})

  print(tabulate(df, headers='keys', tablefmt='psql'))
  '''
    +----+-----------+-------------+
    |    |   col_two | column_3    |
    |----+-----------+-------------|
    |  0 |    0.0001 | ABCD        |
    |  1 |    1e-05  | ABCD        |
    |  2 |    1e-06  | long string |
    |  3 |    1e-07  | ABCD        |
    +----+-----------+-------------+
  '''