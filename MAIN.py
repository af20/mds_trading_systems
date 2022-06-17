from backtesting.backtesting import Backtest
import pandas as pd
from library import *
from c_trading_strategies import *

upper_bound = 70
lower_bound = 30
indicator_window = 14
mean_periods = 7


my_data = get_data('eurusd-1h', year_from=2021)
v_backtests = []
bt = Backtest(my_data, c_Oscillator_Strategy, cash=100_000)#, commission=.002)
v_ind_names = ['RSI', 'CCI', 'OBV', 'SAR']
for ind_name in v_ind_names:
  print('   INDICATOR name', ind_name)
  stats = bt.run(indicator_name=ind_name, upper_bound=upper_bound, lower_bound=lower_bound, indicator_window=indicator_window, mean_periods=mean_periods)
  v_backtests.append(c_BT_Stats(ind_name, bt, stats))

df = get_df_from_v_backtests(v_ind_names, v_backtests)
print_pretty_table(df)
