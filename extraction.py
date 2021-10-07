class Currency_data():
    
    def __init__(self):
        self.filename = 'FX_Test_USD-per-FX_Chicago.csv'

        import numpy as np
        import pandas as pd

        self.fin_data = pd.read_csv(self.filename,index_col='DATE',parse_dates=True)

    def batch(self,start=None,end=None,days=0,months=0,years=0,currencies=None):
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
                return self.fin_data[self.start:self.end]
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
                return cropped_data[:self.days]
            if self.end != None:
                cropped_data = self.fin_data[:self.end]
                return cropped_data[self.days:]

        start_end_date = '{}-{}-{}'.format(year,month,day)
        if self.start != None:
            return self.fin_data[self.start:start_end_date]
        if self.end != None:
            return self.fin_data[start_end_date:self.end]


#log_returns - maybe do this a a feature, add number of days or columns as features
#random _times
# and then let's do indicators


if __name__ == '__main__':
    hola = Currency_data()
    print(hola.batch(end='1996-01-01',years=1))