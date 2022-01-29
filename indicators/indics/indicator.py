import talib
from talib import MA_Type
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json
import pandas as pd
import time

def gettime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

class Indicators():
    def __init__(self, rsi=None, rsibasedma=None, macd=None, macdsignal=None, macdhist=None,
                 buy=None, sell=None, macdbuy=None, macdsell=None, rsibuy=None, rsisell=None,
                 currenttime=None, pricetime=None, obv=None, kauf=None, obv_ema=None, chande=None,
                 bbandupper=None, bbandmiddle=None, bbandlittle=None, dmi=None, dmiplus=None, dmineg=None, closeprice=None):
        self.rsi = rsi
        self.rsibasedma = rsibasedma
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
        self.bbandupper = bbandupper
        self.bbandmiddle = bbandmiddle
        self.bbandlittle = bbandlittle
        self.dmi = dmi
        self.dmineg = dmineg
        self.dmiplus = dmiplus
        self.closeprice = closeprice
    def keys(self):
        return [self.rsi, self.rsibasedma, self.macd, self.macdsignal, self.macdhist,
                 self.buy, self.sell, self.macdbuy, self.macdsell, self.rsibuy, self.rsisell,
                 self.currenttime, self.pricetime, self.obv, self.kauf, self.obv_ema, self.chande,
                 self.bbandupper, self.bbandmiddle, self.bbandlittle, self.dmi, self.dmiplus, self.dmineg, self.closeprice]
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

    def OBV(prices):
        """
        Granville went on to explain his theory by stating that when volume increased or decreased dramatically without
        any significant change in the issue's price, then at some point the price would "spring" upward or downward.
        It appears that as institutions (pension funds, investment funds, and large trading houses) begin to buy into an
        issue that retail investors are still selling, volume increases as the price is still slightly falling or
        leveling out.
        Over a period of time, volume begins to drive the price upward and the converse then begins to take over as the
        institutions begin to sell their position and the retail investors begin again to accumulate their positions.
        """
        obv = talib.OBV(prices.close_price, prices.volume)
        obv_ema = talib.EMA(obv, timeperiod=50)
        return obv, obv_ema

    def KAUF(prices):
        kauf= talib.KAMA(prices.close_price, timeperiod=21)
        return kauf

    def Chande(prices):
        """
        A security is deemed to be overbought when the Chande momentum oscillator is above +50 and oversold when it is
        below -50. Many technical traders add a 10-period moving average to this oscillator to act as a signal line.
        The oscillator generates a bullish signal when it crosses above the moving average and a bearish signal when it
        drops below the moving average.
        The oscillator can be used as a confirmation signal when it crosses above or below the 0 line. For example, if
        the 50-day moving average crosses above the 200-day moving average (golden cross), a buy signal is confirmed
        when the Chande momentum oscillator crosses above 0, predicting prices are headed higher.
        """
        chande = talib.CMO(prices.close_price, timeperiod=9)
        return chande

    def BollingerBands(prices):
        """
        https://www.investopedia.com/terms/b/bollingerbands.asp
        A Bollinger Band® is a technical analysis tool defined by a set of trendlines plotted two standard deviations
        (positively and negatively) away from a simple moving average (SMA) of a security's price, but which can be
        adjusted to user preferences.
        The upper and lower bands are typically 2 standard deviations +/- from a 20-day simple moving average,
        but they can be modified.
        Bollinger Bands® are a highly popular technique. Many traders believe the closer the prices move to the upper
        band, the more overbought the market,the closer the prices move to the lower band, the more oversold the market.
        """
        # upper, middle, lower = talib.BBANDS(prices.close_price,matype = MA_Type.T3) #defult option
        upper, middle, lower = talib.BBANDS(prices.close_price, timeperiod=20, nbdevup=2, nbdevdn=2)
        return upper, middle, lower

    def DMI(prices):
        """
        The directional movement indicator (also known as the directional movement index or DMI) is a valuable tool for
        assessing price direction and strength.

        """
        adx = talib.ADX(prices.high_price, prices.low_price, prices.close_price, timeperiod=14)
        minus = talib.MINUS_DI(prices.high_price, prices.low_price, prices.close_price, timeperiod=14)
        plus = talib.PLUS_DI(prices.high_price, prices.low_price, prices.close_price, timeperiod=14)
        return adx, minus, plus

    def pricetime(prices):
        return prices.close_time
    def price(prices):
        return prices.close_price

