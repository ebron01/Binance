"""This code reads the values from the database we created with the code file 04Cryptobot.py
The have a live streaming data 04Cryptobot.py must be running simultaneously """

import sqlalchemy
import pandas as pd
from binance.client import Client
from keys import api_keys

binance_api, binance_secret = api_keys()
client = Client(binance_api, binance_secret)
engine = sqlalchemy.create_engine('sqlite:///sqldatabase/BTCUSDTstream.db')

df = pd.read_sql('BTCUSDT', engine)

#Trendfollowing
#if the crypto was rising by x % -> buy
#exit when profit is above 0.15% or loss is crossing -0.15%

def strategy(entry, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql('BTCUSDT', engine)
        lookbackperiod = df.iloc[-lookback:] #this brings rows of lookback window from the database
        cumreturn = (lookbackperiod.Price.pct_change()+1).cumprod()-1 #this checks the price change in the window by considering two entries as s, s+1
        print('not yet')
        if not open_position:
            print(cumreturn[cumreturn.last_valid_index()])
            if cumreturn[cumreturn.last_valid_index()] > entry :#cumreturn[-1] means last valid entry of this cumulative return of lookback window
                print('Here we go')
                order = client.create_order(symbol='BTCUSDT',
                                            side='BUY',
                                            type='MARKET',
                                            quantity= qty)
                print(order)
                open_position = True
                break
    if open_position:
        while True:
            df = pd.read_sql('BTCUSDT', engine)
            sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'], unit='ms')]
            print('waiting to sell')
            if len(sincebuy) > 1:
                sincebuyreturn = (sincebuy.Price.pct_change()+1).cumprod()-1
                last_entry = sincebuyreturn[sincebuyreturn.last_valid_index()]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    print('I am selling')
                    order = client.create_order(symbol='BTCUSDT',
                                            side='SELL',
                                            type='MARKET',
                                            quantity= qty)
                    print(order)
                    open_position = False
                    break

strategy(0.001, 60, 0.001)