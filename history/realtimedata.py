import sys
sys.path.append('C:/Users/a/PycharmProjects/Binance/')
sys.path.append('C:/Users/a/PycharmProjects/Binance/indicators/')
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
from keys import api_keys
from binance.client import Client
from timeit import default_timer as timer
import sqlite3
from data.coins import coin_details
import sqlalchemy
from indics import indicator

"""IF NOT SUCCESSFUL THEN https://www.geeksforgeeks.org/python-schedule-library/"""
def getPairs(client):
    """This part creates the list of coin pairs that are listed on Binance"""
    symbol = []
    deadtokens = ['BCCUSDT', 'VENUSDT', 'PAXUSDT', 'BCHABCUSDT', 'BCHSVUSDT', 'USDSUSDT', 'USDSBUSDT', 'ERDUSDT', 'NPXSUSDT',
     'STORMUSDT', 'HCUSDT', 'MCOUSDT', 'BULLUSDT', 'BEARUSDT', 'ETHBULLUSDT', 'ETHBEARUSDT', 'EOSBULLUSDT',
     'EOSBEARUSDT', 'XRPBULLUSDT', 'XRPBEARUSDT', 'STRATUSDT', 'BNBBULLUSDT', 'BNBBEARUSDT', 'USDTZAR', 'XZCUSDT',
     'LENDUSDT', 'BKRWUSDT', 'DAIUSDT', 'USDTBKRW', 'BZRXUSDT', 'EOSUPUSDT', 'EOSDOWNUSDT', 'UNIUPUSDT', 'UNIDOWNUSDT',
     'SXPUPUSDT', 'SXPDOWNUSDT', 'YFIUPUSDT', 'YFIDOWNUSDT', 'AAVEUPUSDT', 'AAVEDOWNUSDT', 'SUSHIUPUSDT',
     'SUSHIDOWNUSDT', 'XLMUPUSDT', 'XLMDOWNUSDT', 'USDTBVND', '1INCHUPUSDT', '1INCHDOWNUSDT', 'USDTGYEN']
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        if s['symbol'] not in deadtokens:
            if 'USDT' in s['symbol']:
                symbol.append(s['symbol'])
    return symbol

def datacleaning(line):
    """ RETURN DATA FORMAT OF client.get_historical_klines
            [
          [
            1499040000000,      // Open time
            "0.01634790",       // Open
            "0.80000000",       // High
            "0.01575800",       // Low
            "0.01577100",       // Close
            "148976.11427815",  // Volume
            1499644799999,      // Close time
            "2434.19055334",    // Quote asset volume
            308,                // Number of trades
            "1756.87402397",    // Taker buy base asset volume
            "28.46694368",      // Taker buy quote asset volume
            "17928899.62484339" // Ignore.
          ]
        ]
        """
    return [str(pd.to_datetime(line[6], unit='ms')), line[1], line[2], line[3], line[4], line[5], str(pd.to_datetime(line[6], unit='ms'))]

