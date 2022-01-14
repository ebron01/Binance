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

class plotter():
    def __init__(self, RSI=None, RSIbasedMA=None, macd=None, macdsignal=None, macdhist=None,
                 buy=None, sell=None, macdbuy=None, macdsell=None, rsibuy=None, rsisell=None):
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

    def plotRSI(self, pair, interval):
        plt.figure(figsize=(30, 5))
        plt.plot(self.RSI, label='RSI', c='r')
        plt.plot(self.RSIbasedMA, label='SMA', c='b')
        plt.scatter(list(self.rsibuy.keys()), self.RSIbasedMA.iloc[list(self.rsibuy.keys())], marker='^', color='g', s=100)
        plt.scatter(list(self.rsisell.keys()), self.RSIbasedMA.iloc[list(self.rsisell.keys())], marker='v', color='r', s=100)
        plt.yticks(np.arange(0, 100, step=10))
        plt.grid()
        plt.legend()
        plt.title(pair)
        # plt.show()
        plt.savefig('./charts/RSIbuysell' + pair + interval + '.png')
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
        plt.savefig('./charts/MACDbuysell' + pair + interval + '.png')
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
        fig.savefig('./charts/MACDRSI' + pair + interval + '.png')

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
                data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i], 'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': prices['close_time'][i]}
                buy.update({i: data})
            elif results.macd.iloc[i] <= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] >= results.macdsignal.iloc[i - 1]:
                data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i], 'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': prices['close_time'][i]}
                sell.update({i: data})
        return buy, sell
    def RSIcond(results):
        buy = {}
        sell = {}
        for i in range(len(results.RSI)):
            if i == 0:
                continue
            if np.isnan(results.RSI.iloc[i]) | np.isnan(results.RSIbasedMA.iloc[i]):
                print(f"{i} is nan")
                continue
            if results.RSI.iloc[i] >= results.RSIbasedMA.iloc[i] and results.RSI.iloc[i - 1] <= results.RSIbasedMA.iloc[i - 1]:
                data = {'RSI :': results.RSI.iloc[i], 'RSIbasedMA :': results.RSIbasedMA.iloc[i], 'RSIdate :': prices['close_time'][i]}
                buy.update({i: data})
            elif results.RSI.iloc[i] <= results.RSIbasedMA.iloc[i] and results.RSI.iloc[i - 1] >= results.RSIbasedMA.iloc[i - 1]:
                data = {'RSI :': results.RSI.iloc[i], 'RSIbasedMA :': results.RSIbasedMA.iloc[i], 'RSIdate :': prices['close_time'][i]}
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
                    and results.RSI.iloc[i] >= results.RSIbasedMA.iloc[i]) \
                        or \
                    (results.RSI.iloc[i] >= results.RSIbasedMA.iloc[i] and results.RSI.iloc[i - 1] <= results.RSIbasedMA.iloc[i - 1] \
                    and results.macd.iloc[i] >= results.macdsignal.iloc[i]):
                    data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i],
                            'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': prices['close_time'][i],
                            'RSI :': results.RSI.iloc[i], 'RSIbasedMA :': results.RSIbasedMA.iloc[i],
                            'RSIdate :': prices['close_time'][i]}
                    buy.update({i: data})
                    openposition = True
            if openposition == True:
                if (results.macd.iloc[i] <= results.macdsignal.iloc[i] and results.macd.iloc[i - 1] >= results.macdsignal.iloc[i - 1]) \
                    or \
                    (results.RSI.iloc[i] <= results.RSIbasedMA.iloc[i] and results.RSI.iloc[i - 1] >= results.RSIbasedMA.iloc[i - 1]):
                        data = {'MACD :': results.macd.iloc[i], 'MACDSIGNAL :': results.macdsignal.iloc[i],
                                'MACDHIST :': results.macdhist.iloc[i], 'MACDdate :': prices['close_time'][i],
                                'RSI :': results.RSI.iloc[i], 'RSIbasedMA :': results.RSIbasedMA.iloc[i],
                                'RSIdate :': prices['close_time'][i]}
                        sell.update({i: data})
                        openposition = False
        return buy, sell
    #TODO: create a function for profits
    def profits(results):
        buy_keys = list(results.buy.keys())
        buy_prices = results.macd.iloc[list(results.buy.keys())]
        sell_keys = list(results.sell.keys())
        sell_prices = results.macd.iloc[list(results.sell.keys())]
        print()

class indicators():
    def RSI(prices):
        #TODO:RSI - needs conditions, needs an informer
        """This is RSI plot, tradingview
        Default time period for RSI oscillator is 14 timestamps.
        """
        RSI = talib.RSI(prices.close_price, timeperiod=14)
        RSIbasedMA = talib.MA(RSI, timeperiod=14)
        return RSI, RSIbasedMA

    def MACD(prices):
        #TODO:MACD - needs amendment in notify
        """
        The basic bullish signal (buy sign) occurs when the MACD line (the blue line) crosses above the signal line (the orange
        line), and the basic bearish signal (sell sign) is generated when the MACD crosses below the signal line. Traders who
        attempt to profit from bullish MACD crosses that occur when the indicator is below zero should be aware that they are
        attempting to profit from a change in momentum direction, while the moving averages are still suggesting that the
        security could experience a short-term sell-off. This bullish crossover can often correctly predict the reversal in the
        trend, as shown below, but it is often considered riskier than if the MACD were above zero.
        https://www.investopedia.com/terms/m/macd.asp
        macd=12-Period EMA − 26-Period EMA of close prices
        macdsignal=9-Period EMA of macd not close prices
        macdhist=macd-macdsignal
        Limitations:  A slowdown in the momentum—sideways movement or slow trending movement—of the price will cause
        the MACD to pull away from its prior extremes and gravitate toward the zero lines even in the absence of a true
        reversal.
        MACD is a lagging indicator.All of the data used in MACD is based on the historical price action of the stock.
        """
        macd, macdsignal, macdhist = talib.MACD(prices.close_price, fastperiod=12, slowperiod=26, signalperiod=9)
        return macd, macdsignal, macdhist

if __name__ == '__main__':
    symbol, intervals = coin_details()

    pair = "ETHUSDT"
    interval = intervals[0]
    engine = sqlalchemy.create_engine('sqlite:///../history/DBDEV/DEVSELECTED.db')
    chart = plotter()
    prices = pd.read_sql('SELECT * FROM ' + pair + interval + '', engine)

    """Does required calculations based on indicator types"""
    chart.RSI, chart.RSIbasedMA = indicators.RSI(prices)
    chart.macd, chart.macdsignal, chart.macdhist = indicators.MACD(prices)
    """returns buy and sell dates of indicators accordingly and plots buy/sell ticks and signals"""
    chart.macdbuy, chart.macdsell = conditions.MACDcond(chart)
    plotter.plotMACD(chart, pair, interval)
    chart.rsibuy, chart.rsisell = conditions.RSIcond(chart)
    plotter.plotRSI(chart, pair, interval)
    chart.buy, chart.sell = conditions.MACDRSIcond(chart)
    plotter.plotMACDRSI(chart, pair, interval)

    # profit = conditions.profits(chart)

    """needs some amendment in slackinformer function"""
    MACD_info = Inform(message1=chart)
    Inform.MACD_informer(MACD_info)







