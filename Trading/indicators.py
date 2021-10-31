# Add indicators separately and then also all of them to a dataframe at once, or selecting which ones you want
import numpy as np
import pandas as pd
from .extraction import Batch, Random_batch

def prepare_data(data):

    if isinstance(data, Batch) or isinstance(data, Random_batch):
        data = data.px_data

    if ((isinstance(data, pd.DataFrame)) and (len(data.columns)==1)) or ((isinstance(data, pd.DataFrame)) and ('close' in data)):
        data.rename(columns={data.columns[0]:'close'},inplace=True)
        data['high'] = data['close'].cummax()
        data['low'] = data['close'].cummin()
        return data

    elif (isinstance(data, pd.DataFrame)) and (len(data.columns)>1):
        all_columns_dict = {}
        for column in data.columns:

            column_df = data[column]
            column_df = column_df.to_frame()
            column_df.rename(columns={column:'close'},inplace=True)
            column_df['high'] = column_df['close'].cummax()
            column_df['low'] = column_df['close'].cummin()

            all_columns_dict[column] = column_df

        return all_columns_dict

    elif type(data) == dict:
        for key,value in data.items():
            if 'high' not in value:
                value['high'] = value['close'].cummax()
            if 'low' not in value:
                value['low'] = value['close'].cummax()
        return data

    else:
        raise TypeError('Pass a Dataframe or dictionary with currency data')

