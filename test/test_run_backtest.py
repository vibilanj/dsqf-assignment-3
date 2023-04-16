"""
This module is responsible for testing the functions that simulate
the backtest
"""
import sys
import unittest
from src.stocks_fetcher import StocksFetcher, DATE_FORMAT
from src.run_backtest import RunBacktest, MOMENTUM, REVERSAL, CLOSE_PRICE
from random import randint
import pandas as pd
import os
import pytz

sys.path.append("/.../src")

class TestRunBacktest(unittest.TestCase):
  """
  Defines the TestRunBacktest class which tests the RunBacktest class.
  """

  tickers = ["WMT", "AMZN", "NFLX", "SPY"]

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
    date_indexes = self.stocks_data[self.tickers[0]].index
    expected = ["20221230", "20230131", "20230228", "20230331"]
    for idx, month_end_index in enumerate(rbt.month_end_indexes):
      self.assertEqual(date_indexes[month_end_index].strftime(DATE_FORMAT), 
                       expected[idx])

  def test_get_feature_M50(self):
    """
    _summary_
    """
    rbt = self.init_run_backtest()
    feature = rbt.get_feature(self.tickers[0], 
                               self.strategy1, 
                               self.days1, 
                               rbt.month_end_indexes[1])
    self.assertAlmostEqual(feature, 6.402901975)

  def test_get_feature_R5(self):
    """
    _summary_
    """
    rbt = self.init_run_backtest()
    feature = rbt.get_feature(self.tickers[0], 
                               self.strategy2, 
                               self.days2, 
                               rbt.month_end_indexes[1])
    self.assertAlmostEqual(feature, 0.5943201811) 

  def test_get_label(self):
    """
    _summary_
    """
    rbt = self.init_run_backtest()
    label = rbt.get_label(self.tickers[3],
                          rbt.month_end_indexes[2])
    self.assertAlmostEqual(label, -2.514270969)


  # def test_calc_stocks_to_buy_m(self):
  #   """
  #   Tests the calc_stocks_to_buy method for momentum.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   num_stocks_to_buy = int(len(self.tickers_str) * self.top_pct / 100)
  #   stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   self.assertEqual(len(stocks_to_buy_m), num_stocks_to_buy)
  #   self.assertTrue(self.ticker_3 in stocks_to_buy_m \
  #                   and self.ticker_5 in stocks_to_buy_m)

  # def test_calc_stocks_to_buy_r(self):
  #   """
  #   Tests the calc_stocks_to_buy method for reversal.
  #   """
  #   run_backtest = self.init_run_backtest(REVERSAL)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   num_stocks_to_buy = int(len(self.tickers_str) * self.top_pct / 100)
  #   stocks_to_buy_r = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   self.assertEqual(len(stocks_to_buy_r), num_stocks_to_buy)
  #   self.assertTrue(self.ticker_1 in stocks_to_buy_r \
  #                   and self.ticker_3 in stocks_to_buy_r)

  # def test_calc_portfolio_first_positioning_m(self):
  #   """
  #   Tests the calc_stocks_to_buy and calc_portfolio methods for momentum.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   new_portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
  #                                               self.initial_aum,
  #                                               first_month_end_index)
  #   total_aum = 0
  #   for stock, amount in new_portfolio:
  #     total_aum += \
  #       self.stocks_data[stock].iloc[first_month_end_index][CLOSE_PRICE] \
  #         * amount
  #   self.assertEqual(int(total_aum), self.initial_aum)

  # def test_calc_portfolio_first_positioning_r(self):
  #   """
  #   Tests the calc_stocks_to_buy and calc_portfolio methods for reversal.
  #   """
  #   run_backtest = self.init_run_backtest(REVERSAL)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   stocks_to_buy_r = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   new_portfolio = run_backtest.calc_portfolio(stocks_to_buy_r,
  #                                               self.initial_aum,
  #                                               first_month_end_index)
  #   total_aum = 0
  #   for stock, amount in new_portfolio:
  #     total_aum += \
  #       self.stocks_data[stock].iloc[first_month_end_index][CLOSE_PRICE] \
  #         * amount
  #   self.assertEqual(int(total_aum), self.initial_aum)

  # def test_init_portfolio_performance(self):
  #   """
  #   Tests the init_portfolio_performance and portfolio_performance methods.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   run_backtest.init_portfolio_performance()
  #   portfolio_performance_len = len(run_backtest.portfolio_performance)
  #   self.assertEqual(portfolio_performance_len, \
  #                    len(self.stocks_data[self.ticker_1]))
  #   self.assertEqual(\
  #     run_backtest.portfolio_performance.at[\
  #     randint(0, portfolio_performance_len - 1), "aum"], self.initial_aum)

  # def test_calc_aum_first_positioning(self):
  #   """
  #   Tests the calc_aum method.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
  #                                                        self.initial_aum,
  #                                                        first_month_end_index)
  #   self.assertEqual(run_backtest.calc_aum(first_month_end_index),
  #                    self.initial_aum)

  # def test_calc_aum_day_after_first_positioning(self):
  #   """
  #   Tests the calc_aum method.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
  #                                                        self.initial_aum,
  #                                                        first_month_end_index)
  #   self.assertAlmostEqual(run_backtest.calc_aum(first_month_end_index + 1),
  #                          10238.9627300)

  # def test_calc_dividends_0(self):
  #   """
  #   Tests the calc_dividends method.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
  #   stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
  #   run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
  #                                                        self.initial_aum,
  #                                                        first_month_end_index)
  #   self.assertEqual(run_backtest.calc_dividends(first_month_end_index), 0)

  # def test_calc_dividends_not_0(self):
  #   """
  #   Tests the calc_dividends method.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   msft_stocks_owned = 20
  #   run_backtest.portfolio = [(self.ticker_3, msft_stocks_owned)]
  #   # based on dividend earned on 2023-02-15 00:00:00-05:00
  #   self.assertEqual(run_backtest.calc_dividends(314), msft_stocks_owned * 0.68)

  # def test_fill_up_portfolio_performance_on_second_position_dates_m(self):
  #   """
  #   Tests the fill_up_portfolio_performance method.
  #   """
  #   run_backtest_auto = self.init_run_backtest(MOMENTUM)
  #   run_backtest_auto.fill_up_portfolio_performance()

  #   run_backtest_manual = self.init_run_backtest(MOMENTUM)
  #   month_end_indexes = run_backtest_manual.get_month_end_indexes_from_b()
  #   first_month_end_index = month_end_indexes[0]
  #   first_pos_stocks_to_buy_m = \
  #     run_backtest_manual.calc_stocks_to_buy(first_month_end_index)
  #   run_backtest_manual.portfolio = \
  #     run_backtest_manual.calc_portfolio(first_pos_stocks_to_buy_m,
  #                                        self.initial_aum,
  #                                        first_month_end_index)

  #   second_month_end_index = month_end_indexes[1]
  #   previous_aum = run_backtest_manual.calc_aum(second_month_end_index - 1)
  #   second_pos_stocks_to_buy_m = \
  #     run_backtest_manual.calc_stocks_to_buy(second_month_end_index)
  #   run_backtest_manual.portfolio = \
  #     run_backtest_manual.calc_portfolio(second_pos_stocks_to_buy_m,
  #                                        previous_aum,
  #                                        second_month_end_index)
  #   res_second_month_end_index_aum = \
  #     run_backtest_manual.calc_aum(second_month_end_index)
  #   # comparing aum
  #   res_auto = run_backtest_auto.portfolio_performance.at[29, "aum"]
  #   self.assertAlmostEqual(res_auto, res_second_month_end_index_aum)
  #   self.assertAlmostEqual(res_auto, 10750.4649708)

  # def test_fill_up_portfolio_performance_end_m(self):
  #   """
  #   Tests the fill_up_portfolio_performance method for momentum.
  #   """
  #   run_backtest = self.init_run_backtest(MOMENTUM)
  #   run_backtest.fill_up_portfolio_performance()
  #   last_index = len(run_backtest.portfolio_performance) - 1
  #   self.assertAlmostEqual(\
  #     run_backtest.portfolio_performance.at[last_index, "aum"], 10566.8301891)

  # def test_fill_up_portfolio_performance_end_r(self):
  #   """
  #   Tests the fill_up_portfolio_performance method for reversal.
  #   """
  #   run_backtest = self.init_run_backtest(REVERSAL)
  #   run_backtest.fill_up_portfolio_performance()
  #   last_index = len(run_backtest.portfolio_performance) - 1
  #   self.assertAlmostEqual(\
  #     run_backtest.portfolio_performance.at[last_index, "aum"], 10141.2860640)

  # start_str_calc_ic = "20221217"
  # stocks_data_calc_ic = ticker_obj.fetch_stocks_data(tickers_str,
  #                                                    start_str_calc_ic,
  #                                                    end_str)
  # top_pct_calc_ic = 80

  # def init_run_backtest_calc_ic(self, strategy: str):
  #   """
  #   Tests the RunBacktest class instantiation.
  #   """
  #   return RunBacktest(
  #     self.stocks_data,
  #     self.initial_aum,
  #     self.start_str_calc_ic,
  #     self.days,
  #     strategy,
  #     self.top_pct_calc_ic)

  # def test_calc_ic_m(self):
  #   """
  #   Tests the calc_ic method for momentum.
  #   """
  #   run_backtest = self.init_run_backtest_calc_ic(MOMENTUM)
  #   run_backtest.fill_up_portfolio_performance()
  #   run_backtest.calc_ic()
  #   self.assertEqual(run_backtest.monthly_ic.at[0, "ic"], 1)
  #   self.assertEqual(run_backtest.monthly_ic.at[1, "ic"], 1.5)

  # def test_calc_ic_r(self):
  #   """
  #   Tests the calc_ic method for reversal.
  #   """
  #   run_backtest = self.init_run_backtest_calc_ic(REVERSAL)
  #   run_backtest.fill_up_portfolio_performance()
  #   run_backtest.calc_ic()
  #   self.assertEqual(run_backtest.monthly_ic.at[0, "ic"], 1)
  #   self.assertEqual(run_backtest.monthly_ic.at[1, "ic"], 1)


