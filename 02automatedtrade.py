from binance.client import Client
import pandas as pd
from keys import api_keys


binance_api, binance_secret = api_keys()
client = Client(binance_api, binance_secret)
#print(client.get_account())

#datastream with websocket - will not be covered in this code
#print(pd.DataFrame(client.get_historical_klines('BTCUSDT', '1m', '30 m ago UTC')))

def getminutedata(symbol, interval, lookback):
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC'))
    df = df.iloc[:, :6]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df.set_index('Time')
    df.index = pd.to_datetime(df.index, unit = 'ms')
    df = df.astype(float)
    return df

#test = getminutedata('BTCUSDT', '1m', '30')

#buy if asset fell by more then 0.2% within the last 30 min
#sell if asset rises by more then 0.15% or falls further by 0.15%
def strategytest(symbol, qty, entered = False):
    df = getminutedata(symbol, '1m', '15')
    cumulret = (df.Open.pct_change() +1).cumprod() - 1
    if not entered:
        if cumulret[-1] < -0.002:
            order = client.create_order(symbol=symbol, side='BUY',
                                        type='MARKET', quantity=qty)
            print(order)
            entered = True
        else:
            print('No trade has been executed')
    if entered:
        while True:#after order is created we have to control how the asset behaved in every minute
            df = getminutedata(symbol, '1m', '15')
            sincebuy = df.loc[df.index > pd.to_datetime(order['transactTime'], unit='ms')]
            if len(sincebuy) > 0:
                sincebuyret = (sincebuy.Open.pct_change() +1).cumprod() - 1
                if sincebuyret[-1] > 0.0015 or sincebuyret[-1] < -0.0015:
                    order = client.create_order(symbol=symbol, side='SELL',
                                                type='MARKET', quantity=qty)
                    print(order)
                    break

strategytest('ALGOUSDT', 7)