# Assignment 3 - Alan, Vibilan, Jerri, Nahian

## Setting up virtual environment (recommended)

1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.

## Direction of use

1. To install packages, run `pip install -r requirements.txt`.

## Updating environment

1. If you install new packages, run `pip freeze > requirements.txt` afterwards to update the environment requirements.

## Usage

### Backtesting Strategy

To backtest a linear combination of 1) momentum strategy with 60 days, and 2) reversal strategy with 30 days, with an initial AUM of 10000, and on the top 10% of the stock universe containing AAPL, TSLA, LMT, BA, GOOG, AMZN, NVDA, META, WMT, MCD from January 1, 2022 to January 1, 2023, run the following: 

* `python backtest_two_signal_strategy.py --tickers AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD --b 20220101 --e 20230101 --initial_aum 10000 --strategy1_type M --days1 60 --strategy2_type R --days2 30 --top_pct 10`

To backtest a linear combination of 1) reversal strategy with 10 days, and 2) momentum strategy with 40 days, with an initial AUM of 10000, and on the top 20% of the stock universe containing AAPL, TSLA, LMT, BA, GOOG, AMZN, NVDA, META, WMT, MCD from June 1, 2022 to today run the following: 

* `python backtest_strategy.py --tickers AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD --b 20220601 --initial_aum 10000 --strategy1_type R --days1 10 --strategy2_type M --days2 40 --top_pct 20`

### Note

The plot filenames can be specified but default to `daily_aum.png` and `cumulative_ic.png`.

### Unit Tests

Run the unit tests using the following command:

* `pytest -vv`

To see the code coverage report, run the following command:

1. `coverage run -m pytest`
2. `coverage report`

### Project Accomplishments

1. Produces the correct analytics and plot
2. Code coverage of the project is 99%
3. Functions have been tested for multiple scenarios
4. Functions have been correctly typed

Screenshot of pytest results of the project:

TODO

Screenshot of code coverage report of the project:

TODO

python -i backtest_two_signal_strategy.py --tickers NFLX,SPY,AMZN,WMT --b 20230101 --e 20230410 --initial_aum 10000 --strategy1_type M --days1 50 --strategy2_type R --days2 5 --top_pct 50 