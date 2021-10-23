#Maybe include easy graphs here

import numpy as np
import pandas as pd

class Currency_data():
    
    def __init__(self,filepath=None):

        import json

        if filepath != None:
            try:
                self.px_data = pd.read_csv(filepath,index_col='DATE',parse_dates=True)
            except:
                pass
        elif True:
            try:
                settings_file = open('Trading/settings.json')
                data = json.load(settings_file)

                if data['csv_file']['csv_file_location']:
                    self.px_data = pd.read_csv(data['csv_file']['csv_file_location'],index_col='DATE',parse_dates=True)
            except:
                pass
        else:
            try:
                self.px_data = pd.read_csv('./Data/FX_Test_USD-per-FX_Chicago.csv',index_col='DATE',parse_dates=True)
            except:
                print('Update csv data file location in /Trading/settings.json or provide filepath')

class Batch(Currency_data):    
    
    def __init__(self,filepath=None,start=None,end=None,days=0,months=0,years=0,currencies=None):

        super().__init__(filepath)

        self.start = start
        self.end = end
        self.days = days
        self.months = months
        self.years = years
        self.currencies = currencies

        if (self.start == None) and (self.end == None):
                raise ValueError('You need to provide a start date, end date, or both.')

        if (self.start != None) and (self.end != None):
            if self.end > self.start:
                self.px_data= self.px_data[self.start:self.end]
            else:
                raise Exception('The end date must be after the start date')
        else:

            if (self.start == None) and (self.end != None):
                self.days,self.months,self.years = -self.days,-self.months,-self.years
            
            year, month, day = self.start.split('-')
            year, month, day = int(year), int(month), int(day)

            if self.years != 0:
                year = year + self.years

            if self.months != 0:
                if (month + self.months) > 12:
                    month = 1 + ((month + self.months) % 12)
                    year = year + ((month + self.months) // 12)
                elif (month + self.months) < 1:
                    month = 12 - ((month - self.months) % 12)
                    year = year - ((month - self.months + 1) // 12)
                else:
                    month = month + self.months

            if self.days != 0:
                if self.start != None:
                    cropped_data = self.px_data[self.start:]
                    self.px_data = cropped_data[:self.days]
                if self.end != None:
                    cropped_data = self.px_data[:self.end]
                    self.px_data = cropped_data[self.days:]
            else:
                start_end_date = '{}-{}-{}'.format(year,month,day)
                if self.start != None:
                    self.px_data= self.px_data[self.start:start_end_date]
                if self.end != None:
                    self.px_data = self.px_data[start_end_date:self.end]

        if (type(self.currencies) == str) or (type(self.currencies) == list):
            self.px_data = self.px_data[self.currencies]
        elif self.currencies == None:
            pass
        else:
            raise Exception('Please enter a string/list for the currencies you want to analyze or leave empty.')

        try:
            self.px_data = self.px_data.to_frame()
        except:
            pass

        self.num_rows = len(self.px_data)
        self.num_cols = len(self.px_data.columns)
        self.px_change = self.px_data - self.px_data.shift(1)
        self.pct_change = self.px_data.pct_change()
        self.log_ret = np.log1p(self.pct_change)

    def stats(self):
        
        self.stats_df = pd.DataFrame(columns=['Minimum','Maximum','Average','Median','StDev'])

        for column in self.px_data.columns:
            data = self.px_data[column]
            minimum = min(self.px_data[column])
            maximum = max(self.px_data[column])
            average = np.mean(self.px_data[column])
            median = np.median(self.px_data[column])
            stdev = np.std(self.px_data[column])
            self.stats_df.loc[column] = [minimum,maximum,average,median,stdev]

        return self.stats_df

class Random_batch(Currency_data):

    def __init__(self,start=None,spec_days=None,min_days=1,max_days=None,currencies=None,spec_curr=None,min_currencies=1,max_currencies=None,seed=None,filepath=None):

        super().__init__(filepath)
        import random
        random.seed(None)

        self.start = start
        self.spec_days = spec_days
        self.min_days = min_days
        self.max_days = max_days
        self.currencies = currencies
        self.spec_curr = spec_curr
        self.min_currencies = min_currencies
        self.max_currencies = max_currencies

        if self.start != None:
            self.px_data = self.px_data[self.start:]
            if self.spec_days != None:
                self.px_data = self.px_data[:self.spec_days]
            else:
                max_num = self.max_days or len(self.px_data)
                rand_num = random.randint(self.min_days,max_num)
                self.px_data = self.px_data[:rand_num]
        
        else:
            rand_start = random.randint(1,len(self.px_data)-self.min_days)
            self.px_data = self.px_data[rand_start:]
            max_num = self.max_days or (len(self.px_data)-self.min_days)
            self.px_data = self.px_data[:random.randint(self.min_days,max_num)]

        if self.currencies != None:
            if (type(self.currencies) == str) or (type(self.currencies) == list):
                self.px_data = self.px_data[self.currencies]
            else:
                raise Exception('Please enter a string/list for the currencies you want to analyze or leave empty.')

        elif self.spec_curr != None:
            rand_curr = random.sample(list(self.px_data.columns),self.spec_curr)
            self.px_data = self.px_data[rand_curr]

        else:
            max_curr = self.max_currencies or len(self.px_data.columns)
            num_curr = random.randint(self.min_currencies,max_curr)
            rand_curr = random.sample(list(self.px_data.columns),num_curr)
            self.px_data = self.px_data[rand_curr]

        try:
            self.px_data = self.px_data.to_frame()
        except:
            pass

        self.num_rows = len(self.px_data)
        self.num_cols = len(self.px_data.columns)
        self.px_change = self.px_data - self.px_data.shift(1)
        self.pct_change = self.px_data.pct_change()
        self.log_ret = np.log1p(self.pct_change)

    def stats(self):
        
        self.stats_df = pd.DataFrame(columns=['Minimum','Maximum','Average','Median','StDev'])

        for column in self.px_data.columns:
            data = self.px_data[column]
            minimum = min(self.px_data[column])
            maximum = max(self.px_data[column])
            average = np.mean(self.px_data[column])
            median = np.median(self.px_data[column])
            stdev = np.std(self.px_data[column])
            self.stats_df.loc[column] = [minimum,maximum,average,median,stdev]

        return self.stats_df

if __name__ == '__main__':
    batch = Batch(start='1999-01-01',end='2000-01-01',currencies=['USDEUR','USDGBP'])
    # # randombatch = Random_batch(start='1999-01-01',min_days=10,max_days=30,max_currencies=3,min_currencies=1)
    print(batch.px_data)
    