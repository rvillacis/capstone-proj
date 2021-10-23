import numpy as np
import pandas as pd

class Portfolio():

    def __init__(self,positions=None,trades=None):
        self.positions = positions or dict()
        self.trades = trades or list()
        self.returns = dict()
        self.stdev = dict()
        self.sharpe = dict()
        self.VaR = dict()
        self.max_drawdown = dict()

    def buy_order():
        pass

    def sell_order():
        pass

    def calc_returns():
        pass

    def calc_stdev():
        pass

    def calc_sharpe():
        pass

    def calc_VaR():
        pass

    def calc_max_drawdown():
        pass

    #Also gonna need graphs for this