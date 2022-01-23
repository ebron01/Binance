import sqlalchemy
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
from data.coins import coin_details
from binance.client import Client
from keys import api_keys
from indics import indicator
from TAlib import conditions

def job(symbol, interval, dbname):
    print("connection is started")
    engine = sqlalchemy.create_engine('sqlite:///../history/DBDEV/' + dbname + '.db')
    print("connection is started")
    prices = pd.read_sql('SELECT * FROM ' + symbol + interval + '', engine)
    """Does required calculations based on indicator types"""
    indicators = indicator.Indicators()
    result = indicator.Calculate.calculator(indicators, prices)
    conditions.MACDRSIcondreal(result)

if __name__ == '__main__':
    dbname = 'DEVSELECTED_15JAN'
    symbol, intervals = coin_details()
    symbol = "BTCUSDT"
    interval = intervals[0]
    job(symbol, '30MINUTE', dbname)


