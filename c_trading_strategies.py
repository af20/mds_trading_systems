from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd
import pandas_ta as pd_ta
import talib as ta
from sklearn import preprocessing
import numpy as np

class c_BT_Stats:
  def __init__(self, indicator_name, bt, stats):
    self.indicator_name = indicator_name
    self.bt = bt
    self.stats = stats
    print(stats)
    bt.plot()
    '''
      Index(['Start', 'End', 'Duration', 'Exposure Time [%]', 'Equity Final [$]',
            'Equity Peak [$]', 'Return [%]', 'Buy & Hold Return [%]',
            'Return (Ann.) [%]', 'Volatility (Ann.) [%]', 'Sharpe Ratio',
            'Sortino Ratio', 'Calmar Ratio', 'Max. Drawdown [%]',
            'Avg. Drawdown [%]', 'Max. Drawdown Duration', 'Avg. Drawdown Duration',
            '# Trades', 'Win Rate [%]', 'Best Trade [%]', 'Worst Trade [%]',
            'Avg. Trade [%]', 'Max. Trade Duration', 'Avg. Trade Duration',
            'Profit Factor', 'Expectancy [%]', 'SQN', '_strategy', '_equity_curve',
            '_trades'],
    '''




class c_Oscillator_Strategy(Strategy): # 13:44
  indicator_name = None
  upper_bound = 70
  lower_bound = 30
  indicator_window = 14
  mean_periods = 7


  # Do as much initial computation as possible
  '''(init) This function is called as soon as the object is created and is only run once. You should put in here anything that can be pre-calculated ahead of time before your backtest, such as any technical indicators.'''
  def init(self):
    super().init()
    match self.indicator_name:
      case 'RSI':
        #self.indic = self.I(pd_ta.rsi, pd.Series(self.data.Close), indicator_window)
        self.indic = self.I(ta.RSI, pd.Series(self.data.Close), self.indicator_window)
        self.indic = self.I(self.M_Avg, self.indic)
      case 'CCI':
        self.indic = self.I(ta.CCI, self.data['High'], self.data['Low'], self.data['Close'], timeperiod=self.indicator_window)
        #self.indic = self.I(pd_ta.cci, pd.Series(self.data['High']), pd.Series(self.data['Low']), pd.Series(self.data['Close']), length=indicator_window)
        self.indic = self.I(self.min_max_scaler, self.indic)
        self.indic = self.I(self.M_Avg, self.indic)

      case 'OBV':
        self.indic = self.I(ta.OBV, self.data['Close'], self.data['Volume'])
        #self.indic = self.I(self.min_max_scaler, self.indic)
        self.indic = self.I(ta.RSI, self.indic)
        self.indic = self.I(self.M_Avg, self.indic)

      case 'SAR':
        self.indic = self.I(ta.SAR, self.data['High'], self.data['Low'])
        #self.indic = self.I(self.min_max_scaler, self.indic)
        self.indic = self.I(ta.RSI, self.indic)
        self.indic = self.I(self.M_Avg, self.indic)
    self.signal = self.I(self.get_signals, self.indic)


  # Step through bars one by one  # Note that multiple buys are a thing here
  def next(self):
    super().init()

    #if crossover(self.indic, self.upper_bound):
    #if (self.sma1[-2] < self.sma2[-2] and self.sma1[-1] > self.sma2[-1]):


    if self.signal[-1] in [1, -1]:
      #print('  signal', self.signal[-1], '   LEN', len(self.signal), '     indic[-1]', self.indic[-1], '    indic[-2]', self.indic[-2], '    indic[-3]', self.indic[-3], '        position', self.position, '    is sh:', self.position.is_short, '   is lo', self.position.is_long)
      if self.signal[-1] == 1:
        if self.position.is_short or not self.position:
          if self.position:
            self.position.close()
          self.buy()#size=10) # entra all'open di questo giorno

      #elif crossover(self.lower_bound, self.indic):
      elif self.signal[-1] == -1:
        if self.position.is_long or not self.position:
          if self.position:
            self.position.close()
          self.sell()#size=10) # entra all'open di questo giorno
    

    if 1==2 and self.position:
      print( self.trades)
      print('  open', self.data['Open'][19], '    close:',  self.data['Close'][19])



  def min_max_scaler(self, v_data):
    min_max_scaler = preprocessing.MinMaxScaler()
    x = np.array(v_data).reshape(-1, 1) # returns a numpy array
    v_scaled = min_max_scaler.fit_transform(x)
    v_scaled = [x[0]*100 for x in v_scaled]
    return v_scaled



  def M_Avg(self, v_data):
    LEN_nan = len(v_data[np.isnan(v_data)]) 
    N = self.mean_periods
    v_data = v_data[~np.isnan(v_data)]
    b = np.array([v_data[0] for x in range(LEN_nan)])
    v_data = np.concatenate((b, v_data), axis=0)

    cumsum = np.cumsum(np.insert(v_data, 0, 0)) 
    v_mean = (cumsum[N:] - cumsum[:-N]) / float(N)
    b = np.array([v_mean[0] for x in range(N-1)])
    v_mean = np.concatenate((v_mean, b), axis=0)
    return v_mean



  def get_signals(self, v_values):
    #import random;    random.seed(9001)   ; rnd = random.randint(1, 10) / 100
    
    last_signal = 0
    v_signals = []

    for i,x in enumerate(v_values):
      
      if i <= 1:
        signal = 0
      else:
        if v_values[i-2] >= self.upper_bound and v_values[i-1] < self.upper_bound and last_signal != -1:
          signal = -1
        elif v_values[i-2] <= self.lower_bound and v_values[i-1] > self.lower_bound and last_signal != 1:
          signal = 1
        else:
          signal = 0

      v_signals.append(signal)

      if signal in [1, -1]:
        last_signal = signal

    #count_1 = sum([1 for x in v_signals if x == 1]);count_m1 = sum([1 for x in v_signals if x == -1])
    #idx_1 = [i for i,x in enumerate(v_signals) if x == 1];idx_m1 = [i for i,x in enumerate(v_signals) if x == -1]
    #print('   len(v_values)', len(v_values),'   len(v_signals)', len(v_signals), '        count_1', count_1, '    count_m1', count_m1)
    return v_signals