def ATR(currency_data,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import AverageTrueRange

    if isinstance(clean_data, pd.DataFrame):
        indicator = AverageTrueRange(input_data=clean_data).getTiData()
        clean_data['ATR'] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = AverageTrueRange(input_data=data).getTiData()
            data['ATR'] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

def Bollinger(currency_data,period=20,std_number=2,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import BollingerBands

    if isinstance(clean_data, pd.DataFrame):
        indicator = BollingerBands(input_data=clean_data,period=period,std_number=std_number).getTiData()
        clean_data = clean_data.join(indicator)

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = BollingerBands(input_data=data,period=period,std_number=std_number).getTiData()
            data = data.join(indicator)

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
        
            clean_data[currency] = data
    
    return clean_data

def Fibonacci(currency_data,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import FibonacciRetracement

    if isinstance(clean_data, pd.DataFrame):
        indicator = FibonacciRetracement(input_data=clean_data).getTiData()
        clean_data = indicator.iloc[-1]

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = FibonacciRetracement(input_data=data).getTiData()
            data = indicator.iloc[-1]
            clean_data[currency] = data
        
    return clean_data

def Momentum(currency_data,period=12,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import Momentum

    if isinstance(clean_data, pd.DataFrame):
        indicator = Momentum(input_data=clean_data,period=period).getTiData()
        clean_data['Momentum'] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = Momentum(input_data=data,period=period).getTiData()
            data['Momentum'] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

def MA(currency_data,period=20,ma_type='simple',show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import MovingAverage

    if isinstance(clean_data, pd.DataFrame):
        indicator = MovingAverage(input_data=clean_data,period=period,ma_type=ma_type).getTiData()
        clean_data['{}d_MA'.format(period)] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = MovingAverage(input_data=data,period=period,ma_type=ma_type).getTiData()
            data['{}d_MA'.format(period)] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

def MACD(currency_data,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import MovingAverageConvergenceDivergence

    if isinstance(clean_data, pd.DataFrame):
        indicator = MovingAverageConvergenceDivergence(input_data=clean_data).getTiData()
        clean_data = clean_data.join(indicator)

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = MovingAverageConvergenceDivergence(input_data=data).getTiData()
            data = data.join(indicator)

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
        
            clean_data[currency] = data
    
    return clean_data

def RSI(currency_data,period=14,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import RelativeStrengthIndex

    if isinstance(clean_data, pd.DataFrame):
        indicator = RelativeStrengthIndex(input_data=clean_data,period=period).getTiData()
        clean_data['RSI'] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = RelativeStrengthIndex(input_data=data,period=period).getTiData()
            data['RSI'] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

def RMI(currency_data,period=14,momentum_period=4,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import RelativeMomentumIndex

    if isinstance(clean_data, pd.DataFrame):
        indicator = RelativeMomentumIndex(input_data=clean_data,period=period).getTiData()
        clean_data['RMI'] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = RelativeMomentumIndex(input_data=data,period=period).getTiData()
            data['RMI'] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

def StochasticO(currency_data,k_periods=14, k_slowing_periods=1,d_periods=3, d_method='simple',show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import StochasticOscillator

    if isinstance(clean_data, pd.DataFrame):
        indicator = StochasticOscillator(input_data=clean_data,k_periods=k_periods, k_slowing_periods=k_slowing_periods,d_periods=d_periods, d_method=d_method).getTiData()
        clean_data = clean_data.join(indicator)

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = StochasticOscillator(input_data=data,k_periods=k_periods, k_slowing_periods=k_slowing_periods,d_periods=d_periods, d_method=d_method).getTiData()
            data = data.join(indicator)

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
        
            clean_data[currency] = data
    
    return clean_data

def RollingStDev(currency_data,period=20,show_hl=False):

    clean_data = prepare_data(currency_data)

    from tti.indicators import StandardDeviation

    if isinstance(clean_data, pd.DataFrame):
        indicator = StandardDeviation(input_data=clean_data, period=period).getTiData()
        clean_data['StDev'] = indicator

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            indicator = StandardDeviation(input_data=data, period=period).getTiData()
            data['StDev'] = indicator

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')
    
    return clean_data

#----------------------------------------------------------------------------------------------------
def Up_Down(px_or_ret,data_type='price',show_hl=False):

    clean_data = prepare_data(px_or_ret)

    if isinstance(clean_data, pd.DataFrame):
        if data_type == 'price':
            clean_data['Up_Down'] = clean_data['close'].pct_change().apply(lambda x: 'Up' if x >= 0 else 'Down')
        elif data_type == 'return':
            clean_data['Up_Down'] = clean_data['close'].apply(lambda x: 'Up' if x >= 0 else 'Down' )

        if show_hl != True:
            clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            if data_type == 'price':
                data['Up_Down'] = data['close'].pct_change().apply(lambda x: 'Up' if x >= 0 else 'Down')
            elif data_type == 'return':
                data['Up_Down'] = data['close'].apply(lambda x: 'Up' if x >= 0 else 'Down' )

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    return clean_data

def Lagged_Data(px_or_ret,lag=None,lag_until=None,col_to_lag=None,show_hl=False):

    if col_to_lag == None:
        raise ValueError('Specify column to lag')

    clean_data = prepare_data(px_or_ret)

    if isinstance(clean_data, pd.DataFrame):
        if lag != None:
            clean_data['lag_{}'.format(lag)] = clean_data[col_to_lag].shift(lag)
        elif lag_until != None:
            for lags in range(-1 if lag_until<0 else 1,lag_until-1 if lag_until<0 else lag_until+1,-1 if lag_until<0 else 1):
                clean_data['lag_{}'.format(lags)] = clean_data[col_to_lag].shift(lags)

        if show_hl != True:
                clean_data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    elif type(clean_data) == dict:
        for currency,data in clean_data.items():
            if lag != None:
                data['lag_{}'.format(lag)] = data[col_to_lag].shift(lag)
            elif lag_until != None:
                for lags in range(-1 if lag_until<0 else 1,lag_until-1 if lag_until<0 else lag_until+1,-1 if lag_until<0 else 1):
                    data['lag_{}'.format(lags)] = data[col_to_lag].shift(lags)

            if show_hl != True:
                data.drop(['high','low'],axis=1,inplace=True,errors='ignore')

    return clean_data

if __name__ == '__main__':
    # batch = Batch(start='1999-01-01',days=30, currencies=['USDEUR','USDGBP'])
    # indicator = Lagged_Data(batch.px_data,lag_until=3)
    # print(indicator['USDEUR'])

    # experiment = Batch(start='2003-01-01',end='2004-12-31',currencies=['USDEUR','USDGBP'])
    experiment = Batch(start='2003-01-01',end='2004-12-31',currencies='USDEUR')
    lagged = Lagged_Data(experiment, lag_until=-3, col_to_lag='close')
    atr = ATR(lagged)
    ma_20d = MA(atr)
    print(ma_20d)
    