def job(client, symbol, interval, dbname):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    interval_function = "Client.KLINE_INTERVAL_" + interval
    start = timer()
    counter = 0
    for sym in symbol:
        connection = sqlite3.connect('./DBDEV/' + dbname + '.db')  # creates a new database if there is none.
        cursor = connection.cursor()
        counter += 1
        tablename = sym + interval
        if tablename.startswith('1'):
            tablename = tablename.strip('1')
            print(f"1 silindi, token ismi {tablename}")
        candles = client.get_klines(symbol=sym, interval=eval(interval_function))
        candletime1 = pd.to_datetime(candles[-1][6], unit='ms')
        candletime2 = pd.to_datetime(candles[-2][6], unit='ms')
        servertime = pd.to_datetime(client.get_server_time()['serverTime'], unit='ms')
        print(f'{sym} {counter} server time is {servertime},' + interval + f' interval datetime -2 {candletime2},' + interval +
               f' interval datetime -1 {candletime1}')
        if (pd.to_datetime(candles[-1][6], unit='ms') > pd.to_datetime(client.get_server_time()['serverTime'], unit='ms')):
            candles = candles[-2]
        else:
            candles = candles[-1]
        cleankline = datacleaning(candles)
        try:
            """this part inserts prices to database first"""
            # cursor.execute("INSERT INTO " + tablename + " VALUES(?, ?, ?, ?, ?, ?, ?)",
            #            (cleankline[0], cleankline[1], cleankline[2], cleankline[3], cleankline[4], cleankline[5], cleankline[6]))
            cursor.execute("INSERT INTO " + tablename + "(open_time , open_price, high_price, low_price, close_price, volume, close_time) VALUES(?, ?, ?, ?, ?, ?, ?)",
                       (cleankline[0], cleankline[1], cleankline[2], cleankline[3], cleankline[4], cleankline[5], cleankline[6]))
            connection.commit()
            """this part reads all prices from database"""
            engine = sqlalchemy.create_engine('sqlite:///./DBDEV/' + dbname + '.db')
            prices = pd.read_sql('SELECT s.open_time , s.open_price, s.high_price, s.low_price, s.close_price, s.volume, s.close_time FROM ' + tablename + ' s', engine)
            """Does required calculations based on indicator types"""
            indicators = indicator.Indicators()
            result = indicator.Calculate.calculator(indicators, prices)
            result_keys = result.keys()
            """fills nan values with 0 to be able to write to database"""
            for i in range(len(result_keys)):
                try:
                    result_keys[i] = result_keys[i].fillna(0)
                except:
                    continue
            """inserts all calculated ta to the affiliated columns"""
            cursor.execute(f'''UPDATE {tablename} SET rsi=?, rsibasedma=?,  macd=?, macdsignal=?, macdhist=?, pricetime=?,
                    obv=?, kauf=?, obv_ema=?, chande=?, bbandupper=?, bbandmiddle=?, bbandlittle=?, dmi=?, dmineg=?, dmiplus=?, closeprice=? WHERE open_time=?''',
                           (result.rsi.iloc[-1:].values[0], result.rsibasedma.iloc[-1:].values[0], result.macd.iloc[-1:].values[0],
                            result.macdsignal.iloc[-1:].values[0],
                            result.macdhist.iloc[-1:].values[0], result.pricetime.iloc[-1:].values[0], result.obv.iloc[-1:].values[0], result.kauf.iloc[-1:].values[0],
                            result.obv_ema.iloc[-1:].values[0], result.chande.iloc[-1:].values[0], result.bbandupper.iloc[-1:].values[0],
                            result.bbandmiddle.iloc[-1:].values[0], result.bbandlittle.iloc[-1:].values[0], result.dmi.iloc[-1:].values[0],
                            result.dmineg.iloc[-1:].values[0], result.dmiplus.iloc[-1:].values[0], result.closeprice.iloc[-1:].values[0],
                            result.pricetime.iloc[-1:].values[0]))
            connection.commit()
            print(f"local execution time {t}")
        except:
            print(f'passed {sym}')
            continue
    end = timer()
    print(f'Execution time {interval} for all tokens in seconds is : {end - start}')  # Time in seconds

if __name__ == '__main__':
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    dbname = 'DEVSELECTED_15JAN'
    symbol, intervals = coin_details()
    scheduler = BlockingScheduler()
    # Run every minute at 22 o'clock a day job Method
    scheduler.add_job(job, 'cron', minute='*/30', args=[client, symbol, '30MINUTE', dbname])
    scheduler.add_job(job, 'cron', hour='*/1', args=[client, symbol, '1HOUR', dbname])
    scheduler.add_job(job, 'cron', hour='*/4', args=[client, symbol, '4HOUR', dbname])
    scheduler.add_job(job, 'cron', day='*/1', args=[client, symbol, '1DAY', dbname])
    scheduler.add_job(job, 'cron', week='*/1', args=[client, symbol, '1WEEK', dbname])
    scheduler.add_job(job, 'cron', month='*',  args=[client, symbol, '1MONTH', dbname])
    # # Run once a day at 22 and 23:25 job Method
    # scheduler.add_job(job, 'cron', hour='14-15', minute='14', args=['job2'])
    scheduler.start()



