"""official sites for TA-Lib Technical Analysis Library- Indicator List
https://www.ta-lib.org/function.html
"""
import talib
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from slackinform import Inform
from data.coins import coin_details
from datetime import datetime
from indics import indicator
import time
import json
import sqlite3
from timeit import default_timer as timer
"""
class Plotter():
    def __init__(self, RSI=None, RSIbasedMA=None, macd=None, macdsignal=None, macdhist=None,
                 buy=None, sell=None, macdbuy=None, macdsell=None, rsibuy=None, rsisell=None,
                 currenttime=None, pricetime=None, obv=None, kauf=None, obv_ema=None, chande=None,
                 bbands=None, dmi=None, dmiplus=None, dmineg=None):
        self.RSI = RSI
        self.RSIbasedMA = RSIbasedMA
        self.macd = macd
        self.macdsignal = macdsignal
        self.macdhist = macdhist
        self.buy = buy
        self.sell = sell
        self.macdbuy = macdbuy
        self.macdsell = macdsell
        self.rsibuy = rsibuy
        self.rsisell = rsisell
        self.currenttime = currenttime
        self.pricetime = pricetime
        self.obv = obv
        self.kauf = kauf
        self.obv_ema = obv_ema
        self.chande = chande
        self.bbands = bbands
        self.dmi = dmi
        self.dmineg = dmineg
        self.dmiplus = dmiplus
    def plotRSI(self, pair, interval):
        plt.figure(figsize=(30, 5))
        plt.plot(self.RSI, label='RSI', c='r')
        plt.plot(self.RSIbasedMA, label='SMA', c='b')
        plt.scatter(list(self.rsibuy.keys()), self.RSIbasedMA.iloc[list(self.rsibuy.keys())], marker='^', color='g', s=100)
        plt.scatter(list(self.rsisell.keys()), self.RSIbasedMA.iloc[list(self.rsisell.keys())], marker='v', color='r', s=100)
        # timestamp = np.arange(np.datetime64(list(self.pricetime)[0]), np.datetime64(list(self.pricetime)[-1]), timedelta(minutes=3))
        # plt.scatter([timestamp[key] for key in list(self.rsibuy.keys())], self.RSIbasedMA.iloc[list(self.rsibuy.keys())], marker='^', color='g', s=100)
        # plt.scatter([timestamp[key] for key in list(self.rsisell.keys())], self.RSIbasedMA.iloc[list(self.rsisell.keys())], marker='v', color='r', s=100)
        # plt.yticks(np.arange(0, 100, step=10))
        # plt.xticks(timestamp)
        plt.grid()
        plt.legend()
        plt.title(pair)
        # plt.show()
        plt.savefig('./charts/RSI/' + pair + interval + plotter.gettime(self).replace(':', '_') + '.png')

    def plotMACD(self, pair, interval):
        plt.figure(figsize=(30, 5))
        plt.plot(self.macd, label='macd', c='blue')
        plt.plot(self.macdsignal, label='macdsignal', c='orange')
        plt.plot(self.macdhist, label='macdhist', c='black')
        plt.scatter(list(self.macdbuy.keys()), self.macd.iloc[list(self.macdbuy.keys())], marker='^', color='g', s=100)
        plt.scatter(list(self.macdsell.keys()), self.macd.iloc[list(self.macdsell.keys())], marker='v', color='r', s=100)
        #plt.yticks(np.arange(0, 100, step=10))
        plt.grid()
        plt.legend()
        plt.title(pair)
        # plt.show()
        plt.savefig('./charts/MACD/' + pair + interval + plotter.gettime(self).replace(':', '_') + '.png')

    def plotMACDRSI(self, pair, interval):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(30, 5))
        fig.suptitle(pair)
        # fig.figure(figsize=(30, 5))
        ax1.plot(self.macd, label='macd', c='blue')
        ax1.plot(self.macdsignal, label='macdsignal', c='orange')
        ax1.plot(self.macdhist, label='macdhist', c='black')
        ax1.scatter(list(self.buy.keys()), self.macd.iloc[list(self.buy.keys())], marker='^', color='g', s=100)
        ax1.scatter(list(self.sell.keys()), self.macd.iloc[list(self.sell.keys())], marker='v', color='r', s=100)
        ax1.grid()
        ax1.legend(loc=1)

        ax2.plot(self.RSI, label='RSI', c='r')
        ax2.plot(self.RSIbasedMA, label='SMA', c='b')
        ax2.scatter(list(self.buy.keys()), self.RSI.iloc[list(self.buy.keys())], marker='^', color='g', s=100)
        ax2.scatter(list(self.sell.keys()), self.RSI.iloc[list(self.sell.keys())], marker='v', color='r', s=100)
        ax2.set_yticks(np.arange(0, 100, step=10))
        #plt.yticks(np.arange(0, 100, step=10))
        ax2.grid()
        ax2.legend(loc=1)
        fig.savefig('./charts/MACDRSI/' + pair + interval + plotter.gettime(self).replace(':', '_') + '.png')
    def gettime(self):
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        return self.current_time
"""

