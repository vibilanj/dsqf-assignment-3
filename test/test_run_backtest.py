"""
This module is responsible for testing the functions that simulate
the backtest
"""
import sys
import unittest

import pandas as pd

from src.run_backtest import (DATE_FORMAT, IC, MOMENTUM, PREDICTED_RETURN,
                              REVERSAL, STOCK, STRATEGY1_COEFF,
                              STRATEGY1_RETURN, STRATEGY2_COEFF,
                              STRATEGY2_RETURN, RunBacktest)

sys.path.append("/.../src")

# Ticker Constants
AMZN = "AMZN"
NFLX = "NFLX"
SPY = "SPY"
WMT = "WMT"

class TestRunBacktest(unittest.TestCase):
  """
  Defines the TestRunBacktest class which tests the RunBacktest class.
  """
  tickers = [AMZN, NFLX, SPY, WMT]

  # RunBacktest parameters
  start_str = "20230101"
  end_str = "20230410"
  initial_aum = 10000
  strategy1 = MOMENTUM
  strategy2 = REVERSAL
  days1 = 50
  days2 = 5
  top_pct = 50

  path = "./test/data/run_backtest/"
  stocks_data = dict()
  for ticker in tickers:
    stock_data = pd.read_csv(path + ticker + ".csv",
                             parse_dates=["Date"],
                             index_col="Date")
    stock_data.index = stock_data.index.map(pd.Timestamp)
    stocks_data[ticker] = stock_data

  def init_run_backtest(self):
    """
    Tests the RunBacktest class instantiation.
    """
    return RunBacktest(
      self.stocks_data,
      self.initial_aum,
      self.start_str,
      self.strategy1,
      self.strategy2,
      self.days1,
      self.days2,
      self.top_pct)
  
  def test_get_month_end_indexes_from_b(self):
    """
    Tests the get_month_end_indexes_from_b method.
    """
    rbt = self.init_run_backtest()
    self.assertEqual(len(rbt.month_end_indexes), 4)
    date_indexes = self.stocks_data[self.tickers[3]].index
    expected = ["20221230", "20230131", "20230228", "20230331"]
    for idx, month_end_index in enumerate(rbt.month_end_indexes):
      self.assertEqual(date_indexes[month_end_index].strftime(DATE_FORMAT),
                       expected[idx])

  def test_get_feature_m50(self):
    """
    Tests the get_feature method for momentum strategy.
    """
    rbt = self.init_run_backtest()
    feature = rbt.get_feature(self.tickers[3],
                               self.strategy1,
                               self.days1,
                               rbt.month_end_indexes[1])
    self.assertAlmostEqual(feature, 6.402901975)

  def test_get_feature_r5(self):
    """
    Tests the get_feature method for reversal strategy.
    """
    rbt = self.init_run_backtest()
    feature = rbt.get_feature(self.tickers[3],
                               self.strategy2,
                               self.days2,
                               rbt.month_end_indexes[1])
    self.assertAlmostEqual(feature, 0.5943201811)

  def test_get_label(self):
    """
    Tests the get_label method.
    """
    rbt = self.init_run_backtest()
    label = rbt.get_label(self.tickers[2],
                          rbt.month_end_indexes[2])
    self.assertAlmostEqual(label, -2.514270969)

  def test_update_monthly_training_data(self):
    """
    Tests the update_monthly_training_data method.
    """
    rbt = self.init_run_backtest()
    self.assertEqual(len(rbt.model_training_data.index), 0)
    rbt.update_monthly_training_data(rbt.month_end_indexes[1])
    print(rbt.model_training_data[STRATEGY1_RETURN][0])
    self.assertEqual(len(rbt.model_training_data.index), len(self.tickers))
    expected_strategy1_return = [-19.43647776,
                                 33.80758169,
                                 7.94668542,
                                 13.80128421]
    expected_strategy2_return = [0.250625471,
                                 -0.9638942459,
                                 0.4491470511,
                                 -1.177856641]
    for i in range(len(self.tickers)):
      self.assertAlmostEqual(rbt.model_training_data.iloc[i][STRATEGY1_RETURN],
                             expected_strategy1_return[i])
      self.assertAlmostEqual(rbt.model_training_data.iloc[i][STRATEGY2_RETURN],
                             expected_strategy2_return[i])

  def test_fit_model_and_store_statistics_first_month(self):
    """
    Tests the fit_model_and_store_statistics method for the first month.
    """
    rbt = self.init_run_backtest() 
    rbt.update_monthly_training_data(rbt.month_end_indexes[1]) 
    model = rbt.fit_model_and_store_statistics()
    self.assertEqual(len(rbt.model_statistics_record.index), 1)
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[0][STRATEGY1_COEFF], -0.06298238419)
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[0][STRATEGY2_COEFF], 1.651083787)
    # TODO T-value
  
  def test_fit_model_and_store_statistics_initial_second_month(self):
    """
    Tests the fit_model_and_store_statistics method for the second month.
    """
    rbt = self.init_run_backtest() 
    rbt.update_monthly_training_data(rbt.month_end_indexes[1]) 
    model1 = rbt.fit_model_and_store_statistics()
    rbt.update_monthly_training_data(rbt.month_end_indexes[2]) 
    model2 = rbt.fit_model_and_store_statistics()
    self.assertEqual(len(rbt.model_statistics_record.index), 2)
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[1][STRATEGY1_COEFF], 0.01157124919)
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[1][STRATEGY2_COEFF], -1.1538965)
    # TODO T-value

  def test_predict_return(self):
    """
    Tests the predict_return method.
    """
    rbt = self.init_run_backtest()
    rbt.update_monthly_training_data(rbt.month_end_indexes[1]) 
    model1 = rbt.fit_model_and_store_statistics()
    predicted_returns = rbt.predict_returns(rbt.month_end_indexes[1])
    expected_returns = {
      self.tickers[0]: 27.17067977,
      self.tickers[1]: 8.751917726,
      self.tickers[2]: 16.1194461,
      self.tickers[3]: 14.37463767
    }
    for ticker in self.tickers:
      predicted_return = predicted_returns.loc[predicted_returns[STOCK] == ticker].iloc[0][PREDICTED_RETURN]
      self.assertAlmostEqual(predicted_return, expected_returns[ticker])
    
  def test_select_stocks_to_buy(self):
    """
    Tests the select_stocks_to_buy method.
    """
    rbt = self.init_run_backtest()
    rbt.update_monthly_training_data(rbt.month_end_indexes[1]) 
    model1 = rbt.fit_model_and_store_statistics()
    predicted_returns = rbt.predict_returns(rbt.month_end_indexes[1]) 
    stocks_to_buy = rbt.select_stocks_to_buy(rbt.month_end_indexes[1])
    self.assertListEqual(stocks_to_buy, [AMZN, SPY])
  
  def test_calc_portfolio(self):
    """
    Tests the calc_portfolio method.
    """
    rbt = self.init_run_backtest()
    portfolio= rbt.calc_portfolio([AMZN, WMT], 10000, rbt.month_end_indexes[1])
    self.assertAlmostEqual(portfolio[0][1], 48.48249911)
    self.assertAlmostEqual(portfolio[1][1], 34.89604083)
    
  def test_calc_aum(self):
    """
    Tests the calc_aum method.
    """
    rbt = self.init_run_backtest()
    amt_AMZN = 15
    amt_WMT = 40
    rbt.portfolio = [(AMZN, amt_AMZN), (WMT, amt_WMT)]
    self.assertAlmostEqual(rbt.calc_aum(rbt.month_end_indexes[2]), 7075.44406891)
  
  def test_calc_dividends(self):
    """
    Tests the calc_dividends method.
    """
    rbt = self.init_run_backtest()
    amt_AMZN = 80
    amt_SPY = 20
    rbt.portfolio = [(AMZN, amt_AMZN), (SPY, amt_SPY)]   
    self.assertAlmostEqual(rbt.calc_dividends(203), amt_SPY * 1.366 + amt_AMZN * 0)

  def test_fill_up_portfolio_performance(self):
    """
    Tests the fill_up_portfolio_performance method.
    """
    rbt = self.init_run_backtest()
    rbt.fill_up_portfolio_performance()
    self.assertEqual(len(rbt.model_statistics_record.index), 3)
    self.assertEqual(len(rbt.portfolio_record), 3)
    self.assertEqual(len(rbt.model_training_data.index), 3 * len(self.tickers))
    last_stocks = [stock for stock, _ in rbt.portfolio]
    self.assertListEqual(last_stocks, [SPY, WMT])
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[-1][STRATEGY1_COEFF], 0.05126014085)
    self.assertAlmostEqual(rbt.model_statistics_record.iloc[-1][STRATEGY2_COEFF], -0.7767555499)

  def test_calc_ic(self):
    """
    Tests the calc_ic method.
    """
    rbt = self.init_run_backtest()
    rbt.fill_up_portfolio_performance()
    rbt.calc_ic()
    self.assertEqual(rbt.monthly_ic.at[1, IC], 0)
  