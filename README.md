# Dynamic ML Models for FX Portfolio Risk Management

Capstone project for the M.S. in Analytics at the University of Chicago. The goal of this repository is to test and implement the use of different machine learning methods applied to a number of currency pairs for which we have daily data. We plan to create a suite of strategies that, in conjunction with one another, can build a portfolio that will hopefully exceed benchmarks in risk/return parameters. Every strategy will be backtested using multiple methods including random time series and portfolios. The success of this portfolio will be measured by risk adjusted returns.

## Usage
```python
import capstone_proj as cp
```

### Data Extraction for Time Series Tests
Data extraction methods provide a dataframe with currency data for specified dates. 
```python
batch = cp.Batch(start=str,[end=str],[days=int],[months=int],[years=int],\
                [currencies=str/list],[filepath=str])
randombatch = cp.Random_batch(start=str,[spec_days=int],[min_days=int],[max_days=int],\
                [currencies=str/list],[spec_curr=int],[min_currencies=int],\
                [max_currencies=int],[seed=int],[filepath=str])

# Output Attributes:
.px_data, .px_change, .pct_change, .log_ret, .currencies, .num_rows, .num_cols

# Methods
.stats()
```
- Batch provides data for specific dates/currencies. Specific start/end dates and currencies can be declared. Otherwise days/months/years can be used after a start date.

- Random_batch provides random date/currency data within certain parameters. Specific dates/currencies can be specified. Otherwise use min/max days or currencies to get data from a random number of days or currencies within those intervals.

### Technical Indicators
Indicators provide valuable information on a batch of currency data. 
```python
atr = cp.ATR(batch,[show_hl=False])
bollinger_bands = cp.Bollinger(batch,[period=20],[std_number=2],[show_hl=False])
fibonacci_retracement = cp.Fibonacci(batch,[show_hl=False])
momentum = cp.Momentum(batch,[period=12],[show_hl=False])
moving_average = cp.MA(batch,[period=20],[ma_type='simple'],[show_hl=False])
converge_divergence = cp.MACD(batch,[show_hl=False])
relative_strength = cp.RSI(batch,[period=14],[show_hl=False])
relative_momentum = cp.RMI(batch,[period=14],[momentum_period=4],[show_hl=False])
stochastic_oscillator = cp.StochasticO(batch,[k_periods=14], [k_slowing_periods=1],\
                        [d_periods=3],[d_method='simple'],[show_hl=False])
rolling_st_dev = cp.RollingStDev(batch,[period=20],[show_hl=False])
up_down = cp.Up_Down(px_or_ret,[show_hl=False],[data_type='price'])
lagged_data = cp.Lagged_Data(px_or_ret,[lag=None],[lag_until=None])

# For px_or_ret you must pass specific price or return data: .px_data, .pct_change, .log_ret
# Show_hl = True includes the cumulative min/max price for the period
# Moving average type can be simple, exponential, time_series, triangular or variable
# data_type can be either 'price' or 'return' where needed
```
- Indicators take a data batch (dataframe) and output a dictionary according to currency. 
- The value associated with each currency key will be a dataframe with the currency raw data plus the indicator
- A batch with one or multiple currencies can be passed as input