class conditions():


    def MACDcond(results):
        buy = {}
        sell = {}
        for i in range(len(results.macd)):
            if i == 0:
                continue
            if np.isnan(results.macd.iloc[i]) | np.isnan(results.macdsignal.iloc[i]) | np.isnan(results.macdhist.iloc[i]):
                print(f"{i} is nan")
                continue
            if results.macd.iloc[i] >= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] <= results.macdsignal.iloc[i - 1]:
                data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i], 'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': results.pricetime.iloc[i]}
                buy.update({i: data})
            elif results.macd.iloc[i] <= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] >= results.macdsignal.iloc[i - 1]:
                data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i], 'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': results.pricetime.iloc[i]}
                sell.update({i: data})
        return buy, sell
    def RSIcond(results):
        buy = {}
        sell = {}
        for i in range(len(results.rsi)):
            if i == 0:
                continue
            if np.isnan(results.rsi.iloc[i]) | np.isnan(results.rsibasedma.iloc[i]):
                print(f"{i} is nan")
                continue
            if results.rsi.iloc[i] >= results.rsibasedma.iloc[i] and results.rsi.iloc[i - 1] <= results.rsibasedma.iloc[i - 1]:
                data = {'RSI :': results.rsi.iloc[i], 'RSIbasedMA :': results.rsibasedma.iloc[i], 'RSIdate :': results.pricetime.iloc[i]}
                buy.update({i: data})
            elif results.rsi.iloc[i] <= results.rsibasedma.iloc[i] and results.rsi.iloc[i - 1] >= results.rsibasedma.iloc[i - 1]:
                data = {'RSI :': results.rsi.iloc[i], 'RSIbasedMA :': results.rsibasedma.iloc[i], 'RSIdate :': results.pricetime.iloc[i]}
                sell.update({i: data})
        return buy, sell
    def MACDRSIcond(results):
        buy = {}
        sell = {}
        openposition = False
        for i in range(len(results.macd)):
            if i == 0:
                continue
            if np.isnan(results.macd.iloc[i]) | np.isnan(results.macdsignal.iloc[i]) | np.isnan(results.macdhist.iloc[i]):
                print(f"{i} is nan")
                continue
            if openposition == False:
                if (results.macd.iloc[i] >= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] <= results.macdsignal.iloc[i - 1] \
                    and results.rsi.iloc[i] >= results.rsibasedma.iloc[i]) \
                        or \
                    (results.rsi.iloc[i] >= results.rsibasedma.iloc[i] and results.rsi.iloc[i - 1] <= results.rsibasedma.iloc[i - 1] \
                    and results.macd.iloc[i] >= results.macdsignal.iloc[i]):
                    data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i],
                            'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': results.pricetime.iloc[i],
                            'RSI :': results.rsi.iloc[i], 'RSIbasedMA :': results.rsibasedma.iloc[i],
                            'RSIdate :': results.pricetime.iloc[i]}
                    buy.update({i: data})
                    openposition = True
            if openposition == True:
                if (results.macd.iloc[i] <= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] >= results.macdsignal.iloc[i - 1]) \
                    or \
                    (results.rsi.iloc[i] <= results.rsibasedma.iloc[i] and results.rsi.iloc[i - 1] >= results.rsibasedma.iloc[i - 1]):
                        data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i],
                                'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': results.pricetime.iloc[i],
                                'RSI :': results.rsi.iloc[i], 'RSIbasedMA :': results.rsibasedma.iloc[i],
                                'RSIdate :': results.pricetime.iloc[i]}
                        sell.update({i: data})
                        openposition = False
        return buy, sell
    def MACDRSIcondreal(results, engine):
        print("MACDRSIcondreal started")
        openposition = False
        print("position is closed")
        if openposition == False:
            while True:
                if (results.macd.iloc[-1:] >= results.macdsignal.iloc[-1:] and results.macd.iloc[-2:] <= results.macdsignal.iloc[-2:] \
                    and results.rsi.iloc[-1:] >= results.rsibasedma.iloc[-1:]) \
                        or \
                    (results.rsi.iloc[-1:] >= results.rsibasedma.iloc[-1:] and results.rsi.iloc[-2:] <= results.rsibasedma.iloc[-2:] \
                    and results.macd.iloc[-1:] >= results.macdsignal.iloc[-1:]):
                    print("buy condition has happened")
                    data = {'MACD :': results.macd.iloc[-1:], 'MACDSIGNAL :': results.macdsignal.iloc[-1:],
                            'MACDHIST :': results.macdhist.iloc[-1:], 'MACDdate :': results.pricetime.iloc[-1:],
                            'RSI :': results.rsi.iloc[-1:], 'RSIbasedMA :': results.rsibasedma.iloc[-1:],
                            'RSIdate :': results.pricetime.iloc[-1:]}
                    with open('buysell.json', 'w+') as f:
                        json.dump(data, f)
                    informer = Inform(message1=f'Buying price is {results.closeprice[-1:]}')
                    Inform.general_notify(informer)
                    openposition = True
                    break
                results = conditions.indreturner(engine)
        if openposition == True:
            print("searching for sell price")
            while True:
                time.sleep(conditions.sleepint(interval))
                newresults = conditions.indreturner(engine)
                if (newresults.macd.iloc[-1:] <= newresults.macdsignal.iloc[-1:] and newresults.macd.iloc[-2:] >= newresults.macdsignal.iloc[-2:]) \
                    or \
                    (newresults.rsi.iloc[-1:] <= newresults.rsibasedma.iloc[-1:] and newresults.rsi.iloc[-2:] >= newresults.rsibasedma.iloc[-2:]):
                    print("sell condition has happened")
                    data = {'MACD :': newresults.macd.iloc[-1:], 'MACDSIGNAL :': newresults.macdsignal.iloc[-1:],
                            'MACDHIST :': newresults.macdhist.iloc[-1:], 'MACDdate :': newresults.pricetime.iloc[-1:],
                            'RSI :': newresults.rsi.iloc[-1:], 'RSIbasedMA :': newresults.rsibasedma.iloc[-1:],
                            'RSIdate :': newresults.pricetime.iloc[-1:]}
                    informer = Inform(message1=f'Selling price is {newresults.closeprice[-1:]}')
                    Inform.general_notify(informer)
                    print("open position changed to false")
                    openposition = False
                    with open('buysell.json', 'r+') as f:
                        dic = json.load(f)
                        dic.update(data)
                    with open('buysell.json', 'w+') as f:
                        json.dump(dic, f)
                    break
        print("MACDRSIcondreal finished")
    #TODO: create a function for profits
    def profits(results):
        buy_keys = list(results.buy.keys())
        buy_prices = results.macd.iloc[list(results.buy.keys())]
        sell_keys = list(results.sell.keys())
        sell_prices = results.macd.iloc[list(results.sell.keys())]
        print()

