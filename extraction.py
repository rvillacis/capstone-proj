class Currency_data():
    
    def __init__(self):

        import pandas as pd

        self.filename = 'FX_Test_USD-per-FX_Chicago.csv'
        self.fin_data = pd.read_csv(self.filename,index_col='DATE',parse_dates=True)

class Batch(Currency_data):    
    
    def __init__(self,start=None,end=None,days=0,months=0,years=0,currencies=None):

        super().__init__()
        import numpy as np

        self.start = start
        self.end = end
        self.days = days
        self.months = months
        self.years = years
        self.currencies = currencies

        if (self.start == None) and (self.end == None):
                raise ValueError('You need to provide a start date, end date, or both.')

        if (self.end != None) and (self.start == None):
            self.days,self.months,self.years = -self.days,-self.months,-self.years

        if (self.start != None) and (self.end != None):
            if self.end > self.start:
                self.fin_data= self.fin_data[self.start:self.end]
            else:
                raise Exception('The end date must be after the start date')
            
        if self.start != None:
            year, month, day = self.start.split('-')
        else:
            year, month, day = self.end.split('-')
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
                cropped_data = self.fin_data[self.start:]
                self.fin_data = cropped_data[:self.days]
            if self.end != None:
                cropped_data = self.fin_data[:self.end]
                self.fin_data = cropped_data[self.days:]
        else:
            start_end_date = '{}-{}-{}'.format(year,month,day)
            if self.start != None:
                self.fin_data= self.fin_data[self.start:start_end_date]
            if self.end != None:
                self.fin_data = self.fin_data[start_end_date:self.end]

        if (type(self.currencies) == str) or (type(self.currencies) == list):
            self.fin_data = self.fin_data[self.currencies]
        elif self.currencies == None:
            pass
        else:
            raise Exception('Please enter a string/list for the currencies you want to analyze or leave empty.')

        try:
            self.fin_data = self.fin_data.to_frame()
        except:
            pass

        self.num_rows = len(self.fin_data)
        self.num_cols = len(self.fin_data.columns)
        self.px_change = self.fin_data - self.fin_data.shift(1)
        self.pct_change = self.fin_data.pct_change()
        self.log_ret = np.log1p(self.pct_change)

    def stats(self):
        
        import numpy as np
        import pandas as pd
        self.stats_df = pd.DataFrame(columns=['Minimum','Maximum','Average','Median','StDev'])

        for column in self.fin_data.columns:
            data = self.fin_data[column]
            minimum = min(self.fin_data[column])
            maximum = max(self.fin_data[column])
            average = np.mean(self.fin_data[column])
            median = np.median(self.fin_data[column])
            stdev = np.std(self.fin_data[column])
            self.stats_df.loc[column] = [minimum,maximum,average,median,stdev]

        return self.stats_df

class Random_batch(Currency_data):

    def __init__(self,start=None,spec_days=None,min_days=1,max_days=None,currencies=None,spec_curr=None,min_currencies=1,max_currencies=None,seed=None):

        super().__init__()
        import random
        import numpy as np

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
            self.fin_data = self.fin_data[self.start:]
            if self.spec_days != None:
                self.fin_data = self.fin_data[:self.spec_days]
            else:
                max_num = self.max_days or len(self.fin_data)
                rand_num = random.randint(self.min_days,max_num)
                self.fin_data = self.fin_data[:rand_num]
        
        else:
            rand_start = random.randint(1,len(self.fin_data)-self.min_days)
            self.fin_data = self.fin_data[rand_start:]
            max_num = self.max_days or (len(self.fin_data)-self.min_days)
            self.fin_data = self.fin_data[:random.randint(self.min_days,max_num)]

        if self.currencies != None:
            if (type(self.currencies) == str) or (type(self.currencies) == list):
                self.fin_data = self.fin_data[self.currencies]
            else:
                raise Exception('Please enter a string/list for the currencies you want to analyze or leave empty.')

        elif self.spec_curr != None:
            rand_curr = random.sample(list(self.fin_data.columns),self.spec_curr)
            self.fin_data = self.fin_data[rand_curr]

        else:
            max_curr = self.max_currencies or len(self.fin_data.columns)
            num_curr = random.randint(self.min_currencies,max_curr)
            rand_curr = random.sample(list(self.fin_data.columns),num_curr)
            self.fin_data = self.fin_data[rand_curr]

        try:
            self.fin_data = self.fin_data.to_frame()
        except:
            pass

        self.num_rows = len(self.fin_data)
        self.num_cols = len(self.fin_data.columns)
        self.px_change = self.fin_data - self.fin_data.shift(1)
        self.pct_change = self.fin_data.pct_change()
        self.log_ret = np.log1p(self.pct_change)

    def stats(self):
        
        import numpy as np
        import pandas as pd
        self.stats_df = pd.DataFrame(columns=['Minimum','Maximum','Average','Median','StDev'])

        for column in self.fin_data.columns:
            data = self.fin_data[column]
            minimum = min(self.fin_data[column])
            maximum = max(self.fin_data[column])
            average = np.mean(self.fin_data[column])
            median = np.median(self.fin_data[column])
            stdev = np.std(self.fin_data[column])
            self.stats_df.loc[column] = [minimum,maximum,average,median,stdev]

        return self.stats_df

if __name__ == '__main__':
    batch = Batch(start='1997-01-01',days=30,currencies=['USDEUR','USDGBP'])
    randombatch = Random_batch(start='1999-01-01',min_days=10,max_days=30,max_currencies=3,min_currencies=1)
    print(randombatch.stats())
    