class Calculate(Indicators):
    # def job(scheduler, time, engine, symbol, intervals):
    #     if intervals == '30MINUTES':
    #         scheduler.add_job(Calculate.indreturner, 'interval', minutes=30, start_date=time,
    #                       args=[engine, symbol, intervals])
    #     # elif intervals == '1HOUR':
    #     #     scheduler.add_job(Calculate.indreturner, 'interval', hours=1, start_date=time,
    #     #                   args=[engine, symbol, intervals])
    #     # elif intervals == '4HOUR':
    #     #     scheduler.add_job(Calculate.indreturner, 'interval', hours=4, start_date=time,
    #     #                   args=[engine, symbol, intervals])
    #     # elif intervals == '1DAY':
    #     #     scheduler.add_job(Calculate.indreturner, 'interval', hours=24, start_date=time,
    #     #                   args=[engine, symbol, intervals])
    def calculator(self, prices):
        self.rsi, self.rsibasedma = Indicators.RSI(prices)
        self.macd, self.macdsignal, self.macdhist = Indicators.MACD(prices)
        self.obv, self.obv_ema = Indicators.OBV(prices) #different obv and ema but obv-ema of the chart and the function is same.
        self.kauf = Indicators.KAUF(prices) #almost the same
        self.chande = Indicators.Chande(prices)
        self.bbandupper, self.bbandmiddle, self.bbandlittle = Indicators.BollingerBands(prices)
        self.dmi, self.dmineg, self.dmiplus = Indicators.DMI(prices)
        self.pricetime = Indicators.pricetime(prices)
        self.closeprice = Indicators.price(prices)
        return self
    def sleepint(interval):
        if interval == "30MINUTE":
            sleeptime = 30 * 60
        elif interval == "1HOUR":
            sleeptime = 60 * 60
        elif interval == "4HOUR":
            sleeptime = 4 * 60 * 60
        elif interval == "1DAY":
            sleeptime = 24 * 60 * 60
        elif interval == "1WEEK":
            sleeptime = 7 * 24 * 60 * 60
        elif interval == "1MONTH":
            sleeptime = 30 * 7 * 24 * 60 * 60
        return sleeptime
    def indreturner(engine, symbol, intervals):
        """this sql returns the last price"""
        # # updated = {}
        # # for sym in symbol:
        #     for interval in intervals:
        #         updatedprices = pd.read_sql('SELECT * FROM ' + sym + interval + ' ORDER BY close_time DESC LIMIT 1', engine)
        #         updated.update({sym + interval : updatedprices})
        updated = pd.read_sql('SELECT * FROM ' + symbol + intervals + ' ORDER BY close_time DESC LIMIT 2', engine)
        return updated
    def MACDRSIcondreal(engine, symbol, intervals):
        print("MACDRSIcondreal started")
        """returns last two timestamps with descending order"""
        results = Calculate.indreturner(engine, symbol, intervals)
        print("indicators for the starting position is calculated")
        # scheduler = BlockingScheduler()
        openposition = False
        print("position is closed")
        if openposition == False:
            while True:
                print("searching for buy price")
                if (results.macd.iloc[0] >= results.macdsignal.iloc[0] and results.macd.iloc[1] <= results.macdsignal.iloc[1] \
                    and results.rsi.iloc[0] >= results.rsibasedma.iloc[0]) \
                        or \
                    (results.rsi.iloc[0] >= results.rsibasedma.iloc[0] and results.rsi.iloc[1] <= results.rsibasedma.iloc[1] \
                    and results.macd.iloc[0] >= results.macdsignal.iloc[0])\
                        or \
                    (results.rsi.iloc[0] >= results.rsibasedma.iloc[0] and results.macd.iloc[0] >= results.macdsignal.iloc[0]):
                    print("buy condition has happened")
                    data = {'buy': { 'MACD :': results.macd.iloc[0], 'MACDSIGNAL :': results.macdsignal.iloc[0],
                            'MACDHIST :': results.macdhist.iloc[0], 'MACDdate :': results.pricetime.iloc[0],
                            'RSI :': results.rsi.iloc[0], 'RSIbasedMA :': results.rsibasedma.iloc[0],
                            'RSIdate :': results.pricetime.iloc[0]}}
                    with open('./buysell/buysell1.json', 'w') as f:
                        json.dump(data, f)
                        f.write('\n')
                    # informer = Inform(message1=f'Buying price is {results.closeprice[-1:]}')
                    # Inform.general_notify(informer)
                    print("open position changed to true")
                    openposition = True
                    break
                print(f'sleep started at: {gettime()}')
                time.sleep(Calculate.sleepint(intervals))
                print(f'sleep ended at: {gettime()}')
                print('getting new values')
                results = Calculate.indreturner(engine, symbol, intervals)
        if openposition == True:
            while True:
                print("searching for sell price")
                print(f'sleep started at: {gettime()}')
                time.sleep(Calculate.sleepint(intervals))
                print(f'sleep ended at: {gettime()}')
                print('getting new values')
                newresults = Calculate.indreturner(engine, symbol, intervals)
                print('got new values')
                if (newresults.macd.iloc[0] <= newresults.macdsignal.iloc[0] and newresults.macd.iloc[1] >= newresults.macdsignal.iloc[1]) \
                    or \
                    (newresults.rsi.iloc[0] <= newresults.rsibasedma.iloc[0] and newresults.rsi.iloc[1] >= newresults.rsibasedma.iloc[1]):
                    print("sell condition has happened")
                    newdata = {'sell' : {'MACD :': newresults.macd.iloc[0], 'MACDSIGNAL :': newresults.macdsignal.iloc[0],
                            'MACDHIST :': newresults.macdhist.iloc[0], 'MACDdate :': newresults.pricetime.iloc[0],
                            'RSI :': newresults.rsi.iloc[0], 'RSIbasedMA :': newresults.rsibasedma.iloc[0],
                            'RSIdate :': newresults.pricetime.iloc[0]}}
                    # informer = Inform(message1=f'Selling price is {newresults.closeprice[-1:]}')
                    # Inform.general_notify(informer)
                    print("open position changed to false")
                    openposition = False
                    with open('./buysell/buysell.json', 'a') as f:
                        json.dump(newdata, f)
                        f.write('\n')
                    break
                print('sell condition is not activated yet')
                data = {'MACD :': newresults.macd.iloc[0], 'MACDSIGNAL :': newresults.macdsignal.iloc[0],
                        'MACDHIST :': newresults.macdhist.iloc[0], 'MACDdate :': newresults.pricetime.iloc[0],
                        'RSI :': newresults.rsi.iloc[0], 'RSIbasedMA :': newresults.rsibasedma.iloc[0],
                        'RSIdate :': newresults.pricetime.iloc[0]}
                print(data)
        print("MACDRSIcondreal finished")

