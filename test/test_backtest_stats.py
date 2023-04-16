"""
This module is responsible for testing the functions that calculate
backtest statistics.
"""
import sys
import unittest
import pytest
import os.path
from datetime import date
from src.stocks_fetcher import StocksFetcher
from src.run_backtest import RunBacktest, MOMENTUM, REVERSAL
from src.backtest_stats import BacktestStats

sys.path.append("/.../src")

class TestBacktestStats(unittest.TestCase):
  """
  Defines the TestBacktestStats class which tests the BacktestStats class.
  """
  # StockFetcher parameters
  start_str = "20230101"
  end_str = "20230410"
  ticker_1 = "AMZN"
  ticker_2 = "NFLX"
  ticker_3 = "SPY"
  ticker_4 = "WMT"
  tickers_list = [ticker_1, ticker_2, ticker_3, ticker_4]
  ticker_obj = StocksFetcher()
  stocks_data = ticker_obj.fetch_stocks_data(tickers_list, start_str, end_str)

  # RunBacktest parameters
  initial_aum = 10000
  strategy1 = MOMENTUM
  strategy2 = REVERSAL
  days1 = 50
  days2 = 5
  top_pct = 50

  def init_backtest_stats(self):
    """
    Tests the BacktestStats class instantiation.
    """
    run_backtest = RunBacktest(
      self.stocks_data,
      self.initial_aum,
      self.start_str,
      self.strategy1,
      self.strategy2,
      self.days1,
      self.days2,
      self.top_pct)
    run_backtest.fill_up_portfolio_performance()
    run_backtest.calc_ic()

    return BacktestStats(
      run_backtest.portfolio_performance,
      run_backtest.monthly_ic,
      run_backtest.model_statistics_record)

  def test_get_beginning_trading_date_str(self):
    backtest_stats = self.init_backtest_stats()
    self.assertEqual(backtest_stats.get_beginning_trading_date_str(),
      "03/01/2023")

  def test_get_ending_trading_date_str(self):
    backtest_stats = self.init_backtest_stats()
    self.assertEqual(backtest_stats.get_ending_trading_date_str(), "10/04/2023")

  def test_get_number_of_days(self):
    backtest_stats = self.init_backtest_stats()
    beginning_trading_date = date(2023, 1, 1)
    ending_trading_date = date(2023, 4, 10)
    diff = ending_trading_date - beginning_trading_date
    self.assertEqual(backtest_stats.get_number_of_days(), diff)

  def test_get_initial_aum(self):
    backtest_stats = self.init_backtest_stats()
    self.assertAlmostEqual(backtest_stats.get_initial_aum(), self.initial_aum)

  def test_get_final_aum(self):
    backtest_stats = self.init_backtest_stats()
    final_aum = backtest_stats.get_final_aum()
    self.assertIsInstance(final_aum, float)
    self.assertAlmostEqual(final_aum, 10088.08542)

  def test_get_profit_loss(self):
    backtest_stats = self.init_backtest_stats()
    profit_loss = backtest_stats.get_profit_loss()
    self.assertIsInstance(profit_loss, float)
    self.assertAlmostEqual(profit_loss, 107.09778)

  def test_get_total_stock_return(self):
    backtest_stats = self.init_backtest_stats()
    total_stock_return = backtest_stats.get_total_stock_return()
    self.assertIsInstance(total_stock_return, float)
    self.assertAlmostEqual(total_stock_return, 0.00881)


  def test_get_total_return(self):
    backtest_stats = self.init_backtest_stats()
    total_return = backtest_stats.get_total_return()
    self.assertIsInstance(total_return, float)
    self.assertAlmostEqual(total_return, 0.01071)

  def test_get_annualized_rate_of_return(self):
    backtest_stats = self.init_backtest_stats()
    annualized_rate_of_return = backtest_stats.get_annualized_rate_of_return()
    self.assertIsInstance(annualized_rate_of_return, float)
    self.assertAlmostEqual(annualized_rate_of_return, 0.04133)

  def test_get_average_daily_aum(self):
    backtest_stats = self.init_backtest_stats()
    average_daily_aum = backtest_stats.get_average_daily_aum()
    self.assertIsInstance(average_daily_aum, float)
    self.assertAlmostEqual(average_daily_aum, 9698.81620)

  def test_get_maximum_daily_aum(self):
    backtest_stats = self.init_backtest_stats()
    maximum_daily_aum = backtest_stats.get_maximum_daily_aum()
    self.assertIsInstance(maximum_daily_aum, float)
    self.assertAlmostEqual(maximum_daily_aum, 10600.85658)

  def test_get_daily_returns(self):
    backtest_stats = self.init_backtest_stats()
    daily_returns = backtest_stats.get_daily_returns()
    self.assertIsInstance(daily_returns, list)
    self.assertIsInstance(daily_returns[0], float)

  def test_get_average_daily_return(self):
    backtest_stats = self.init_backtest_stats()
    average_daily_return = backtest_stats.get_average_daily_return()
    self.assertIsInstance(average_daily_return, float)
    self.assertAlmostEqual(average_daily_return, 9698.81620)

  def test_get_daily_standard_deviation(self):
    backtest_stats = self.init_backtest_stats()
    daily_standard_deviation = backtest_stats.get_daily_standard_deviation()
    self.assertIsInstance(daily_standard_deviation, float)
    self.assertAlmostEqual(daily_standard_deviation, 0.0193234)

  def test_get_daily_sharpe_ratio(self):
    backtest_stats = self.init_backtest_stats()
    daily_sharpe_ratio = backtest_stats.get_daily_sharpe_ratio()
    self.assertIsInstance(daily_sharpe_ratio, float)
    self.assertAlmostEqual(daily_sharpe_ratio, 0.01167)

  def test_get_strategy1_coefficient(self):
    backtest_stats = self.init_backtest_stats()
    strategy1_coefficient = backtest_stats.get_strategy1_coefficient()
    self.assertIsInstance(strategy1_coefficient, float)
    self.assertAlmostEqual(strategy1_coefficient, 0.05126)

  def test_get_strategy2_coefficient(self):
    backtest_stats = self.init_backtest_stats()
    strategy2_coefficient = backtest_stats.get_strategy2_coefficient()
    self.assertIsInstance(strategy2_coefficient, float)
    self.assertAlmostEqual(strategy2_coefficient, -0.77676)

  
 


