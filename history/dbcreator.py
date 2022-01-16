from keys import api_keys
from binance.client import Client
import sqlite3
from data.coins import coin_details
def getPairs(client):
    """This part creates the list of coin pairs that are listed on Binance"""
    symbol = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
        if 'USDT' in s['symbol']:
            symbol.append(s['symbol'])
    return symbol

def writetoSQLite(symbol, intervals, dbname):
    counter = 0
    for interval in intervals:
        for sym in symbol:
            counter += 1
            print(f'Doing {sym}{interval}')
            connection = sqlite3.connect('./DBDEV/' + dbname + '.db')  # creates a new database if there is none.
            cursor = connection.cursor()  # we can execute sql commands with this cursor.
            tablename = sym+interval
            if tablename.startswith('1'):
                tablename = tablename.strip('1')
                print(f"1 silindi, token ismi {tablename}")
            """This cursor keeps us connected to './DB/selecteddatabase.db'"""
            cursor.execute("CREATE TABLE IF NOT EXISTS " + tablename + " (open_time TEXT, open_price REAL, high_price REAL, low_price REAL, \
                            close_price REAL, volume REAL, close_time TEXT, PRIMARY KEY(close_time))")
            connection.commit()
            print(f'Done creating {counter} out of {len(symbol)*len(intervals)} ')

if __name__ == '__main__':
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    """
    FOR ALL COINS OTHER THAN DEAD ONES
    """
    # symbol = getPairs(client)
    # intervals = ['1HOUR', '4HOUR', '1DAY', '1WEEK', '1MONTH']
    """
    FOR SELECTED COINS OUT OF EVERY COIN OTHER THAN DEAD ONES
    """
    symbol, intervals = coin_details()
    dbname = 'DEVSELECTEDLIVE_15JAN'
    writetoSQLite(symbol, intervals, dbname)
