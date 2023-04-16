"""
This module is responsible for testing the functions that calculate
backtest statistics.
"""
import os.path
import sys
import unittest
from datetime import date

import pandas as pd
import pytest
from dateutil.parser import parse

from src.backtest_stats import BacktestStats

sys.path.append("/.../src")

class TestBacktestStats(unittest.TestCase):
  """
  Defines the TestBacktestStats class which tests the BacktestStats class.
  """
  def init_backtest_stats(self):
    """
    Tests the BacktestStats class instantiation.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    portfolio_performance = pd.read_csv(
      os.path.join(current_dir, "data", "backtest_stats",
                   "portfolio_performance.csv"),
      dtype={"aum": "float64",
             "dividends": "float64"},
      parse_dates=["datetime"],
      date_parser=lambda x: pd.to_datetime(parse(x)))

    monthly_ic = pd.read_csv(os.path.join(
      current_dir, "data", "backtest_stats", "monthly_ic.csv"),
      dtype={"ic": "int64"},
      parse_dates=["datetime"],
      date_parser=lambda x: pd.to_datetime(parse(x)))

    model_statistics_record = pd.read_csv(
      os.path.join(current_dir, "data", "backtest_stats",
                   "model_statistics_record.csv"),
      dtype={"strategy1_coeff": "float64",
             "strategy2_coeff": "float64",
             "strategy1_t": "float64",
             "strategy2_t": "float64"})

    return BacktestStats(
      portfolio_performance,
      monthly_ic,
      model_statistics_record)

  def test_get_beginning_trading_date_str(self):
    """
    Tests the get_beginning_trading_date_str function.
    """
    backtest_stats = self.init_backtest_stats()
    self.assertEqual(backtest_stats.get_beginning_trading_date_str(),
      "03/01/2023")

  def test_get_ending_trading_date_str(self):
    """
    Tests the get_ending_trading_date_str function.
    """
    backtest_stats = self.init_backtest_stats()
    self.assertEqual(backtest_stats.get_ending_trading_date_str(), "10/04/2023")

  def test_get_number_of_days(self):
    """
    Tests the get_number_of_days function.
    """
    backtest_stats = self.init_backtest_stats()
    beginning_trading_date = date(2023, 1, 3)
    ending_trading_date = date(2023, 4, 10)
    diff = ending_trading_date - beginning_trading_date

    number_of_days = backtest_stats.get_number_of_days()
    self.assertIsInstance(number_of_days, int)
    self.assertEqual(number_of_days, diff.days)

  def test_get_initial_aum(self):
    """
    Tests the get_initial_aum function.
    """
    backtest_stats = self.init_backtest_stats()
    initial_aum = backtest_stats.get_initial_aum()
    self.assertIsInstance(initial_aum, float)
    self.assertAlmostEqual(initial_aum, 10000.0)

  def test_get_final_aum(self):
    """
    Tests the get_final_aum function.
    """
    backtest_stats = self.init_backtest_stats()
    final_aum = backtest_stats.get_final_aum()
    self.assertIsInstance(final_aum, float)
    self.assertAlmostEqual(final_aum, 10088.085424940917)

  def test_get_profit_loss(self):
    """
    Tests the get_profit_loss function.
    """
    backtest_stats = self.init_backtest_stats()
    profit_loss = backtest_stats.get_profit_loss()
    self.assertIsInstance(profit_loss, float)
    self.assertAlmostEqual(profit_loss, 107.09777892942658)

  def test_get_total_stock_return(self):
    """
    Tests the get_total_stock_return function.
    """
    backtest_stats = self.init_backtest_stats()
    total_stock_return = backtest_stats.get_total_stock_return()
    self.assertIsInstance(total_stock_return, float)
    self.assertAlmostEqual(total_stock_return, 0.008808542494091671)

  def test_get_total_return(self):
    """
    Tests the get_total_return function.
    """
    backtest_stats = self.init_backtest_stats()
    total_return = backtest_stats.get_total_return()
    self.assertIsInstance(total_return, float)
    self.assertAlmostEqual(total_return, 0.010709777892942658)

  def test_get_annualized_rate_of_return(self):
    """
    Tests the get_annualized_rate_of_return function.
    """
    backtest_stats = self.init_backtest_stats()
    annualized_rate_of_return = backtest_stats.get_annualized_rate_of_return()
    self.assertIsInstance(annualized_rate_of_return, float)
    self.assertAlmostEqual(annualized_rate_of_return, 0.04089967145335871)

  def test_get_average_daily_aum(self):
    """
    Tests the get_average_daily_aum function.
    """
    backtest_stats = self.init_backtest_stats()
    average_daily_aum = backtest_stats.get_average_daily_aum()
    self.assertIsInstance(average_daily_aum, float)
    self.assertAlmostEqual(average_daily_aum, 9698.81619722861)

  def test_get_maximum_daily_aum(self):
    """
    Tests the get_maximum_daily_aum function.
    """
    backtest_stats = self.init_backtest_stats()
    maximum_daily_aum = backtest_stats.get_maximum_daily_aum()
    self.assertIsInstance(maximum_daily_aum, float)
    self.assertAlmostEqual(maximum_daily_aum, 10600.856580331776)

  def test_get_daily_returns(self):
    """
    Tests the get_daily_returns function.
    """
    backtest_stats = self.init_backtest_stats()
    daily_returns = backtest_stats.get_daily_returns()
    self.assertIsInstance(daily_returns, list)
    daily_returns = [-0.008731629564034208, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.01510737901850589, 0.06008565803317761,
                     -0.006527674736961923, -0.057137603026440636,
                     -0.0026895482902068607, -0.009322606625240119,
                     -0.028561578543029695, -0.01518912140505129,
                     0.013677348979776722, 0.016193471082655845,
                     0.009358591053235634, -0.012995547849090579,
                     -0.02747414235911976, -0.02925416790979879,
                     -0.01806428180463718, 0.008365861385941255,
                     -0.014413140393723997, -0.014196244597490007,
                     0.0036047215834901997, -0.01990346054427741,
                     -0.02164393181236096, 0.00456099645336216,
                     0.0007772559050832411, -0.015659812561862524,
                     -0.009542354247888804, -0.02468339223990598,
                     -0.03455758578097156, -0.006270556167904786,
                     0.007859973650233044, 0.025501870749006717,
                     0.02765496514856809, 0.0007431420388665299,
                     0.0016525412089877154, 0.007428693078031061,
                     -0.02296410363144749, 0.024151956075216946,
                     0.06489696823790307, 0.02389031953615926,
                     -0.0011533750051817297, 0.006872305968541893,
                     0.0301351027584137, 0.03146927698999326,
                     0.022781317439025197, -0.00162537830500341,
                     -0.0007636484991237318, 0.012761643954490597,
                     0.005275078920595299]
    for exp, act in zip(backtest_stats.get_daily_returns(), daily_returns):
      self.assertAlmostEqual(exp, act)

  def test_get_average_daily_return(self):
    """
    Tests the get_average_daily_return function.
    """
    backtest_stats = self.init_backtest_stats()
    average_daily_return = backtest_stats.get_average_daily_return()
    self.assertIsInstance(average_daily_return, float)
    self.assertAlmostEqual(average_daily_return, 0.00032547808103799275)

  def test_get_daily_standard_deviation(self):
    """
    Tests the get_daily_standard_deviation function.
    """
    backtest_stats = self.init_backtest_stats()
    daily_standard_deviation = backtest_stats.get_daily_standard_deviation()
    self.assertIsInstance(daily_standard_deviation, float)
    self.assertAlmostEqual(daily_standard_deviation, 0.01932344778537147)

  def test_get_daily_sharpe_ratio(self):
    """
    Tests the get_daily_sharpe_ratio function.
    """
    backtest_stats = self.init_backtest_stats()
    daily_sharpe_ratio = backtest_stats.get_daily_sharpe_ratio()
    self.assertIsInstance(daily_sharpe_ratio, float)
    self.assertAlmostEqual(daily_sharpe_ratio, 0.011668625782645662)

  def test_get_strategy1_coefficient(self):
    """
    Tests the get_strategy1_coefficient function.
    """
    backtest_stats = self.init_backtest_stats()
    strategy1_coefficient = backtest_stats.get_strategy1_coefficient()
    self.assertIsInstance(strategy1_coefficient, float)
    self.assertAlmostEqual(strategy1_coefficient, 0.05126014084539502)

  def test_get_strategy2_coefficient(self):
    """
    Tests the get_strategy2_coefficient function.
    """
    backtest_stats = self.init_backtest_stats()
    strategy2_coefficient = backtest_stats.get_strategy2_coefficient()
    self.assertIsInstance(strategy2_coefficient, float)
    self.assertAlmostEqual(strategy2_coefficient, -0.7767555498641575)

  def test_get_strategy1_t_value(self):
    """
    Tests the get_strategy1_t_value function.
    """
    backtest_stats = self.init_backtest_stats()
    strategy1_t_value = backtest_stats.get_strategy1_t_value()
    self.assertIsInstance(strategy1_t_value, float)
    self.assertAlmostEqual(strategy1_t_value, 0.20960935880946327)

  def test_get_strategy2_t_value(self):
    """
    Tests the get_strategy2_t_value function.
    """
    backtest_stats = self.init_backtest_stats()
    strategy2_t_value = backtest_stats.get_strategy2_t_value()
    self.assertIsInstance(strategy2_t_value, float)
    self.assertAlmostEqual(strategy2_t_value, -0.597435995779343)

  # Allows us to capture printing to standard output
  @pytest.fixture(autouse=True)
  def capsys(self, capsys):
    self.capsys = capsys

  def test_print_summary(self):
    """
    Tests the print_summary method.
    """
    out_str = """
    Begin Date: 03/01/2023
    End Date: 10/04/2023
    Number of Days: 97
    Total Stock Return: 0.881%
    Total Return: 1.071%
    Annualized Rate of Return: 4.090%
    Initial AUM: 10000.00000
    Final AUM: 10088.08542
    Average Daily AUM: 9698.81620
    Maximum Daily AUM: 10600.85658
    Profit and Loss: 107.09778
    Average Daily Return: 0.03255%
    Daily Standard Deviation: 1.93234%
    Daily Sharpe Ratio: 0.01167
    Strategy 1 Coefficient: 0.05126
    Strategy 2 Coefficient: -0.77676
    Strategy 1 T-Value: 0.20961
    Strategy 2 T-Value: -0.59744
    
"""
    bts = self.init_backtest_stats()
    bts.print_summary()
    captured = self.capsys.readouterr()
    assert len(captured.out) == len(out_str)

  def test_plot_daily_aum(self):
    """
    Tests the plot_daily_aum method.
    """
    bts = self.init_backtest_stats()
    bts.plot_daily_aum()
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    expected_path = os.path.join(parent_dir, "daily_aum.png")
    self.assertTrue(os.path.isfile(expected_path))

  def test_plot_monthly_cumulative_ic(self):
    """
    Tests the plot_monthly_cumulative_ic method.
    """
    bts = self.init_backtest_stats()
    bts.plot_monthly_cumulative_ic()
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    expected_path = os.path.join(parent_dir, "cumulative_ic.png")
    self.assertTrue(os.path.isfile(expected_path))