#   def test_get_beginning_trading_date_str(self):
#     """
#     Tests the get_beginning_trading_date_str method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertEqual(bts.get_beginning_trading_date_str(),
#                      "17/12/2020")

#   def test_get_ending_trading_date_str(self):
#     """
#     Tests the get_ending_trading_date_str method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertEqual(bts.get_ending_trading_date_str(),
#                      "02/03/2021")

#   def test_get_number_days(self):
#     """
#     Tests the get_number_of_days method.
#     """
#     bts = self.init_backtest_stats()
#     beginning_trading_date = date(2020, 12, 17)
#     ending_trading_date = date(2021, 3, 2)
#     diff = ending_trading_date - beginning_trading_date
#     self.assertEqual(bts.get_number_of_days(), diff.days)

#   def test_get_initial_aum(self):
#     """
#     Tests the get_initial_aum method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertEqual(bts.get_initial_aum(), self.initial_aum)

#   def test_get_final_aum(self):
#     """
#     Tests the get_final_aum method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_final_aum(), 10305.45637, 2)

#   def test_get_profit_loss(self):
#     """
#     Tests the get_profit_loss method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_profit_loss(), 313.68406, 2)

#   def test_get_total_stock_return(self):
#     """
#     Tests the get_total_stock_return method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_total_stock_return(), 0.03055, 3)

#   def test_get_total_return(self):
#     """
#     Tests the get_total_return method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_total_return(), 0.03137, 3)

#   def test_get_annualized_rate_of_return(self):
#     """
#     Tests the get_annualized_rate_of_return method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_annualized_rate_of_return(), 0.16220, 3)

