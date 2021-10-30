# Dynamic ML Models for FX Portfolio Risk Management

Capstone project for the M.S. in Analytics at the University of Chicago. The goal of this repository is to test and implement the use of different machine learning methods applied to a number of currency pairs for which we have daily data. We plan to create a suite of strategies that, in conjunction with one another, can build a portfolio that will hopefully exceed benchmarks in risk/return parameters. Every strategy will be backtested using multiple methods including random time series and portfolios. The success of this portfolio will be measured by risk adjusted returns.

## Usage
```python
import capstone_proj as cp
```

### Data Extraction for Time Series Tests
```python
batch = Batch(start=,[end=],[days=],[months=],[years=],[currencies=],[filepath=])
randombatch = Random_batch(start='1999-01-01',min_days=10,max_days=30,max_currencies=3,min_currencies=1)
```
Data extraction methods provide a dataframe with currency data for specified dates. 
- A user can specify a start/end date, or just a start date and an arbitrary number of days/months/years for which data is requested.
- Specific currencies can be specified, otherwise all currencies are returned. 
- Data filepath is optional

