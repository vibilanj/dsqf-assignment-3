"""
This module is responsible for testing the functions that validate
and organise user input.
"""
import sys
import unittest
# from src.input_data import InputData, get_args, DATE_TODAY
from input_data import InputData, get_args

sys.path.append("/.../src")

class TestInputData(unittest.TestCase):
  """
  Defines the TestInputData class which tests the InputData class.
  """
  def test_get_normal_args(self) -> None:
    """
    Tests the get_args method with normal input.
    """
    parser = get_args()
    args = parser.parse_args(["--tickers",
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD", "--b", "20220101",
      "--e", "20230318", "--initial_aum", "10000", "--strategy1_type", "M", 
      "--strategy2_type", "R", "--days1", "100", "--days2", "150",
      "--top_pct", "20"])
    self.assertEqual(args.tickers,
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD")
    self.assertEqual(args.b, 20220101)
    self.assertEqual(args.e, 20230318)
    self.assertEqual(args.initial_aum, 10000)
    self.assertEqual(args.strategy1_type, "M")
    self.assertEqual(args.strategy2_type, "R")
    self.assertEqual(args.days1, 100)
    self.assertEqual(args.days2, 150)
    self.assertEqual(args.top_pct, 20)

  def test_missing_args(self) -> None:
    """
    Tests the get_args method with missing input.
    """
    parser = get_args()
    self.assertRaises(SystemExit, parser.parse_args, [])

  def test_wrong_args(self) -> None:
    """
    Tests the get_args method with wrong input.
    """
    parser = get_args()
    self.assertRaises(SystemExit, parser.parse_args, ["--tickers",
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,HAHAHHAAH,WMT,MCD", "--b", "jjj222",
      "--e", "82j23i2", "--initial_aum", "alsms12", "--strategy1_type", "M",
      "--strategy2_type", "R", "--days1", "100", "--days2", "150", 
      "--top_pct", "l12i2s", "--wrong-stuff"])

  def setUp(self) -> None:
    """
    This method initialises the TestInputData class.
    """
    self.tickers = "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD"
    self.b = 20220101
    self.e = 20230318
    self.initial_aum = 10000
    self.strategy1_type = "M"
    self.strategy2_type = "R"
    self.days1 = 100
    self.days2 = 150
    self.top_pct = 20
    self.input_data = InputData(
      tickers=self.tickers,
      b=self.b,
      e=self.e,
      initial_aum=self.initial_aum,
      strategy1_type=self.strategy1_type,
      strategy2_type=self.strategy2_type,
      days1=self.days1,
      days2=self.days2,
      top_pct=self.top_pct)

  def test_get_tickers_valid(self) -> None:
    """
    This method tests the get_tickers method.
    """
    self.assertEqual(self.input_data.get_tickers(),
      ["AAPL", "TSLA", "LMT", "BA", "GOOG", "AMZN",
      "NVDA", "META", "WMT", "MCD"])

  def test_get_beginning_date_valid(self) -> None:
    """
    This method tests the get_beginning_date method.
    """
    self.assertEqual(self.input_data.get_beginning_date(), "20220101")

  def test_get_end_date_valid(self) -> None:
    """
    This method tests the get_end_date method.
    """
    self.assertEqual(self.input_data.get_ending_date(), "20230318")

  def test_get_initial_aum_valid(self) -> None:
    """
    This method tests the get_initial_aum method.
    """
    self.assertEqual(self.input_data.get_initial_aum(), 10000)

  def test_get_strategy_and_days_valid(self) -> None:
    """
    This method tests the get_strategy_and_days method.
    """
    self.assertEqual(self.input_data.get_strategy_and_days(1), ("M", 100))
    self.assertEqual(self.input_data.get_strategy_and_days(2), ("R", 150))

  def test_get_top_pct_valid(self) -> None:
    """
    This method tests the get_top_pct method.
    """
    self.assertEqual(self.input_data.get_top_pct(), 20)

  def set_wrong_data(self) -> None:
    """
    This method sets the wrong data for the TestInputData class.
    """
    self.wrong_tickers = "AAPL,AMZN,%`$"
    self.wrong_b = "20220301"
    self.wrong_e = "20220228"
    self.wrong_initial_aum = -1000
    self.wrong_strategy1_type = "K"
    self.wrong_strategy2_type = "R"
    self.wrong_days1 = "200"
    self.wrong_days2 = 0
    self.wrong_top_pct = 200
    self.input_data = InputData(
      tickers=self.wrong_tickers,
      b=self.wrong_b,
      e=self.wrong_e,
      initial_aum=self.wrong_initial_aum,
      strategy1_type=self.wrong_strategy1_type,
      strategy2_type=self.wrong_strategy2_type,
      days1=self.wrong_days1,
      days2=self.wrong_days2,
      top_pct=self.wrong_top_pct
    )

  def test_get_tickers_invalid(self) -> None:
    """
    This method tests the get_tickers method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_tickers)

  def test_get_beginning_date_invalid(self) -> None:
    """
    This method tests the get_beginning_date method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_beginning_date)

  def test_get_ending_date_invalid(self) -> None:
    """
    This method tests the get_end_date method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_ending_date)

  def test_get_initial_aum_invalid(self) -> None:
    """
    This method tests the get_initial_aum method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_initial_aum)

  def test_get_strategy_and_days_invalid(self) -> None:
    """
    This method tests the get_strategy_and_days method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_strategy_and_days, 1)
    self.assertRaises(ValueError, self.input_data.get_strategy_and_days, 2)

  def test_get_top_pct_invalid(self) -> None:
    """
    This method tests the get_top_pct method with wrong input.
    """
    self.set_wrong_data()
    self.assertRaises(ValueError, self.input_data.get_top_pct)
