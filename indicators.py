# Add indicators separately and then also all of them to a dataframe at once, or selecting which ones you want
import numpy as np
import pandas as pd
from extraction import Batch, Random_batch
from tti.indicators import StandardDeviation, RelativeVolatilityIndex

def prepare_data(px_data):

    all_columns_dict = {}
    
    for column in px_data.columns:

        column_df = px_data[column]
        column_df = column_df.to_frame()
        column_df.rename(columns={column:'close'},inplace=True)
        column_df['high'] = column_df['close'].cummax()
        column_df['low'] = column_df['close'].cummin()

        all_columns_dict[column] = column_df

    return all_columns_dict

def ATR(px_data,show_hl=False):

    from tti.indicators import AverageTrueRange

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = AverageTrueRange(input_data=data).getTiData()
        data['ATR'] = indicator

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
    
    return col_dict

def Bollinger(px_data,period=20,std_number=2,show_hl=False):

    from tti.indicators import BollingerBands

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = BollingerBands(input_data=data,period=period,std_number=std_number).getTiData()
        data = data.join(indicator)

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
        
        col_dict[currency] = data
    
    return col_dict

def Fibonacci(px_data,show_hl=False):

    from tti.indicators import FibonacciRetracement

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = FibonacciRetracement(input_data=data).getTiData()
        data = indicator.iloc[-1]
        col_dict[currency] = data

    return col_dict

def Momentum(px_data,period=12,show_hl=False):

    from tti.indicators import Momentum

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = Momentum(input_data=data,period=period).getTiData()
        data['Momentum'] = indicator

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
    
    return col_dict

def MA(px_data,period=20,ma_type='simple',show_hl=False):

    from tti.indicators import MovingAverage

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = MovingAverage(input_data=data,period=period,ma_type=ma_type).getTiData()
        data['{}d_MA'.format(period)] = indicator

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
    
    return col_dict

def MACD(px_data,show_hl=False):

    from tti.indicators import MovingAverageConvergenceDivergence

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = MovingAverageConvergenceDivergence(input_data=data).getTiData()
        data = data.join(indicator)

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
        
        col_dict[currency] = data
    
    return col_dict

def RSI(px_data,period=14,show_hl=False):

    from tti.indicators import RelativeStrengthIndex

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = RelativeStrengthIndex(input_data=data,period=period).getTiData()
        data['RSI'] = indicator

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
    
    return col_dict

def RMI(px_data,period=14,momentum_period=4,show_hl=False):

    from tti.indicators import RelativeMomentumIndex

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = RelativeMomentumIndex(input_data=data,period=period,momentum_period=momentum_period).getTiData()
        data['RMI'] = indicator

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
    
    return col_dict

def StochasticO(px_data,k_periods=14, k_slowing_periods=1,d_periods=3, d_method='simple',show_hl=False):

    from tti.indicators import StochasticOscillator

    col_dict = prepare_data(px_data)

    for currency,data in col_dict.items():
        indicator = StochasticOscillator(input_data=data,k_periods=k_periods, k_slowing_periods=k_slowing_periods,d_periods=d_periods, d_method=d_method).getTiData()
        data = data.join(indicator)

        if show_hl != True:
            data.drop(['high','low'],axis=1,inplace=True)
        
        col_dict[currency] = data
    
    return col_dict

def up_down(px_data):
    pass
    #Make also an indicator that shows if the day is up or down
    #Do also a way that you can collect multiple indicators at once


if __name__ == '__main__':
    # batch = Batch(start='1999-01-01',days=30, currencies=['USDEUR','USDGBP'])
    # indicator = StochasticO(batch.px_data)
    # print(indicator['USDEUR'])


    batch = Batch(start='1999-01-01',days=30, currencies='USDEUR').px_data
    prepared = prepare_data(batch)['USDEUR']
    indicator = StochasticOscillator(prepared)
    print(indicator.getTiData())