class Plotter(Indicators):
    def plotRSI(self, pair, interval):
        plt.figure(figsize=(30, 5))
        #TODO: carefully check range(len(self.rsi)) and range(len(self.rsi)) part.
        plt.plot(range(len(self.rsi)), self.rsi, label='RSI', c='r')
        plt.plot(range(len(self.rsi)), self.rsibasedma, label='SMA', c='b')
        plt.scatter(list(self.rsibuy.keys()), self.rsibasedma.iloc[list(self.rsibuy.keys())], marker='^', color='g', s=100)
        plt.scatter(list(self.rsisell.keys()), self.rsibasedma.iloc[list(self.rsisell.keys())], marker='v', color='r', s=100)
        # timestamp = np.arange(np.datetime64(list(self.pricetime)[0]), np.datetime64(list(self.pricetime)[-1]), timedelta(minutes=3))
        # plt.scatter([timestamp[key] for key in list(self.rsibuy.keys())], self.RSIbasedMA.iloc[list(self.rsibuy.keys())], marker='^', color='g', s=100)
        # plt.scatter([timestamp[key] for key in list(self.rsisell.keys())], self.RSIbasedMA.iloc[list(self.rsisell.keys())], marker='v', color='r', s=100)
        # plt.yticks(np.arange(0, 100, step=10))
        # plt.xticks(timestamp)
        plt.grid()
        plt.legend()
        plt.title(pair)
        # plt.show()
        plt.savefig('./charts/RSI/' + pair + interval + Plotter.gettime(self).replace(':', '_') + '.png')

    def plotMACD(self, pair, interval):
        plt.figure(figsize=(30, 5))
        plt.plot(range(len(self.macd)), self.macd, label='macd', c='blue')
        plt.plot(range(len(self.macdsignal)), self.macdsignal, label='macdsignal', c='orange')
        plt.plot(range(len(self.macdhist)), self.macdhist, label='macdhist', c='black')
        plt.scatter(list(self.macdbuy.keys()), self.macd.iloc[list(self.macdbuy.keys())], marker='^', color='g', s=100)
        plt.scatter(list(self.macdsell.keys()), self.macd.iloc[list(self.macdsell.keys())], marker='v', color='r', s=100)
        #plt.yticks(np.arange(0, 100, step=10))
        plt.grid()
        plt.legend()
        plt.title(pair)
        # plt.show()
        plt.savefig('./charts/MACD/' + pair + interval + Plotter.gettime(self).replace(':', '_') + '.png')

    def plotMACDRSI(self, pair, interval):
        fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(30, 5))
        fig.suptitle(pair)
        # fig.figure(figsize=(30, 5))
        ax1.plot(range(len(self.macdhist)), self.macd, label='macd', c='blue')
        ax1.plot(range(len(self.macdsignal)), self.macdsignal, label='macdsignal', c='orange')
        ax1.plot(range(len(self.macdhist)), self.macdhist, label='macdhist', c='black')
        ax1.scatter(list(self.buy.keys()), self.macd.iloc[list(self.buy.keys())], marker='^', color='g', s=100)
        ax1.scatter(list(self.sell.keys()), self.macd.iloc[list(self.sell.keys())], marker='v', color='r', s=100)
        ax1.grid()
        ax1.legend(loc=1)

        ax2.plot(range(len(self.rsi)), self.rsi, label='RSI', c='r')
        ax2.plot(range(len(self.rsibasedma)), self.rsi, label='SMA', c='b')
        ax2.scatter(list(self.buy.keys()), self.rsi.iloc[list(self.buy.keys())], marker='^', color='g', s=100)
        ax2.scatter(list(self.sell.keys()), self.rsi.iloc[list(self.sell.keys())], marker='v', color='r', s=100)
        ax2.set_yticks(np.arange(0, 100, step=10))
        #plt.yticks(np.arange(0, 100, step=10))
        ax2.grid()
        ax2.legend(loc=1)
        fig.savefig('./charts/MACDRSI/' + pair + interval + Plotter.gettime(self).replace(':', '_') + '.png')

    def gettime(self):
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        return self.current_time

