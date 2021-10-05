class Currency_data():
    
    def __init__(self):
        self.filename = 'FX_Test_USD-per-FX_Chicago.csv'

        import numpy as np
        import pandas as pd

        self.fin_data = pd.read_csv(self.filename,index_col='DATE',parse_dates=True)

    def batch(self,start=None,end=None,days=None,months=None,years=None,currencies=None):
        self.start = start
        self.end = end
        self.days = days
        self.months = months
        self.years = years
        self.currencies = currencies

        if self.start != None:
            if self.end != None:
                return self.fin_data[start:end]
            elif days != None:
                data = self.fin_data[start:]
                return data[:days]
            elif months != None:
                year, month, day = start.split('-')
                # bye, chao, todo = int(bye), int(chao), int(todo)
                #You have to consider what if it rolls to the next year
            elif years != None:
                year, month, day = start.split('-')
                new_year = int(year) + years
                end_date = '{}-{}-{}'.format(new_year,month,day)
                return self.fin_data[start:end_date]


if __name__ == '__main__':
    hola = Currency_data()
    hola.batch('1992-01-01',years=1)