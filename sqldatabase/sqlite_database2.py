import sqlite3
import pandas as pd
import sqlalchemy
import yfinance as yf
engine = sqlalchemy.create_engine('sqlite:///OurDataBase.db')
pd.read_sql('SELECT * FROM employees WHERE salary  > 10000', engine)
df1 = pd.DataFrame([{'name' : 'Maxwell', 'surname' : 'Foster', 'salary': 12000.00}])
df1.to_sql('employees', engine, if_exists='append', index=False)
pd.read_sql('employees', engine)

df = yf.download('GME', '2021-01-01')
df.to_sql('GME', engine)
pd.read_sql('GME', engine)
