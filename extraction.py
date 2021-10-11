class Currency_data():
    
    def __init__(self):

        import pandas as pd

        self.filename = 'FX_Test_USD-per-FX_Chicago.csv'
        self.fin_data = pd.read_csv(self.filename,index_col='DATE',parse_dates=True)

    def batch(self,start=None,end=None,days=0,months=0,years=0,currencies=None):

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

        return self.fin_data

#random _times
# and then let's do indicators
#Should currency just be the base class and batch another object that inherits from it


if __name__ == '__main__':
    hola = Currency_data()
    data = hola.batch(end='1997-01-01',days=30,currencies=['USDEUR','USDGBP'])
    print(hola.log_ret)