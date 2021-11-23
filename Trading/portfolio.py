import numpy as np
import pandas as pd
from extraction import Batch, Random_batch

class Portfolio():

    def __init__(self,prices,cash=1000000,positions=None,benchmark=None):

        self.cash = cash
        self.max_portfolio = cash
        self.num_orders = 0
        self.pending_orders = {'target_orders':[], 'stop_losses':[]}

        if (isinstance(prices, pd.DataFrame)) or (isinstance(prices, Batch)):
            if isinstance(prices, Batch):
                self.prices = prices.px_data
                self.positions = prices.px_data.copy()
            else:
                self.prices = prices
                self.positions = prices.copy()

            if not isinstance(self.positions.index,pd.DatetimeIndex):
                raise ValueError('Include dates in the dataframe as a datetime index')

            for col in self.positions.columns:
                self.positions[col].values[:] = 0

            self.prices['cash'] = 1
            self.positions['cash'] = self.cash
            
        else:
            raise TypeError('Pass a dataframe with dates and price data for all possible securities')

        if (isinstance(benchmark, pd.DataFrame)) and (isinstance(benchmark.index,pd.DatetimeIndex)):
            self.benchmark = benchmark
        elif benchmark == None:
            pass
        else:
            raise TypeError('Pass benchmark returns as a dataframe with a datetime index')

        self.transactions = pd.DataFrame(columns=['amount','commission','dt','order_id','price','sid','symbol','txn_dollars'])

    def check_cash(self,symbol,amount,price,date):

        # Return False if there isn't enough cash for the trade. Return True if there is money available

        if self.positions.loc[date,symbol] == 0:
            if self.positions.loc[date,'cash'] < abs(amount*price):
                return False
        elif self.positions.loc[date,symbol] > 0:
            if (amount*price > self.positions.loc[date,'cash']) or (-amount*price > self.cash):
                return False
        elif self.positions.loc[date,symbol] < 0:
            if (-amount*price > self.positions.loc[date,'cash']) or (amount*price > self.cash):
                return False
        else:
            return True

    def kelly_criterion(self,current_price,expected_price,currency,date):
        
        expected_return = 1 + (abs(expected_price - current_price)/current_price)
        favorable_probability = self.model_success_probability.loc[currency]
        current_position = abs(current_price * self.positions.loc[date,currency])

        position_size_usd = (expected_return * favorable_probability + favorable_probability - 1) / (expected_return * max(np.log(current_position)/2,1))

        return position_size_usd

    def execute_pending_orders(self,date):
    
        for order in target_orders:
            if order['long_short'] == 'long':
                if self.prices[date,order['currency']] >= order['target']:
                    portfolio.purchase_order(order['currency'],-order['amount'], self.prices[date,order['currency']], date)

            elif order['long_short'] == 'short':
                if self.prices[date,order['currency']] <= order['target']:
                    portfolio.purchase_order(order['currency'],-order['amount'], self.prices[date,order['currency']], date)

        for order in stop_losses:
            if order['long_short'] == 'long':
                if self.prices[date,order['currency']] <= order['stop']:
                    portfolio.purchase_order(order['currency'],-order['amount'], self.prices[date,order['currency']], date)

            elif order['long_short'] == 'short':
                if self.prices[date,order['currency']] >= order['stop']:
                    portfolio.purchase_order(order['currency'],-order['amount'], self.prices[date,order['currency']], date)

    def purchase_order(self,symbol,amount,price,date):

        if symbol not in self.positions:
            raise ValueError('This symbol is not in the price data passed')

        if date not in self.positions.index:
            raise ValueError('Date {} is not in the data passed'.format(date))
        
        self.check_cash(symbol,amount,price,date)

        self.num_orders += 1

        txn_dollars = (-amount * price)
        transaction_data = {
            'amount':amount,
            'commission':None,
            'dt':date,
            'order_id':self.num_orders,
            'price':price,
            'sid':symbol,'symbol':symbol,
            'txn_dollars':txn_dollars
        }
        transaction = pd.Series(transaction_data,name=date)
        self.transactions = self.transactions.append(transaction)

        if (self.positions.loc[date,symbol] <= 0) and (amount < 0):
            self.positions.loc[date:,'cash'] -= txn_dollars
        elif (self.positions.loc[date,symbol] < 0) and (amount > 0):
            self.positions.loc[date:,'cash'] -= txn_dollars
        else:
            self.positions.loc[date:,'cash'] += txn_dollars

        self.positions.loc[date:,symbol] += amount

    def set_stop_loss(self,currency,units,stop_price):

        long_short = 'long' if units >= 0 else 'short'

        stop_loss = {
            'currency': currency,
            'long_short': long_short,
            'amount': units,
            'stop': stop_price
        }

        self.pending_orders['stop_losses'].append(stop_loss)

    def set_target_order(self,currency,units,target_price):
        
        long_short = 'long' if units >= 0 else 'short'

        target_order = {
            'currency': currency,
            'long_short': long_short,
            'amount': units,
            'target': target_price
        }

        self.pending_orders['target_orders'].append(target_order)

    def long_biggest_winner(self,current_date,future_date):
        percent_next_day = ((self.predictions.loc[future_date] - self.prices.loc[current_date])/self.prices.loc[current_date]).dropna()

        if max(percent_next_day) > 0:
            currency = percent_next_day.idxmax()
            current_price = self.prices.loc[current_date,currency]
            expected_price = self.predictions.loc[future_date,currency]

            return currency, current_price, expected_price

        else:
            return False

    def short_biggest_loser(self,current_date,future_date):

        percent_next_day = ((self.predictions.loc[future_date] - self.prices.loc[current_date])/self.prices.loc[current_date]).dropna()

        if min(percent_next_day) < 0:
            currency = percent_next_day.idxmin()
            current_price = self.prices.loc[current_date,currency]
            expected_price = self.predictions.loc[future_date,currency]
            
            return currency, current_price, expected_price

        else:
            return False
        
    def calc_returns(self):

        position_changes = self.positions.mul((self.prices - self.prices.shift(1)))
        total_changes = position_changes.sum(axis=1).shift(1)
        cumulative_changes = pd.Series(self.cash + total_changes.cumsum(),name='portfolio_value').to_frame()
        cumulative_changes.loc[cumulative_changes.index[0]] = self.cash
        cumulative_changes['PnL'] = cumulative_changes['portfolio_value'] - cumulative_changes['portfolio_value'].shift(1)
        cumulative_changes['daily_returns'] = round(cumulative_changes['portfolio_value'].pct_change(),6)
        cumulative_changes['cumulative_return'] = round((cumulative_changes['portfolio_value'] / self.cash) - 1,6)
        self.returns = cumulative_changes
        
        return self.returns

    def backtest_data(self):
        self.calc_returns()
        returns = self.returns['daily_returns'].dropna()
        positions = self.positions * self.prices
        self.transactions.index = pd.to_datetime(self.transactions.index)
        transactions = self.transactions

        return returns,positions,transactions

    def backtest_pipeline(self,predictions,probabilities):
        self.predictions = predictions
        self.success_probability = probabilities
        dates = predictions.index.strftime('%Y-%m-%d').tolist()

        for date in range(len(dates)-1):

            current_date = dates[date]
            future_date = dates[date+1]

            self.execute_pending_orders(current_date)

            long_currency = self.long_biggest_winner(current_date, future_date)
            short_currency = self.short_biggest_loser(current_date, future_date)

            if long_currency is not False:
                currency, current_price, expected_price = long_currency

            if short_currency is not False:
                currency, current_price, expected_price = short_currency
            



if __name__ == '__main__':

    px_data = pd.read_csv("/Users/andresvillacis/Documents/GitHub/capstone_proj/Data/actual_df.csv", index_col='Date',parse_dates=True)
    predictions = pd.read_csv("/Users/andresvillacis/Documents/GitHub/capstone_proj/Data/predict_df.csv", index_col='Date',parse_dates=True)
    probabilities = pd.read_csv("/Users/andresvillacis/Documents/GitHub/capstone_proj/Data/correct_direction.csv", index_col='Currency')

    portfolio = Portfolio(px_data)
    # portfolio.backtest_pipeline(predictions, probabilities)
    expected_price = 0.97
    current_price = 1
    expected_return = 1 + (abs(expected_price - current_price)/current_price)

    print(expected_return)
    

    
    # print(dates[0].date())

    
    # print(((predictions.iloc[1] - portfolio.prices.iloc[0])/portfolio.prices.iloc[0]).dropna().idxmax())

    # portfolio.purchase_order('USDEUR',-500000, 1.0559, '2003-01-15')
    # # portfolio.calc_returns()

    # # returns,positions,transactions = portfolio.backtest_data()

    # # data = {'price':20}
    # # hola = data['prie'] or 0

    # print(portfolio.positions)
    # print(px_data)
