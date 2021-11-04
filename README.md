# Dynamic ML Models for FX Portfolio Risk Management

Capstone project for the M.S. in Analytics at the University of Chicago. The goal of this repository is to test and implement the use of different machine learning methods applied to a number of currency pairs for which we have daily data. We plan to create a suite of strategies that, in conjunction with one another, can build a portfolio that will hopefully exceed benchmarks in risk/return parameters. Every strategy will be backtested using multiple methods including random time series and portfolios. The success of this portfolio will be measured by risk adjusted returns.

## Usage
```python
import capstone_proj as cp
```
### Dependencies
numpy, pandas, tti, pyfolio

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
- **Batch** provides data for specific dates/currencies. Specific start/end dates and currencies can be declared. Otherwise days/months/years can be used after a start date.

- **Random_batch** provides random date/currency data within certain parameters. Specific dates/currencies can be specified. Otherwise use min/max days or currencies to get data from a random number of days or currencies within those intervals.

### Technical Indicators
Indicators provide valuable information on a batch of currency data. 
Input: Dataframe, Dictionary or Batch/Random_batch object
Output: Dataframe/Dictionary of raw data plus indicator
```python
atr = cp.ATR(currency_data,[show_hl=False])
bollinger_bands = cp.Bollinger(batch,[period=20],[std_number=2],[show_hl=False])
fibonacci_retracement = cp.Fibonacci(currency_data,[show_hl=False])
momentum = cp.Momentum(currency_data,[period=12],[show_hl=False])
moving_average = cp.MA(currency_data,[period=20],[ma_type='simple'],[show_hl=False])
converge_divergence = cp.MACD(currency_data,[show_hl=False])
relative_strength = cp.RSI(currency_data,[period=14],[show_hl=False])
relative_momentum = cp.RMI(currency_data,[period=14],[momentum_period=4],[show_hl=False])
stochastic_oscillator = cp.StochasticO(currency_data,[k_periods=14], [k_slowing_periods=1],\
                        [d_periods=3],[d_method='simple'],[show_hl=False])
rolling_st_dev = cp.RollingStDev(currency_data,[period=20],[show_hl=False])

up_down = cp.Up_Down(px_or_ret,[data_type='price'],[show_hl=False])
lagged_data = cp.Lagged_Data(px_or_ret,[lag=int],[lag_until=int],[col_to_lag=str],[show_hl=False])

# Show_hl = True includes columns with the cumulative min/max price for the period
# Moving average type can be simple, exponential, time_series, triangular or variable
# data_type can be either 'price' or 'return' where needed
```
- A batch with one or multiple currencies can be passed as input
- For px_or_ret you must pass specific price or return data: .px_data, .pct_change, .log_ret. Otherwise if passed a Batch, the default will be price data
- Indicators passed only one currency will output a dataframe, with multiple currencies output will be a dictionary
- The value associated with each currency key will be a dataframe with the currency raw data plus the indicator
- Multiple indicators can be called one after the other 


