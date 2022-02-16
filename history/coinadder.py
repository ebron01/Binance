import sys
sys.path.append('C:/Users/a/PycharmProjects/Binance/')
from keys import api_keys
from binance.client import Client
import sqlalchemy
import sqlite3
import pandas as pd
sys.path.append('C:/Users/a/PycharmProjects/Binance/indicators/')
from data.coins import coin_details
from indics import indicator

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

def writetoSQLite(symbol, intervals, dbname):
    connection = sqlite3.connect('./DBDEV/' + dbname + '.db')  # creates a new database if there is none.
    cursor = connection.cursor()  # we can execute sql commands with this cursor.
    counter = 0
    for sym in symbol:
        for interval in intervals:
            print(f'Doing {sym}')
            print(f'Creating table')
            tablename = sym+interval
            # cursor.execute("CREATE TABLE IF NOT EXISTS " + tablename + " (open_time TEXT, open_price REAL, high_price REAL, low_price REAL, \
            #                 close_price REAL, volume REAL, close_time TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS " + tablename + " ( open_time TEXT, open_price REAL, high_price REAL, low_price REAL, \
            close_price REAL, volume REAL, close_time TEXT, bbandlittle REAL, bbandmiddle REAL, bbandupper REAL, buy REAL, chande REAL, \
            closeprice REAL, currenttime REAL, dmi REAL, dmineg REAL, dmiplus REAL, kauf REAL, macd REAL, macdbuy REAL, macdhist  REAL, macdsell REAL, \
            macdsignal REAL, obv REAL, obv_ema REAL, pricetime REAL, rsi REAL, rsibasedma REAL, rsibuy REAL, rsisell REAL, sell REAL, \
            PRIMARY KEY(close_time))")
            connection.commit()
            print(f'Created table')
            if interval == '30MINUTE' or interval == '1HOUR' or interval == '4HOUR':
                continue
            interval_function = "Client.KLINE_INTERVAL_" + interval
            """
            eval(interval_function) creates a call-function name as Client.KLINE_INTERVAL_1DAY
            """
            print(f"started getting klines of {sym} {interval}")
            """This start and brings excluding start and including  end timestamps so beware to run after the end timestamp
            otherwise will get unclosed end timestamp values"""
            klines = client.get_historical_klines(sym, eval(interval_function), "Jan 1, 2015")
            klines = klines[:-1] #delete unclosed last timestamp
            print(f"ended getting klines of {sym} {interval}, there is {len(klines)} entry")
            print('cleaning lines')
            cleanklines = datacleaning(klines)
            print('cleaned lines')
            print(f"inserting into {sym} {interval}")
            counter =0
            for line in cleanklines:
                cursor.execute("INSERT INTO " + tablename + "(open_time , open_price, high_price, low_price, close_price, volume, close_time) VALUES(?, ?, ?, ?, ?, ?, ?)",
                               (line[0], line[1], line[2], line[3], line[4], line[5], line[6]))
                connection.commit()
                counter += 1
            if counter % 100 == 0:
                print(f'done inserting {counter} out of {len(cleanklines)}')
            print(f"inserted into {sym} {interval}")

            if tablename.startswith('1'):
                tablename = tablename.strip('1')
                print(f"1 silindi, token ismi {tablename}")

            """this part reads all prices from database"""
            engine = sqlalchemy.create_engine('sqlite:///./DBDEV/' + dbname + '.db')
            prices = pd.read_sql('SELECT s.open_time , s.open_price, s.high_price, s.low_price, s.close_price, s.volume, s.close_time FROM ' + tablename + ' s', engine)
            """Does required calculations based on indicator types"""
            indicators = indicator.Indicators()
            try:
                result = indicator.Calculate.calculator(indicators, prices)
                result_keys = result.keys()
                """fills nan values with 0 to be able to write to database"""
                for i in range(len(result_keys)):
                    try:
                        result_keys[i] = result_keys[i].fillna(0)
                    except:
                        continue
                """inserts all calculated ta to the affiliated columns"""
                for i in range(len(result.closeprice.keys())):
                    cursor.execute(f'''UPDATE {tablename} SET rsi=?, rsibasedma=?,  macd=?, macdsignal=?, macdhist=?, pricetime=?,
                            obv=?, kauf=?, obv_ema=?, chande=?, bbandupper=?, bbandmiddle=?, bbandlittle=?, dmi=?, dmineg=?, dmiplus=?, closeprice=? WHERE open_time=?''',
                                   (result.rsi.iloc[i], result.rsibasedma.iloc[i], result.macd.iloc[i], result.macdsignal.iloc[i],
                                    result.macdhist.iloc[i], result.pricetime.iloc[i], result.obv.iloc[i], result.kauf.iloc[i],
                                    result.obv_ema.iloc[i], result.chande.iloc[i], result.bbandupper.iloc[i],
                                    result.bbandmiddle.iloc[i], result.bbandlittle.iloc[i], result.dmi.iloc[i],
                                    result.dmineg.iloc[i], result.dmiplus.iloc[i], result.closeprice.iloc[i],
                                    result.pricetime.iloc[i]))
                    connection.commit()
                    if i % 100 == 0:
                        print(f'done inserting {i} out of {len(result.closeprice.keys())}')
            except Exception as e:
                print(e)
                continue
if __name__ == '__main__':
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    # symbol, intervals = coin_details()
    symbol = ['HNTUSDT', 'XRPUSDT', 'LUNAUSDT', 'NEARUSDT', 'SHIBUSDT', 'DOGEUSDT', 'EGLDUSDT']
    interval = ['1MONTH', '1WEEK', '1DAY', '4HOUR', '1HOUR', '30MINUTE']
    dbname = 'COINADDERDB'
    writetoSQLite(symbol, interval, dbname)



