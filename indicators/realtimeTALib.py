print('started imports')
import sqlalchemy
from data.coins import coin_details
from indics import indicator
import argparse
print('done imports')
def job(symbol, intervals, dbname):
    print("connection is started")
    # engine = sqlalchemy.create_engine('sqlite:///E:/Binance/history/DBDEV/' + dbname + '.db')
    path = '/mnt/e/wsl/e/Binance/indicators/buysell/'
    # path = 'E:/Binance/indicators/buysell/'
    engine = sqlalchemy.create_engine('sqlite:////mnt/e/wsl/e/Binance/history/DBDEV/' + dbname + '.db')
    #
    print("connection is done")
    indicator.Calculate.MACDRSIcondreal(engine, symbol, intervals, path)
    # prices = pd.read_sql('SELECT * FROM ' + symbol + interval + '', engine)
    """Does required calculations based on indicator types"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', action="store", dest='intervals')
    parser.add_argument('--symbol', action="store", dest='symbol')
    args = parser.parse_args()
    dbname = 'DEVSELECTED_15JAN'
    # symbol, intervals = coin_details()
    # symbol = "BTCUSDT"
    # intervals = intervals[0]
    intervals = args.intervals
    symbol = args.symbol
    job(symbol, intervals, dbname)


