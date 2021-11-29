#You pass it a return data dataframe and it returns X_train, Y_train, X_test, and Y_test for your model
import numpy as np
import pandas as pd

def only_price(experiment_data,currency,start_train,end_train,start_test,end_test):

    experiment_px_data = experiment_data.px_data
    experiment_px_data['target'] = experiment_px_data[currency].shift(-1)
    experiment_px_data.dropna(inplace=True)

    train_data = experiment_px_data[start_train:end_train]
    X_train = train_data[currency].to_frame()
    Y_train = train_data['target'].to_frame()
    
    test_data = experiment_px_data[start_test:end_test]
    X_test = test_data[currency].to_frame()
    Y_test = test_data['target'].to_frame()

    return X_train,Y_train,X_test,Y_test

def lagged_returns(experiment_data,currency,lag,start_train,end_train,start_test,end_test):

    lag_ret = cp.Lagged_Data(experiment_data.log_ret,lag_until=lag)[currency]
    up_down = cp.Up_Down(experiment_data.log_ret,data_type='return')[currency]
    all_data = up_down.join(lag_ret,rsuffix='_right')
    all_data['Up_Down'] = all_data['Up_Down'].shift(-1)
    all_data.drop('close_right',axis=1,inplace=True,errors='ignore')
    all_data.dropna(inplace=True)

    train_data = all_data[start_train:end_train]
    X_train = train_data.loc[:, train_data.columns != 'Up_Down']
    Y_train = train_data.loc[:, 'Up_Down']

    test_data = all_data[start_test:end_test]
    X_test = test_data.loc[:, test_data.columns != 'Up_Down']
    Y_test = test_data.loc[:, 'Up_Down']

    return X_train,Y_train,X_test,Y_test

def indicators(experiment_data,currency,start_train,end_train,start_test,end_test):

    all_data = pd.DataFrame()
    all_data['close'] = experiment_data.log_ret
    all_data['Up_Down'] = cp.Up_Down(experiment_data.px_data,data_type='price')[currency]['Up_Down'].shift(-1)
    all_data['ATR'] = cp.ATR(experiment_data.px_data)[currency]['ATR']
    all_data['Momentum'] = cp.Momentum(experiment_data.px_data, period=20)[currency]['Momentum']
    all_data['50d_MA'] = cp.MA(experiment_data.px_data,period=50,ma_type='exponential')[currency]['50d_MA']
    all_data['200d_MA'] = cp.MA(experiment_data.px_data,period=200,ma_type='exponential')[currency]['200d_MA']
    all_data['RSI'] = cp.RSI(experiment_data.px_data)[currency]['RSI']
    all_data['StDev'] = cp.RollingStDev(experiment_data.px_data)[currency]['StDev']
    all_data.dropna(inplace=True)

    train_data = all_data[start_train:end_train]
    X_train = train_data.loc[:, train_data.columns != 'Up_Down']
    Y_train = train_data.loc[:, 'Up_Down']

    test_data = all_data[start_test:end_test]
    X_test = test_data.loc[:, test_data.columns != 'Up_Down']
    Y_test = test_data.loc[:, 'Up_Down']

    return X_train,Y_train,X_test,Y_test

def interpreted_indicators(experiment_data,currency,start_train,end_train,start_test,end_test):

    all_data = pd.DataFrame()
    all_data['Momentum'] = cp.Momentum(experiment_data.px_data, period=20)[currency]['Momentum']
    all_data['50d_MA'] = cp.MA(experiment_data.px_data,period=50,ma_type='exponential')[currency]['50d_MA']
    all_data['200d_MA'] = cp.MA(experiment_data.px_data,period=200,ma_type='exponential')[currency]['200d_MA']
    all_data['RSI'] = cp.RSI(experiment_data.px_data)[currency]['RSI']
    all_data['StDev'] = cp.RollingStDev(experiment_data.px_data)[currency]['StDev']

    processed = pd.DataFrame()
    processed['close'] = experiment_data.log_ret
    processed['Up_Down'] = cp.Up_Down(experiment_data.px_data,data_type='price')[currency]['Up_Down'].shift(-1)
    processed['Momentum'] = all_data['Momentum'].apply(lambda x: 1 if x >= 100 else 0)
    processed['RSI'] = all_data['RSI'].apply(lambda x: 1 if x < 30 else -1 if x > 70 else 0)
    processed['Volatility'] = all_data['StDev'].apply(lambda x: 1 if x < np.percentile(all_data['StDev'].dropna(),20) else -1 if x > np.percentile(all_data['StDev'].dropna(),80) else 0)
    processed['MA'] = np.where(all_data['50d_MA'] > all_data['200d_MA'], 1, -1)
    processed['MACD'] = np.where(cp.MACD(experiment_data.px_data)[currency]['macd'] > cp.MACD(experiment_data.px_data)[currency]['signal_line'], 1, -1)
    processed.dropna(inplace=True)

    train_data = processed[start_train:end_train]
    X_train = train_data.loc[:, train_data.columns != 'Up_Down']
    Y_train = train_data.loc[:, 'Up_Down']

    test_data = processed[start_test:end_test]
    X_test = test_data.loc[:, test_data.columns != 'Up_Down']
    Y_test = test_data.loc[:, 'Up_Down']

    return X_train,Y_train,X_test,Y_test

