import sys
sys.path.append('C:/Users/a/PycharmProjects/Binance/')
from keys import api_keys
from binance.client import Client
import csv
import sqlite3
import pandas as pd
sys.path.append('C:/Users/a/PycharmProjects/Binance/indicators/')
from data.coins import coin_details


def datacleaning(klines):
    cleanklines = []
    for line in klines:
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
        cleanklines.append([str(pd.to_datetime(line[6], unit='ms')), line[1], line[2], line[3], line[4], line[5], str(pd.to_datetime(line[6], unit='ms'))])
    return cleanklines

def getPairs(client):
    """This part creates the list of coin pairs that are listed on Binance"""
    symbol = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        if 'USDT' in s['symbol']:
            symbol.append(s['symbol'])
    return symbol

def writetocsv(symbol, interval):
    """This part writes all historical data of all pairs of USDT in a given interval. Must change
    client.KLINE_INTERNAL_1DAY according to the interval needed"""
    for sym in symbol:
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
        klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "9 Jan, 2021")
        csvfile = open('./'+interval+'/'+sym+interval+'.csv', 'w', newline='')
        csvwriter = csv.writer(csvfile, delimiter=',')
        for kline in klines:
            csvwriter.writerow(kline)

def writetoSQLite(symbol, intervals, dbname):
    connection = sqlite3.connect('./DBDEV/' + dbname + '.db')  # creates a new database if there is none.
    cursor = connection.cursor()  # we can execute sql commands with this cursor.
    counter = 0
    for sym in symbol:
        for interval in intervals:
            counter +=1
            print(f'Doing {sym}')
            interval_function = "Client.KLINE_INTERVAL_" + interval
            """
            eval(interval_function) creates a call-function name as Client.KLINE_INTERVAL_1DAY
            """
            print(f"started getting klines of {sym} {interval}")
            """This start and brings including start and end timestamps so beware to run after the end timestamp
            otherwise will get unclosed end timestamp values"""
            if interval == "30MINUTE":
                start = '2022-01-22 18:29:59.999000'
                end = '2022-01-23 18:59:59.999000'
            elif interval == "1HOUR":
                start = '2022-01-22 17:59:59.999000'
                end = '2022-01-23 18:59:59.999000'
            elif interval == "4HOUR":
                start = '2022-01-21 23:59:59.999000'
                end = '2022-01-23 15:59:59.999000'
            elif interval == "1DAY":
                start = '2022-01-21 23:59:59.999000'
                end = '2022-01-22 23:59:59.999000'
            elif interval == "1WEEK":
                start = '2022-01-21 23:59:59.999000'
                end = '2022-01-22 23:59:59.999000'
            elif interval == "1MONTH":
                start = '2022-01-21 23:59:59.999000'
                end = '2022-01-22 23:59:59.999000'
            #klines = client.get_historical_klines(sym, eval(interval_function), "2021-01-15 19:47:59.999000", end_str="2022-01-15 07:59:59.999000")
            klines = client.get_historical_klines(sym, eval(interval_function), start, end)
            print(f"ended getting klines of {sym} {interval}")
            tablename = sym+interval
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
            # if tablename.startswith('1'):
            #     tablename = tablename.strip('1')
            #     print(f"1 silindi, token ismi {tablename}")
            # cursor.execute("CREATE TABLE IF NOT EXISTS " + tablename + " (open_time TEXT, open_price REAL, high_price REAL, low_price REAL, \
            #                 close_price REAL, volume REAL, close_time TEXT)")
            # connection.commit()
            cleanklines = datacleaning(klines)
            print(f"inserting into {sym} {interval}")
            for line in cleanklines:
                cursor.execute("INSERT INTO " + tablename + "(open_time , open_price, high_price, low_price, close_price, volume, close_time) VALUES(?, ?, ?, ?, ?, ?, ?)",
                               (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                connection.commit()
            print(f'Doing {interval}, Done {counter} out of {len(symbol) * len(intervals)} ')

if __name__ == '__main__':
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    symbol, intervals = coin_details()
    dbname = 'DEVSELECTED_15JAN'
    writetoSQLite(symbol, intervals, dbname)



