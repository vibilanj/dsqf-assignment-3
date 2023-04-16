"""
This module is responsible for running the backtest simulation.
"""
import pandas as pd
from math import ceil
from typing import Dict, List, Tuple
from sklearn.linear_model import LinearRegression
import numpy as np

# Constants
MOMENTUM = "M"
REVERSAL = "R"
MOMENTUM_GAP = 20
DATE_FORMAT = "%Y%m%d"
AUM = "aum"
IC = "ic"
DATETIME = "datetime"
DIVIDENDS_DF = "dividends"

# Yahoo Finance Constants
CLOSE_PRICE = "Close"
DIVIDENDS = "Dividends"

# Model Constants
STOCK = "stock"
STRATEGY1_RETURN = "strategy1_return"
STRATEGY2_RETURN = "strategy2_return"
ACTUAL_RETURN = "actual_return"
PREDICTED_RETURN = "predicted_return"

# Model Statistics Constants
STRATEGY1_COEFF = "strategy1_coeff"
STRATEGY2_COEFF = "strategy2_coeff"
STRATEGY1_T = "strategy1_t"
STRATEGY2_T = "strategy2_t"

class RunBacktest:
  """
  Defines the RunBacktest class which runs the backtest based on 
  the stock data obtained by the fetcher and the user defined
  inputs.
  """
  def __init__(self,
    stocks_data: Dict[str, pd.DataFrame],
    initial_aum: int,
    beginning_date: int,
    strategy1: str,
    strategy2: str,
    days1: int,
    days2: int,
    top_pct: int):
    """
    This method initialises the RunBacktest class.

    Args:
      stocks_data (Dict[str, pd.DataFrame]): The dictionary that matches 
        the stock ticker to the price information of the stock.
      initial_aum (int): The initial asset under management amount.
      beginning_date (str): The beginning date of the backtest period.
      days (int): The number of days to look back during calculation
        of stock returns.
      strategy (str): The backtesting strategy, either Momentum or Reversal.
      top_pct (int): The percentage of stocks to pick for the portfolio.
      TODO
    """
    self.stocks_data: Dict[str, pd.DataFrame] = stocks_data
    self.initial_aum: int = initial_aum
    self.beginning_date: str = beginning_date
    self.strategy1: str = strategy1
    self.strategy2: str = strategy2
    self.days1: int = days1
    self.days2: int = days2
    self.top_pct: int = top_pct

    """
    portfolio_performance (pd.DataFrame): The dataframe to store the 
      portfolio performance information such as AUM and dividends.
    portfolio (List[Tuple[str, float]]): The list containing the 
      current portfolio. Each element is a tuple of the stock ticker
      and the amount of the stock.
    portfolio_record (List[List[Tuple[str, float]]]): The list containing 
      a record of previous portfolios. Each element is a portfolio.
    monthly_ic (pd.DataFrame): The dataframe to store the monthly 
      cumulative information coefficient of the portfolio.
    TODO
    """
    self.portfolio_performance: pd.DataFrame = self.init_portfolio_performance()
    self.portfolio: List[Tuple[str, float]] = []
    self.portfolio_record: List[List[Tuple[str, float]]] = []
    self.monthly_ic: pd.DataFrame = pd.DataFrame()
    self.model_training_data: pd.DataFrame = \
      pd.DataFrame(columns=[STOCK,
                            STRATEGY1_RETURN,
                            STRATEGY2_RETURN,
                            ACTUAL_RETURN])
    self.model_statistics_record: pd.DataFrame = \
      pd.DataFrame(columns=[STRATEGY1_COEFF,
                            STRATEGY2_COEFF,
                            STRATEGY1_T,
                            STRATEGY2_T])
    self.month_end_indexes = self.get_month_end_indexes_from_b()

  def init_portfolio_performance(self) -> None:
    """
    None: Initialises the portfolio performance dataframe with 
      the datetime indexes in the specified period, the initial 
      AUM and empty dividends.
    """
    datetime_indexes = list(self.stocks_data.values())[0].index.to_list()
    portfolio_performance = pd.DataFrame()
    portfolio_performance[DATETIME] = datetime_indexes
    portfolio_performance[AUM] = \
      [self.initial_aum for _ in range(len(datetime_indexes))]
    portfolio_performance[DIVIDENDS_DF] = \
      [0 for _ in range(len(datetime_indexes))]
    return portfolio_performance

  def get_month_end_indexes_from_b(self) -> List[int]:
    """
    List[int]: Returns the indexes of the month end dates starting
      from one month before the beginning date.
    """
    datetime_indexes = list(self.stocks_data.values())[0].index.to_list()
    b_timestamp = pd.to_datetime(self.beginning_date, format=DATE_FORMAT)
    month_end_indexes = []
    first_index_after_b = None

    for idx, datetime in enumerate(datetime_indexes[:-1]):
      if datetime.month != datetime_indexes[idx + 1].month:
        month_end_indexes.append(idx)
        if first_index_after_b is None and\
          datetime_indexes[idx].tz_localize(None) > b_timestamp:
          first_index_after_b = idx

    first_index_after_b = month_end_indexes.index(first_index_after_b)
    return month_end_indexes[first_index_after_b - 1:]

  def get_feature(self,
    stock: str,
    strategy: str,
    days: int,
    date_index: int) -> float:
    """
    _summary_ TODO

    Args:
        ticker (str): _description_
        strategy (str): _description_
        days (int): _description_
        date_index (int): _description_

    Returns:
        float: _description_
    """
    is_momentum = strategy == MOMENTUM
    date_index -= MOMENTUM_GAP * is_momentum

    history = self.stocks_data[stock]
    end_close = history.iloc[date_index][CLOSE_PRICE]
    start_close = history.iloc[date_index - days][CLOSE_PRICE]
    return (end_close - start_close) / start_close * 100

  def get_label(self,
    stock: str,
    date_index: int) -> float:
    """
    _summary_ TODO

    Args:
        stock (str): _description_
        date_index (int): _description_

    Returns:
        float: _description_
    """
    previous_month_index = \
      self.month_end_indexes[self.month_end_indexes.index(date_index) - 1]

    history = self.stocks_data[stock]
    end_close = history.iloc[date_index][CLOSE_PRICE]
    start_close = history.iloc[previous_month_index][CLOSE_PRICE]
    return (end_close - start_close) / start_close * 100

  def update_monthly_training_data(self,
    date_index: int) -> None:
    """
    _summary_ TODO

    Args:
        date_index (int): _description_
    """
    previous_month_index = \
      self.month_end_indexes[self.month_end_indexes.index(date_index) - 1]

    training_data_block = []
    stock_list = list(self.stocks_data.keys())
    for stock in stock_list:
      strategy1_return = self.get_feature(
        stock,
        self.strategy1,
        self.days1,
        previous_month_index)
      strategy2_return = self.get_feature(
        stock,
        self.strategy2,
        self.days2,
        previous_month_index)
      actual_return = self.get_label(stock, date_index)
      training_data_block.append(\
        [stock, strategy1_return, strategy2_return, actual_return])

    training_data_df = pd.DataFrame(training_data_block,
                                    columns=[STOCK,
                                             STRATEGY1_RETURN,
                                             STRATEGY2_RETURN,
                                             ACTUAL_RETURN])
    self.model_training_data = \
      pd.concat([self.model_training_data, training_data_df],
                ignore_index=True)

  def store_model_statistics(self,
    x: pd.DataFrame,
    y: pd.Series,
    model: LinearRegression) -> None:
    """
    _summary_ TODO

    Args:
        model (LinearRegression): _description_
    """
    coefficients = model.coef_

    n_samples, n_predictors = x.shape
    residuals = y - model.predict(x)
    residual_std_error = np.sqrt(np.sum(residuals ** 2) / \
                                 (n_samples - n_predictors - 1))

    x_design = np.concatenate([np.ones((n_samples, 1)), x], axis=1)
    design_matrix_inv = np.linalg.inv(np.dot(x_design.T, x_design))
    standard_errors = np.sqrt(np.diagonal(design_matrix_inv))\
      * residual_std_error
    t_values = coefficients / standard_errors[1:]

    statistics = np.concatenate((coefficients, t_values))
    statistics_df = \
      pd.DataFrame(statistics.reshape(1, -1),
                   columns=[STRATEGY1_COEFF,
                            STRATEGY2_COEFF,
                            STRATEGY1_T,
                            STRATEGY2_T])
    self.model_statistics_record = \
      pd.concat([self.model_statistics_record, statistics_df], ignore_index=True)

  def fit_model_and_store_statistics(self) -> LinearRegression:
    """
    _summary_ TODO

    Returns:
        LinearRegression: _description_
    """
    x = self.model_training_data[[STRATEGY1_RETURN, STRATEGY2_RETURN]]
    y = self.model_training_data[ACTUAL_RETURN]

    model = LinearRegression()
    model.fit(x, y)
    self.store_model_statistics(x, y, model)
    return model

  def predict_returns(self,
    date_index: int) -> pd.DataFrame:
    """
    _summary_ TODO

    Args:
        date_index (int): _description_

    Returns:
        pd.DataFrame: _description_
    """
    prediction_features = []
    stock_list = list(self.stocks_data.keys())
    for stock in stock_list:
      strategy1_return = self.get_feature(
        stock,
        self.strategy1,
        self.days1,
        date_index)
      strategy2_return = self.get_feature(
        stock,
        self.strategy2,
        self.days2,
        date_index)
      prediction_features.append([stock, strategy1_return, strategy2_return])

    prediction_features_df = pd.DataFrame(prediction_features,
                                          columns=[STOCK,
                                                   STRATEGY1_RETURN,
                                                   STRATEGY2_RETURN])

    self.update_monthly_training_data(date_index)
    model = self.fit_model_and_store_statistics()
    x_new = prediction_features_df[[STRATEGY1_RETURN, STRATEGY2_RETURN]]
    y_pred = pd.Series(model.predict(x_new), name=PREDICTED_RETURN)
    predicted_returns = \
      pd.concat([prediction_features_df[STOCK], y_pred], axis=1)
    return predicted_returns

  def select_stocks_to_buy(self,
    date_index: int) -> List[str]:
    """
    _summary_ TODO

    Args:
        date_index (int): _description_
        top_pct (int): _description_

    Returns:
        List[str]: _description_
    """
    stocks = list(self.stocks_data.keys())
    n_stocks = ceil(len(stocks) * (self.top_pct / 100))
    predicted_returns = self.predict_returns(date_index)
    sorted_predicted_returns = \
      predicted_returns.sort_values(PREDICTED_RETURN, ascending=False)
    return list(sorted_predicted_returns[STOCK][:n_stocks])


  def calc_portfolio(self,
    stocks_to_buy: List[str],
    aum: int,
    date_index: int) -> List[Tuple[str, float]]:
    """
    Calculates the portfolio based on which stocks need to be bought
    and the AUM amount.

    Args:
      stocks_to_buy (List[str]): The list of stocks to be bought.
      aum (int): The assets under management amount.
      date_index (int): The index of the date at which the stocks are 
        bought.

    Returns:
      List[Tuple[str, float]]: The list containing the portfolio. 
      Each element is a tuple of the stock ticker and the amount of 
      the stock.
    """
    aum_per_stock = aum / len(stocks_to_buy)
    stocks_amount = []
    for stock in stocks_to_buy:
      history = self.stocks_data[stock]
      price = history.iloc[date_index][CLOSE_PRICE]
      amount = aum_per_stock / price
      stocks_amount.append((stock, amount))
    return stocks_amount

  def calc_aum(self, date_index: int) -> float:
    """
    Calculates the assets under management amount for a given date.

    Args:
      date_index (int): The index of the date at which AUM must be 
        calculated

    Returns:
      float: Returns the AUM amount.
    """
    total_aum = 0
    for stock, amount in self.portfolio:
      end_close = self.stocks_data[stock].iloc[date_index][CLOSE_PRICE]
      total_aum += amount * end_close
    return total_aum

  def calc_dividends(self, date_index: int) -> float:
    """
    Calculates the dividends amount for a given date.

    Args:
      date_index (int): The index of the date at which dividends 
        must be calculated

    Returns:
      float: Returns the dividends amount.
    """
    total_dividends = 0
    for stock, amount in self.portfolio:
      dividends = self.stocks_data[stock].iloc[date_index][DIVIDENDS]
      total_dividends += amount * dividends
    return total_dividends

  def fill_up_portfolio_performance(self) -> None:
    """
    None: TODO
    """
    month_end_idx = self.month_end_indexes[1:]
    for date_index in range(month_end_idx[0], \
                            len(list(self.stocks_data.values())[0].index)):
      # updating portfolio performance by each row
      if date_index == month_end_idx[0]:
        self.portfolio_performance.at[date_index, AUM] = self.initial_aum
      else:
        self.portfolio_performance.at[date_index, AUM] = \
          self.calc_aum(date_index)

      self.portfolio_performance.at[date_index, DIVIDENDS_DF] = \
        self.portfolio_performance.at[date_index - 1, DIVIDENDS_DF] \
          + self.calc_dividends(date_index)

      # rebalance and store new portfolio
      if date_index in month_end_idx:
        stocks_to_buy = self.select_stocks_to_buy(date_index)
        self.portfolio = self.calc_portfolio(
          stocks_to_buy,
          self.portfolio_performance.iloc[date_index][AUM],
          date_index)
        self.portfolio_record.append(self.portfolio)

    # cut portfolio performance to only start from beginning date
    datetime_indexes = self.portfolio_performance[DATETIME].to_list()
    b_idx = None
    for idx, datetime in enumerate(datetime_indexes):
      if datetime.tz_localize(None) >= \
        pd.to_datetime(self.beginning_date, format=DATE_FORMAT):
        b_idx = idx
        break
    self.portfolio_performance = \
      self.portfolio_performance[b_idx:].reset_index(drop=True)

  def calc_ic(self) -> None:
    """
    None: Simulates backtesting based on the user-defined information
      and strategy and fills up the dataframe of monthly cumulative 
      information coefficient for each month end day in the specified 
      period.
    """
    month_end_idx = self.month_end_indexes[1:]
    self.monthly_ic[DATETIME] = \
      list(self.stocks_data.values())[0].index[month_end_idx[:-1]]
    self.monthly_ic[IC] = [0 for _ in range(len(month_end_idx[:-1]))]

    number_stocks_bought = ceil(len(self.stocks_data) * (self.top_pct / 100))
    for i in range(len(month_end_idx[:-1])):
      number_correct = 0

      for stock, _ in self.portfolio_record[i]:
        current_close = \
          list(self.stocks_data[stock][CLOSE_PRICE])[month_end_idx[i]]
        next_close = \
          list(self.stocks_data[stock][CLOSE_PRICE])[month_end_idx[i + 1]]
        if next_close > current_close:
          number_correct += 1

      prop_correct = number_correct / number_stocks_bought
      information_coeff = (2 * prop_correct) - 1
      if i == 0:
        self.monthly_ic.at[i, IC] = information_coeff
      else:
        self.monthly_ic.at[i, IC] = self.monthly_ic.at[i - 1, IC] \
          + information_coeff
