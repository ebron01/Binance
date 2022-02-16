import talib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json
import pandas as pd
pd.set_option('display.max_columns', 10)
import time
from slackinform import Inform

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
    def alternatesleep(closetime, symbol, intervals, engine):
        while True:
            result = Calculate.indreturner(engine, symbol, intervals)
            if closetime < result.close_time.iloc[0]:
                print("found a new entry at the db")
                closetime = result.close_time.iloc[0]
                break
            else:
                if gettime().split(' ')[1].split(':')[1] == '01' or gettime().split(' ')[1].split(':')[1] == '31':
                    print('due to database entry will sleep for extra 2 minutes')
                    time.sleep(120)
                    print(f'continue at {gettime()}')
                print(f"sleeping at {gettime()} for 1 minutes")
                time.sleep(60)
        return closetime, result
    def localconverter(pricetime):
        return str(pd.to_datetime(pricetime) + pd.to_timedelta('04:30:00'))
    def indreturner(engine, symbol, intervals):
        """this sql returns the last price"""
        # # updated = {}
        # # for sym in symbol:
        #     for interval in intervals:
        #         updatedprices = pd.read_sql('SELECT * FROM ' + sym + interval + ' ORDER BY close_time DESC LIMIT 1', engine)
        #         updated.update({sym + interval : updatedprices})
        # connection = sqlite3.connect('/mnt/e/wsl/e/Binance/history/DBDEV/DEVSELECTED_15JAN.db')  # creates a new database if there is none.
        # cursor = connection.cursor()
        updated = pd.read_sql('SELECT * FROM ' + symbol + intervals + ' ORDER BY close_time DESC LIMIT 2', engine)
        # updated = cursor.execute('SELECT * FROM ' + symbol + intervals + ' ORDER BY close_time DESC LIMIT 2')
        return updated
    def MACDRSIcondreal(engine, symbol, intervals, path):
        try:
            # print("MACDRSIcondreal started")
            informer = Inform(message1=f'{symbol}-{intervals} started at {gettime()}')
            Inform.general_notify(informer)
            # """returns last two timestamps with descending order"""
            # results = Calculate.indreturner(engine, symbol, intervals)
            # print("indicators for the starting position is calculated")
            openposition = False
            print("position is closed")
            while True:
                """returns last two timestamps with descending order"""
                results = Calculate.indreturner(engine, symbol, intervals)
                print("indicators for the starting position is calculated")
                data = {}
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
                            print(f'buy localtime: {Calculate.localconverter(results.pricetime.iloc[0])}, buy_timestamp: {results.pricetime.iloc[0]}, buy_price: {results.close_price.iloc[0]}')
                            # data = {'buy': { 'MACD :': results.macd.iloc[0], 'MACDSIGNAL :': results.macdsignal.iloc[0],
                            #         'MACDHIST :': results.macdhist.iloc[0], 'MACDdate :': results.pricetime.iloc[0],
                            #         'RSI :': results.rsi.iloc[0], 'RSIbasedMA :': results.rsibasedma.iloc[0],
                            #         'RSIdate :': results.pricetime.iloc[0]}}
                            # data = {'buy_price' : results.close_price.iloc[0], 'buy_timestamp' : results.close_time.iloc[0]}
                            # with open('./buysell/buysell'+ symbol + intervals +'.json', 'w') as f:
                            #     json.dump(data, f)
                            #     f.write('\n')
                            # informer = Inform(message1=f'BUY: {symbol}-{intervals}, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, Localtime: {Calculate.localconverter(results.pricetime.iloc[0])}')
                            # Inform.general_notify(informer)
                            print("open position changed to true")
                            openposition = True
                            break
                        # print(f'sleep started at: {gettime()}')
                        # time.sleep(Calculate.sleepint(intervals))
                        # print(f'sleep ended at: {gettime()}')
                        # print('getting new values')
                        # results = Calculate.indreturner(engine, symbol, intervals)
                        print("trying alternate sleep started-buy")
                        closetime, results = Calculate.alternatesleep(results.close_time[0], symbol, intervals, engine)
                        print("trying alternate sleep finished-buy ")
                        print('got new values')
                if openposition == True:
                    closetime = results.close_time[0]
                    while True:
                        print("searching for sell price")
                        # print(f'sleep started at: {gettime()}')
                        # time.sleep(Calculate.sleepint(intervals))
                        # print(f'sleep ended at: {gettime()}')
                        # print('getting new values')
                        # newresults = Calculate.indreturner(engine, symbol, intervals)
                        print("trying alternate sleep started-sell")
                        # newresults = Calculate.alternatesleep(results.close_time[0], symbol, intervals, engine)
                        closetime, newresults = Calculate.alternatesleep(closetime, symbol, intervals, engine)
                        print("trying alternate sleep finished-sell")
                        print('got new values')
                        if (newresults.macd.iloc[0] <= newresults.macdsignal.iloc[0] and newresults.macd.iloc[1] >= newresults.macdsignal.iloc[1]) \
                            or \
                            (newresults.rsi.iloc[0] <= newresults.rsibasedma.iloc[0] and newresults.rsi.iloc[1] >= newresults.rsibasedma.iloc[1]):
                            print("sell condition has happened")
                            print(f'sell localtime: {Calculate.localconverter(newresults.pricetime.iloc[0])},sell_timestamp: {newresults.pricetime.iloc[0]}, sell_price: {newresults.close_price.iloc[0]}')
                            # newdata = {'sell' : {'MACD :': newresults.macd.iloc[0], 'MACDSIGNAL :': newresults.macdsignal.iloc[0],
                            #         'MACDHIST :': newresults.macdhist.iloc[0], 'MACDdate :': newresults.pricetime.iloc[0],
                            #         'RSI :': newresults.rsi.iloc[0], 'RSIbasedMA :': newresults.rsibasedma.iloc[0],
                            #         'RSIdate :': newresults.pricetime.iloc[0]}}
                            # informer = Inform(message1=f'Selling price is {newresults.closeprice[-1:]}')
                            # Inform.general_notify(informer)
                            informer = Inform(message1=f'BUY: {symbol}-{intervals}, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, Localtime: {Calculate.localconverter(results.pricetime.iloc[0])},SELL: {symbol}-{intervals}, Price: {newresults.close_price.iloc[0]}, UTC Time: {newresults.pricetime.iloc[0]}, Localtime: {Calculate.localconverter(newresults.pricetime.iloc[0])}')
                            Inform.general_notify(informer)
                            print("open position changed to false")
                            openposition = False
                            profit = (newresults.close_price.iloc[0] - results.close_price.iloc[0]) / results.close_price.iloc[0]
                            data.update({newresults.pricetime.iloc[0]:
                                        {'buy_timestamp': results.pricetime.iloc[0], 'buy_price': results.close_price.iloc[0],
                                         'sell_timestamp': newresults.pricetime.iloc[0], 'sell_price': newresults.close_price.iloc[0],
                                         'profit': profit * 100, 'difference': newresults.close_price.iloc[0] - results.close_price.iloc[0]}})
                            # with open('./buysell/buysell' + symbol + intervals + '.json', 'a') as f:
                            with open(path + 'rsimacd/' + symbol + intervals +'.json', 'a') as f:
                                json.dump(data, f)
                                f.write('\n')
                            break
                        print('sell condition is not activated yet')
                print("MACDRSIcondreal finished")
        except Exception as e:
            print(e)
    def RSI50(engine, symbol, intervals, path, kauf, pc):
        try:
            # print("MACDRSIcondreal started")
            if kauf:
                informer = Inform(message1=f'{pc}-{symbol}-{intervals}-RSI50kauf started at {gettime()} localtime')
            else:
                informer = Inform(message1=f'{pc}-{symbol}-{intervals}-RSI50 started at {gettime()} localtime')
            Inform.general_notify(informer)
            # """returns last two timestamps with descending order"""
            # results = Calculate.indreturner(engine, symbol, intervals)
            # print("indicators for the starting position is calculated")
            openposition = False
            print("position is closed")
            while True:
                """returns last two timestamps with descending order"""
                results = Calculate.indreturner(engine, symbol, intervals)
                print("indicators for the starting position is calculated")
                data = {}
                if openposition == False:
                    while True:
                        print("searching for buy price")
                        if kauf:
                            condition_buy = (results.rsi.iloc[0] >= 50) and (results.close_price.iloc[0] > results.kauf.iloc[0])
                            informer = Inform(
                                message1=f'{pc}-BUY: {symbol}-{intervals}-RSI50-Kauf, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]} RSI Value: {results.rsi.iloc[0]}, KAUF Value: {results.kauf.iloc[0]}')
                            filename = path + 'rsi50kauf/' + symbol + intervals + '_rsi50kauf.json'
                        else:
                            condition_buy = (results.rsi.iloc[0] >= 50)
                            informer = Inform(
                                message1=f'{pc}-BUY: {symbol}-{intervals}-RSI50, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, RSI Value: {results.rsi.iloc[0]}')
                            filename = path + 'rsi50/' + symbol + intervals + '_rsi50.json'
                        if condition_buy:
                            print("buy condition has happened")
                            print(f'buy localtime: {Calculate.localconverter(results.pricetime.iloc[0])}, \
                                  buy_timestamp: {results.pricetime.iloc[0]}, buy_price: {results.close_price.iloc[0]}\
                                  buy_rsi: {results.rsi.iloc[0]}')
                            # data = {'buy': { 'MACD :': results.macd.iloc[0], 'MACDSIGNAL :': results.macdsignal.iloc[0],
                            #         'MACDHIST :': results.macdhist.iloc[0], 'MACDdate :': results.pricetime.iloc[0],
                            #         'RSI :': results.rsi.iloc[0], 'RSIbasedMA :': results.rsibasedma.iloc[0],
                            #         'RSIdate :': results.pricetime.iloc[0]}}
                            # data = {'buy_price' : results.close_price.iloc[0], 'buy_timestamp' : results.close_time.iloc[0]}
                            # with open('./buysell/buysell'+ symbol + intervals +'.json', 'w') as f:
                            #     json.dump(data, f)
                            #     f.write('\n')
                            Inform.general_notify(informer)
                            print("open position changed to true")
                            openposition = True
                            break
                        # print(f'sleep started at: {gettime()}')
                        # time.sleep(Calculate.sleepint(intervals))
                        # print(f'sleep ended at: {gettime()}')
                        # print('getting new values')
                        # results = Calculate.indreturner(engine, symbol, intervals)
                        print("trying alternate sleep started-buy")
                        closetime, results = Calculate.alternatesleep(results.close_time[0], symbol, intervals, engine)
                        print("trying alternate sleep finished-buy ")
                        print('got new values')
                if openposition == True:
                    closetime = results.close_time[0]
                    while True:
                        print("searching for sell price")
                        # print(f'sleep started at: {gettime()}')
                        # time.sleep(Calculate.sleepint(intervals))
                        # print(f'sleep ended at: {gettime()}')
                        # print('getting new values')
                        # newresults = Calculate.indreturner(engine, symbol, intervals)
                        print("trying alternate sleep started-sell")
                        # newresults = Calculate.alternatesleep(results.close_time[0], symbol, intervals, engine)
                        closetime, newresults = Calculate.alternatesleep(closetime, symbol, intervals, engine)
                        print("trying alternate sleep finished-sell")
                        print('got new values')
                        if (newresults.rsi.iloc[0] < 50):
                            print("sell condition has happened")
                            print(
                                f'sell localtime: {Calculate.localconverter(newresults.pricetime.iloc[0])},\
                                sell_timestamp: {newresults.pricetime.iloc[0]}, sell_price: {newresults.close_price.iloc[0]}, \
                                rsi: {newresults.rsi.iloc[0]}')
                            # newdata = {'sell' : {'MACD :': newresults.macd.iloc[0], 'MACDSIGNAL :': newresults.macdsignal.iloc[0],
                            #         'MACDHIST :': newresults.macdhist.iloc[0], 'MACDdate :': newresults.pricetime.iloc[0],
                            #         'RSI :': newresults.rsi.iloc[0], 'RSIbasedMA :': newresults.rsibasedma.iloc[0],
                            #         'RSIdate :': newresults.pricetime.iloc[0]}}
                            # informer = Inform(message1=f'Selling price is {newresults.closeprice[-1:]}')
                            # Inform.general_notify(informer)
                            informer = Inform(
                                message1=f'{pc}-BUY: {symbol}-{intervals}, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, SELL: Price: {newresults.close_price.iloc[0]}, UTC Time: {newresults.pricetime.iloc[0]}, RSI: {newresults.rsi.iloc[0]}')
                            Inform.general_notify(informer)
                            print("open position changed to false")
                            openposition = False
                            profit = (newresults.close_price.iloc[0] - results.close_price.iloc[0]) / \
                                     results.close_price.iloc[0]
                            data.update({newresults.pricetime.iloc[0]:
                                             {'buy_timestamp': results.pricetime.iloc[0],
                                              'buy_price': results.close_price.iloc[0],
                                              'buy_rsi': results.rsi.iloc[0],
                                              'sell_timestamp': newresults.pricetime.iloc[0],
                                              'sell_price': newresults.close_price.iloc[0],
                                              'sell_rsi': newresults.rsi.iloc[0],
                                              'profit percentage': profit * 100,
                                              'difference': newresults.close_price.iloc[0] - results.close_price.iloc[
                                                  0]}})
                            # with open('./buysell/buysell' + symbol + intervals + '.json', 'a') as f:
                            with open(filename, 'a') as f:
                                json.dump(data, f)
                                f.write('\n')
                            break
                        print('sell condition is not activated yet')
                print("MACDRSIcondreal finished")
        except Exception as e:
            if kauf:
                informer = Inform(message1=f'{pc}-EXCEPTION-RSI50Kauf for {symbol}-{intervals} as {e}')
            else:
                informer = Inform(message1=f'{pc}-EXCEPTION-RSI50 for {symbol}-{intervals} as {e}')
            Inform.general_notify(informer)
            print(e)
    def RSI50autobuy(engine, symbol, interval, client, assetQty, kauf, pc):
        try:
            remaining_fund = assetQty
            if kauf:
                informer = Inform(
                    message1=f'{pc}-Real time buy for {symbol}-{interval}-RSI50kauf started at {gettime()} localtime')
            else:
                informer = Inform(
                    message1=f'{pc}-Real time buy for {symbol}-{interval}-RSI50 started at {gettime()} localtime')
            Inform.general_notify(informer)
            openposition = False
            print("position is closed")
            """returns last two timestamps with descending order"""
            results = Calculate.indreturner(engine, symbol, interval)
            print("indicators for the starting position is calculated")
            while True:
                if openposition == False:
                    if kauf:
                        condition_buy = (results.rsi.iloc[0] >= 50) and (
                                results.close_price.iloc[0] > results.kauf.iloc[0])
                    else:
                        condition_buy = (results.rsi.iloc[0] >= 50)
                    while True:
                        assetQty = float(round(remaining_fund, 8))
                        print("searching for buy price")
                        if condition_buy:
                            if kauf:
                                informer = Inform(
                                    message1=f'{pc}-real time buy done. BUY: {symbol}-{interval}-RSI50-Kauf, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, RSI Value: {results.rsi.iloc[0]}, KAUF Value: {results.kauf.iloc[0]}')
                            else:
                                informer = Inform(
                                    message1=f'{pc}-real time buy done. BUY: {symbol}-{interval}-RSI50, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, RSI Value: {results.rsi.iloc[0]}')
                            print("buy condition has happened")
                            print(f'buy localtime: {Calculate.localconverter(results.pricetime.iloc[0])}, \
                                  buy_timestamp: {results.pricetime.iloc[0]}, buy_price: {results.close_price.iloc[0]}\
                                  buy_rsi: {results.rsi.iloc[0]}')
                            order = client.create_order(symbol=symbol,
                                                        side='BUY',
                                                        type='MARKET',
                                                        quoteOrderQty=assetQty)
                            qt = order['executedQty']
                                                        #quantity=qty
                            # informer = Inform(message1=f'BUY: {symbol}-{interval}, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, QT: {assetQty} USDT')
                            Inform.general_notify(informer)
                            print("open position changed to true")
                            openposition = True
                            break
                        print("trying alternate sleep started-buy")
                        closetime, results = Calculate.alternatesleep(results.close_time[0], symbol, interval, engine)
                        print("trying alternate sleep finished-buy ")
                        print('got new values')
                if openposition == True:
                    closetime = results.close_time[0]
                    while True:
                        print("searching for sell price")
                        print("trying alternate sleep started-sell")
                        closetime, newresults = Calculate.alternatesleep(closetime, symbol, interval, engine)
                        print("trying alternate sleep finished-sell")
                        print('got new values')
                        if (newresults.rsi.iloc[0] < 50):
                            print("sell condition has happened")
                            print(
                                f'sell localtime: {Calculate.localconverter(newresults.pricetime.iloc[0])},\
                                sell_timestamp: {newresults.pricetime.iloc[0]}, sell_price: {newresults.close_price.iloc[0]}, \
                                rsi: {newresults.rsi.iloc[0]}')
                            order = client.create_order(symbol=symbol,
                                                        side='SELL',
                                                        type='MARKET',
                                                        quantity=qt)
                            informer = Inform(
                                message1=f'{pc}-BUY: {symbol}-{interval} real money, Price: {results.close_price.iloc[0]}, UTC Time: {results.pricetime.iloc[0]}, SELL: Price: {newresults.close_price.iloc[0]}, UTC Time: {newresults.pricetime.iloc[0]}')
                            Inform.general_notify(informer)
                            print("open position changed to false")
                            openposition = False
                            remaining_fund = float(qt) * float(order['fills'][0]['price'])
                            print("realtime buy-sell finished")
                            break
                        print('sell condition is not activated yet')
        except Exception as e:
            informer = Inform(
                message1=f'{pc}-EXCEPTION-RSI50KAUFreal: for {symbol}-{interval} as {e}')
            Inform.general_notify(informer)
            print(e)
    def RSI50backtest(engine, symbol, intervals, path, kauf):
        # results = pd.read_sql("SELECT * FROM " + symbol + intervals + " WHERE close_time BETWEEN '2021-07-27 23:59:59.999000' AND '2022-02-02 23:59:59.999000'", engine)
        results = pd.read_sql("SELECT * FROM " + symbol + intervals + " WHERE close_time BETWEEN '2021-07-27 23:59:59.999000' AND strftime('%Y-%m-%d %H-%M-%f', 'now')", engine)
        # results = pd.read_sql("SELECT * FROM " + symbol + intervals + " WHERE close_time BETWEEN '2021-02-05 23:59:59.999000' AND strftime('%Y-%m-%d %H-%M-%f', 'now')",
        #                         engine)
        counter = 0
        price = 1000
        for i in range(len(results)):
            data = {}
            try:
                if counter == 0:
                    if kauf:
                        condition_buy = (results.iloc[i].rsi >= 50) and (results.iloc[i].close_price > results.iloc[i].kauf)
                    else:
                        condition_buy = (results.iloc[i].rsi >= 50) and (results.iloc[i].macd >=0)
                    if condition_buy:
                        counter = 1
                        buy_timestamp = results.iloc[i].pricetime
                        buy_price = results.iloc[i].close_price
                        buy_rsi = results.iloc[i].rsi
                else:
                    if (results.iloc[i].rsi < 50):
                    # if ((results.macd.iloc[i] <= results.macdsignal.iloc[i] and results.macd.iloc[i-1] >= results.macdsignal.iloc[i-1]) \
                    #     and (results.rsi.iloc[i] <= results.rsibasedma.iloc[i] and results.rsi.iloc[i-1] >= results.rsibasedma.iloc[i-1])):
                        counter = 0
                        sell_timestamp = results.iloc[i].pricetime
                        sell_price = results.iloc[i].close_price
                        sell_rsi = results.iloc[i].rsi
                        price += (((sell_price-buy_price) / buy_price)) * price
                        data.update({'buy pricetime': buy_timestamp,
                                     'buy price': buy_price,
                                     'buy rsi': buy_rsi,
                                     'sell pricetime': sell_timestamp,
                                     'sell_price': sell_price,
                                     'sell_rsi': sell_rsi,
                                     'profit percentage': ((sell_price-buy_price) / buy_price) * 100,
                                     'difference': sell_price - buy_price,
                                     'price': price})

                                # with open('./buysell/buysell' + symbol + intervals + '.json', 'a') as f:
                        with open(path + 'bt/' + intervals + '/' + symbol + intervals + '_rsi50_backtest.json', 'a') as f:
                            json.dump(data, f)
                            f.write('\n')
            except Exception as e:
                print(f'{e}, {symbol}{intervals}')
                continue

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

