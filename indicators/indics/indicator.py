import talib
from talib import MA_Type
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class Indicators():
    def __init__(self, rsi=None, rsibasedma=None, macd=None, macdsignal=None, macdhist=None,
                 buy=None, sell=None, macdbuy=None, macdsell=None, rsibuy=None, rsisell=None,
                 currenttime=None, pricetime=None, obv=None, kauf=None, obv_ema=None, chande=None,
                 bbands=None, dmi=None, dmiplus=None, dmineg=None):
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
        self.bbands = bbands
        self.dmi = dmi
        self.dmineg = dmineg
        self.dmiplus = dmiplus

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

class Calculate(Indicators):
    def calculator(self, prices):
        self.rsi, self.rsibasedma = Indicators.RSI(prices)
        self.macd, self.macdsignal, self.macdhist = Indicators.MACD(prices)
        self.obv, self.obv_ema = Indicators.OBV(prices) #different obv and ema but obv-ema of the chart and the function is same.
        self.kauf = Indicators.KAUF(prices) #almost the same
        self.chande = Indicators.Chande(prices)
        self.bbandupper, self.bbandmiddle, self.bbandlittle = Indicators.BollingerBands(prices)
        self.dmi, self.dmineg, self.dmiplus = Indicators.DMI(prices)
        self.pricetime = Indicators.pricetime(prices)
        return self

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