#   def test_get_average_daily_aum(self):
#     """
#     Tests the get_average_daily_aum method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_average_daily_aum(), 10306.71087, 2)

#   def test_get_maximum_daily_aum(self):
#     """
#     Tests the get_maximum_daily_aum method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_maximum_daily_aum(), 10902.82288, 2)

#   def test_get_daily_returns(self):
#     """
#     Tests the get_daily_returns method.
#     """
#     bts = self.init_backtest_stats()
#     dr = [-0.029640397582960193, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#           -0.019922489837307693, -0.009922241610900164, -0.011749927582867048,
#           0.009537970135655426, 0.04327931329369445, -0.01246580376766709,
#           -0.029172021587267154, 0.004678976684473441, -0.001470585128347106,
#           -0.019896438726364568, 0.011441158035954191, 0.06370494885844678,
#           0.06308392797820443, 0.02910548937188815, 0.02438827515572276,
#           0.018612059233934584, -0.022923957235919053, -0.03551727576720656,
#           -0.008493492599531775, 0.014505609856717916, 0.02629137486387206,
#           -0.0003674471774606418, 0.012521128160366908, 0.021801336006444957,
#           -0.004836327673704285, 0.004757795014086287, 0.008653537336325725,
#           -0.0045422098229200404, -0.006438489640713136, -0.007383824429011465,
#           -0.021281181164778423, -0.02110660948144507, -0.013925446006276805,
#           -0.027445571084428095, -0.009645725385907305, 0.016304394560859244,
#           -0.018135447824884576, -0.02295198250639831, 0.021619686633503114,
#           0.013733150610690529]
#     for exp, act in zip(bts.get_daily_returns(), dr):
#       self.assertAlmostEqual(exp, act, 3)

#   def test_get_average_daily_return(self):
#     """
#     Tests the get_average_daily_return method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_average_daily_return(), 0.0009956, 2)

#   def test_get_daily_standard_deviation(self):
#     """
#     Tests the get_daily_standard_deviation method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_daily_standard_deviation(), 0.0212649, 2)

#   def test_get_daily_sharpe_ratio(self):
#     """
#     Tests the get_daily_sharpe_ratio method.
#     """
#     bts = self.init_backtest_stats()
#     self.assertAlmostEqual(bts.get_daily_sharpe_ratio(), 0.04212, 2)

#   # Allows us to capture printing to standard output
#   @pytest.fixture(autouse=True)
#   def capsys(self, capsys):
#     self.capsys = capsys

#   def test_print_summary(self):
#     """Tests the print_summary method."""
#     out_str = """
#     Begin Date: 17/12/2020
#     End Date: 02/03/2021
#     Number of Days: 75
#     Total Stock Return: 3.055%
#     Total Return: 3.137%
#     Annualized Rate of Return: 16.220%
#     Initial AUM: 10000.00000
#     Final AUM: 10305.45721
#     Average Daily AUM: 10306.71195
#     Maximum Daily AUM: 10902.82411
#     Profit and Loss: 313.68634
#     Average Daily Return: 0.09956%
#     Daily Standard Deviation: 2.12649%
#     Daily Sharpe Ratio: 0.04212
    
# """
#     bts = self.init_backtest_stats()
#     bts.print_summary()
#     captured = self.capsys.readouterr()
#     assert len(captured.out) == len(out_str)

#   def test_plot_daily_aum(self):
#     """
#     Tests the plot_daily_aum method.
#     """
#     bts = self.init_backtest_stats()
#     bts.plot_daily_aum()
#     parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#     expected_path = os.path.join(parent_dir, "daily_aum.png")
#     self.assertTrue(os.path.isfile(expected_path))

#   def test_plot_monthly_cumulative_ic(self):
#     """
#     Tests the plot_monthly_cumulative_ic method.
#     """
#     bts = self.init_backtest_stats()
#     bts.plot_monthly_cumulative_ic()
#     parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#     expected_path = os.path.join(parent_dir, "cumulative_ic.png")
#     self.assertTrue(os.path.isfile(expected_path))
