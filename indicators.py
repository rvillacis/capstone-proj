# Add indicators separately and then also all of them to a dataframe at once, or selecting which ones you want
import numpy as np
import pandas as pd
from extraction import Batch, Random_batch
from tti.indicators import AverageTrueRange, BollingerBands, FibonacciRetracement, Momentum, MovingAverage, MovingAverageConvergenceDivergence, RelativeStrengthIndex, StochasticOscillator
#Maybe add high and low columns

def prepare_data(fin_data):

    all_columns = {}
    
    for column in fin_data.columns:

        column_df = fin_data[column]
        column_df = column_df.to_frame()
        column_df.rename(columns={column:'close'},inplace=True)
        

        all_columns[column] = column_df

    return all_columns

if __name__ == '__main__':
    batch = Batch(start='1999-01-01',days=35, currencies='USDEUR')
    new_data = prepare_data(batch.fin_data)
    cols = MovingAverage(new_data['USDEUR'])
    print(cols.getTiData())