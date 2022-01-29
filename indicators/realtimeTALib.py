import sqlalchemy
from data.coins import coin_details
from indics import indicator

def job(symbol, intervals, dbname):
    print("connection is started")
    engine = sqlalchemy.create_engine('sqlite:///C:/Users/eboran/Desktop/' + dbname + '.db')
    print("connection is done")
    indicator.Calculate.MACDRSIcondreal(engine, symbol, intervals)
    # prices = pd.read_sql('SELECT * FROM ' + symbol + interval + '', engine)
    """Does required calculations based on indicator types"""

if __name__ == '__main__':
    dbname = 'DEVSELECTED_15JAN'
    symbol, intervals = coin_details()
    symbol = "BTCUSDT"
    intervals = intervals[0]
    job(symbol, intervals, dbname)


