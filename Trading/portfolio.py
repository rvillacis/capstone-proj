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

        if self.positions.loc[date,symbol] == 0:
            if self.positions.loc[date,'cash'] < abs(amount*price):
                raise ValueError('There is not enough available cash to buy {} {} on {}'.format(amount,symbol,date))
        elif self.positions.loc[date,symbol] > 0:
            if (amount*price > self.positions.loc[date,'cash']) or (-amount*price > self.cash):
                raise ValueError('There is not enough available cash to buy {} {} on {}'.format(amount,symbol,date))
        elif self.positions.loc[date,symbol] < 0:
            if (-amount*price > self.positions.loc[date,'cash']) or (amount*price > self.cash):
                raise ValueError('There is not enough available cash to buy {} {} on {}'.format(amount,symbol,date))

    def kelly_criterion(self,current_price,expected_price,currency,date):
        
        expected_return = 1 + (abs(expected_price - current_price)/current_price)
        favorable_probability = self.model_success_probability.loc[currency]
        current_position = abs(current_price * self.positions.loc[date,currency])

        position_size_usd = (expected_return * favorable_probability + favorable_probability - 1) / (expected_return * max(np.log(current_position)/2,1))

        return position_size_usd

    def execute_pending_orders(self,df_actual,date):
    
        for order in target_orders:
            if order['long_short'] == 'long':
                if df_actual[date,order['currency']] >= order['target']:
                    portfolio.purchase_order(order['currency'],-order['amount'], df_actual[date,order['currency']], date)

            elif order['long_short'] == 'short':
                if df_actual[date,order['currency']] <= order['target']:
                    portfolio.purchase_order(order['currency'],-order['amount'], df_actual[date,order['currency']], date)

        for order in stop_losses:
            if order['long_short'] == 'long':
                if df_actual[date,order['currency']] <= order['stop']:
                    portfolio.purchase_order(order['currency'],-order['amount'], df_actual[date,order['currency']], date)

            elif order['long_short'] == 'short':
                if df_actual[date,order['currency']] >= order['stop']:
                    portfolio.purchase_order(order['currency'],-order['amount'], df_actual[date,order['currency']], date)

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

    def long_biggest_winner():
        pass

    def short_biggest_loser():
        pass
        
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


if __name__ == '__main__':

    batch = Batch(start='2003-01-01',days=30,currencies='USDEUR')
    batch = Batch(start='2003-01-01',days=30,currencies=['USDEUR','USDGBP'])
    portfolio = Portfolio(batch.px_data)
    portfolio.purchase_order('USDEUR',-500000, 1.0559, '2003-01-15')
    # portfolio.calc_returns()

    # returns,positions,transactions = portfolio.backtest_data()

    # data = {'price':20}
    # hola = data['prie'] or 0

    print(portfolio.positions)