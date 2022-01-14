import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def MACD(rawprices):
    rawprices['EMA12'] = rawprices['close_price'].ewm(span=12).mean()
    rawprices['EMA26'] = rawprices['close_price'].ewm(span=26).mean()
    rawprices['MACD'] = rawprices['EMA12'] - rawprices['EMA26']
    rawprices['MACDSignal'] = rawprices['MACD'].ewm(span=9).mean()
    rawprices['MACDHist'] = rawprices['MACD'] - rawprices['MACDSignal']
    buy, sell = [], []
    for i in range(len(rawprices['MACD'])):
        if i == 0:
            continue
        if np.isnan(rawprices['MACD'].iloc[i]) | np.isnan(rawprices['MACDSignal'].iloc[i]) | np.isnan(rawprices['MACDHist'].iloc[i]):
            print(f"{i} is nan")
            continue
        if rawprices['MACD'].iloc[i] >= rawprices['MACDSignal'].iloc[i] and rawprices['MACD'].iloc[i - 1] <= rawprices['MACDSignal'].iloc[i - 1]:
            data = {'MACD :': rawprices['MACD'].iloc[i], 'MACDSIGNAL :': rawprices['MACDSignal'].iloc[i], 'MACDHIST :': rawprices['MACDHist'].iloc[i],
                    'MACDdate :': rawprices['close_time'][i]}
            buy.update({i: data})
        elif rawprices['MACD'].iloc[i] <= rawprices['MACDSignal'].iloc[i] and rawprices['MACD'].iloc[i - 1] >= rawprices['MACDSignal'].iloc[i - 1]:
            data = {'MACD :': rawprices['MACD'].iloc[i], 'MACDSIGNAL :': rawprices['MACDSignal'].iloc[i], 'MACDHIST :': rawprices['MACDHist'].iloc[i],
                    'MACDdate :': rawprices['close_time'][i]}
            sell.update({i: data})
    print('MACD calculated')
    return rawprices, buy, sell

if __name__ == '__main__':
    pair = "BTCUSDT"
    interval = "1DAY"
    engine = sqlalchemy.create_engine('sqlite:///../history/DB/' + pair + '.db')
    rawprices = pd.read_sql('SELECT * FROM ' + pair + interval + '', engine)
    prices, buy_dates, sell_dates = MACD(rawprices)

    plt.figure(figsize=(35, 5))
    plt.plot(prices['MACD'], label='MACD', c='b', alpha=1)
    plt.plot(prices['MACDSignal'], label='MACDSignal', c='orange', alpha=1)
    plt.plot(prices['MACDHist'], label='MACDHist', c='black', alpha=1)

    plt.legend()
    plt.grid()
    plt.show()