def indicators_lagged_returns(experiment_data,currency,lag,start_train,end_train,start_test,end_test):

    lag_ret = cp.Lagged_Data(experiment_data.log_ret,lag_until=lag)[currency]
    up_down = cp.Up_Down(experiment_data.log_ret,data_type='return')[currency]
    all_data = up_down.join(lag_ret,rsuffix='_right')
    all_data['Up_Down'] = all_data['Up_Down'].shift(-1)
    all_data.drop('close_right',axis=1,inplace=True,errors='ignore')

    all_data['ATR'] = cp.ATR(experiment_data.px_data)[currency]['ATR']
    all_data['Momentum'] = cp.Momentum(experiment_data.px_data, period=20)[currency]['Momentum']
    all_data['50d_MA'] = cp.MA(experiment_data.px_data,period=50,ma_type='exponential')[currency]['50d_MA']
    all_data['200d_MA'] = cp.MA(experiment_data.px_data,period=200,ma_type='exponential')[currency]['200d_MA']
    all_data['RSI'] = cp.RSI(experiment_data.px_data)[currency]['RSI']
    all_data['StDev'] = cp.RollingStDev(experiment_data.px_data)[currency]['StDev']
    all_data.dropna(inplace=True)

    train_data = all_data[start_train:end_train]
    X_train = train_data.loc[:, train_data.columns != 'Up_Down']
    Y_train = train_data.loc[:, 'Up_Down']

    test_data = all_data[start_test:end_test]
    X_test = test_data.loc[:, test_data.columns != 'Up_Down']
    Y_test = test_data.loc[:, 'Up_Down']

    return X_train,Y_train,X_test,Y_test

def interpreted_indicators_lagged_returns(experiment_data,currency,lag,start_train,end_train,start_test,end_test):

    lag_ret = cp.Lagged_Data(experiment_data.log_ret,lag_until=lag)[currency]
    up_down = cp.Up_Down(experiment_data.log_ret,data_type='return')[currency]
    lagged = up_down.join(lag_ret,rsuffix='_right')
    lagged['Up_Down'] = lagged['Up_Down'].shift(-1)
    lagged.drop('close_right',axis=1,inplace=True,errors='ignore')

    all_data = pd.DataFrame()
    all_data['Momentum'] = cp.Momentum(experiment_data.px_data, period=20)[currency]['Momentum']
    all_data['50d_MA'] = cp.MA(experiment_data.px_data,period=50,ma_type='exponential')[currency]['50d_MA']
    all_data['200d_MA'] = cp.MA(experiment_data.px_data,period=200,ma_type='exponential')[currency]['200d_MA']
    all_data['RSI'] = cp.RSI(experiment_data.px_data)[currency]['RSI']
    all_data['StDev'] = cp.RollingStDev(experiment_data.px_data)[currency]['StDev']

    processed = pd.DataFrame()
    processed['Momentum'] = all_data['Momentum'].apply(lambda x: 1 if x >= 100 else 0)
    processed['RSI'] = all_data['RSI'].apply(lambda x: 1 if x < 30 else -1 if x > 70 else 0)
    processed['Volatility'] = all_data['StDev'].apply(lambda x: 1 if x < np.percentile(all_data['StDev'].dropna(),20) else -1 if x > np.percentile(all_data['StDev'].dropna(),80) else 0)
    processed['MA'] = np.where(all_data['50d_MA'] > all_data['200d_MA'], 1, -1)
    processed['MACD'] = np.where(cp.MACD(experiment_data.px_data)[currency]['macd'] > cp.MACD(experiment_data.px_data)[currency]['signal_line'], 1, -1)

    final_df = lagged.join(processed)
    final_df.dropna(inplace=True)

    train_data = final_df[start_train:end_train]
    X_train = train_data.loc[:, train_data.columns != 'Up_Down']
    Y_train = train_data.loc[:, 'Up_Down']

    test_data = final_df[start_test:end_test]
    X_test = test_data.loc[:, test_data.columns != 'Up_Down']
    Y_test = test_data.loc[:, 'Up_Down']

    return X_train,Y_train,X_test,Y_test


if __name__ == '__main__':
    # import capstone_proj as cp
    
    # filepath = "/Users/andresvillacis/Documents/GitHub/capstone_proj/Data/FX_Test_USD-per-FX_Chicago_2021_11_04.csv"
    # experiment_data = cp.Batch(start='2003-01-01',end='2021-11-04',currencies='USDEUR',filepath=filepath)

    # X_train,Y_train,X_test,Y_test = only_price(experiment_data, 'USDEUR', '2003-01-01', '2020-12-31', '2021-01-01', '2021-11-04')

    # print(X_train.join(Y_train))

    pass