if __name__ == '__main__':
    symbol, intervals = coin_details()
    pair = "BTCUSDT"
    interval = intervals[0]
    engine = sqlalchemy.create_engine('sqlite:///../history/DBDEV/DEVSELECTED_15JAN.db')
    # engine = sqlalchemy.create_engine('sqlite:///C:/Users/a/Desktop/DEVSELECTED_15JAN.db')
    prices = pd.read_sql('SELECT * FROM ' + pair + interval + '', engine)
    # prices = prices[-100:]
    """Does required calculations based on indicator types"""
    indicators = indicator.Indicators()
    # chart = indicator.Plotter()
    # chart.pricetime=prices['close_time']
    result = indicator.Calculate.calculator(indicators, prices)
    date = result.pricetime

    """returns buy and sell dates of indicators accordingly and plots buy/sell ticks and signals"""
    result.macdbuy, result.macdsell = conditions.MACDcond(result)
    indicator.Plotter.plotMACD(result, pair, interval)
    result.rsibuy, result.rsisell = conditions.RSIcond(result)
    indicator.Plotter.plotRSI(result, pair, interval)
    result.buy, result.sell = conditions.MACDRSIcond(result)
    indicator.Plotter.plotMACDRSI(result, pair, interval)
    # profit = conditions.profits(chart)
    """needs some amendment in slackinformer function"""
    MACD_info = Inform(message1=result)
    Inform.MACD_informer(MACD_info)
