"""
This module is responsible for testing the functions that validate
and organise user input.
"""
import sys
import unittest
from src.input_data import InputData, get_args, DATE_TODAY

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

  def test_get_args_optional_end_date(self) -> None:
    """
    Tests the get_args method when the optional end date is not provided.
    """
    parser = get_args()
    args = parser.parse_args(["--tickers", "AAPL,TSLA", "--b", "20220101",
      "--initial_aum", "10000", 
      "--strategy1_type", "M", "--strategy2_type", "R",
      "--days1", "100", "--days2", "150",
      "--top_pct", "20"])
    self.assertIsNone(args.e)


  def setUp(self):
    self.default_args = {
      "tickers": "MSFT,AMZN,WMT",
      "b": 20220101,
      "e": 20221231,
      "initial_aum": 10000,
      "strategy1_type": "M",
      "strategy2_type": "R",
      "days1": 10,
      "days2": 20,
      "top_pct": 10,
    }

  def test_get_tickers_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_tickers(), ["MSFT", "AMZN", "WMT"])

  def test_get_tickers_invalid(self):
    for invalid_tickers in ["", "MSFT,AMZN,WMT,!", "MSFT,AMZN,,WMT", None, 12,
      "HAAAAAAAAH"]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args,
          "tickers": invalid_tickers})
        input_data.get_tickers()

  def test_get_beginning_date_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_beginning_date(), "20220101")

  def test_get_beginning_date_invalid(self):
    for invalid_b in [202201, "20220101", 20982109382180382091, None]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args, "b": invalid_b})
        input_data.get_beginning_date()

  def test_get_ending_date_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_ending_date(), "20221231")

  def test_get_ending_date_none(self):
    input_data = InputData(**{**self.default_args, "e": None})
    self.assertEqual(input_data.get_ending_date(), DATE_TODAY)

  def test_get_ending_date_invalid(self):
    for invalid_e in [20211231, "20211231", 20231231, "dabdad"]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args, "e": invalid_e})
        input_data.get_ending_date()

  def test_get_initial_aum_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_initial_aum(), 10000)

  def test_get_initial_aum_invalid(self):
    for invalid_aum in ["10000", -10000, None]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args,
          "initial_aum": invalid_aum})
        input_data.get_initial_aum()

  def test_get_top_pct_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_top_pct(), 10)

  def test_get_top_pct_invalid(self):
    for invalid_pct in [0, 101, None, "10", "dabdad"]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args, "top_pct": invalid_pct})
        input_data.get_top_pct()

  def test_get_strategy1_type_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_strategy1_type(), "M")

  def test_get_strategy1_type_invalid(self):
    for invalid_type in [None, "dabdad", 1]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args,
          "strategy1_type": invalid_type})
        input_data.get_strategy1_type()

  def test_get_strategy2_type_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_strategy2_type(), "R")

  def test_get_strategy2_type_invalid(self):
    for invalid_type in [None, "dabdad", 1]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args,
          "strategy2_type": invalid_type})
        input_data.get_strategy2_type()

  def test_get_days1_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_days1(), 10)

  def test_get_days1_invalid(self):
    for invalid_days in [0, 366, None, "10", "dabdad"]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args, "days1": invalid_days})
        input_data.get_days1()

  def test_get_days2_valid(self):
    input_data = InputData(**self.default_args)
    self.assertEqual(input_data.get_days2(), 20)

  def test_get_days2_invalid(self):
    for invalid_days in [0, 366, None, "10", "dabdad"]:
      with self.assertRaises(ValueError):
        input_data = InputData(**{**self.default_args, "days2": invalid_days})
        input_data.get_days2()

