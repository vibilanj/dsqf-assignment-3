import sys
from src.input_data import InputData
from src.stocks_fetcher import StocksFetcher
from src.run_backtest import RunBacktest
from src.backtest_stats import BacktestStats

import os

# RunBacktest parameters
start_str = "20230101"
end_str = "20230410"
initial_aum = 10000
strategy1 = MOMENTUM
strategy2 = REVERSAL
days1 = 50
days2 = 5
top_pct = 50
path = "./test/data/"
stocks_data = dict()
filenames = os.listdir(path)
for filename in filenames:
  stock_data = pd.read_csv(path + filename, parse_dates=["Date"], index_col="Date")
  stock_data.index = stock_data.index.map(pd.Timestamp)
  stocks_data[filename.replace(".csv", "")] = stock_data