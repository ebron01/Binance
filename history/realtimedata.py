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
            cursor.execute("INSERT INTO " + tablename + " VALUES(?, ?, ?, ?, ?, ?, ?)",
                       (cleankline[0], cleankline[1], cleankline[2], cleankline[3], cleankline[4], cleankline[5], cleankline[6]))
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
    dbname = 'DEVSELECTEDLIVE_15JAN'
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



