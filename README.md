# mds_trading_systems
Questo codice esegue il Backtest di una strategia di trading:
- che utilizza un indicatore tecnico tra RSI, CCI, OBV, SAR
- ogni indicatore viene trasformato: reso oscillatore in scala 0, 100, e viene smussato da una media a N periodi
- compra in zona di sottovalutazione e vende in zona di sopravvalutazione
- quando chiude la posizione Long, apre la Short (e viceversa)

Procedura per lanciare il codice:
- Installa i requirements
- Installa TA-Lib:
  - guida: https://blog.quantinsti.com/install-ta-lib-python/
  - download links: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
- Lancia il file MAIN.py
