print('started imports')
import sqlalchemy
from data.coins import coin_details
from indics import indicator
import argparse
import os
print('done imports')
def backtestRSI(engine, path):
    symbol, intervals = coin_details()
    line = 1
    for sym in symbol:
        print(line)
        for interval in intervals:
            # if interval in ['4HOUR', '1DAY', '1WEEK', '1MONTH']:
            #     continue
            indicator.Calculate.RSI50backtest(engine, sym, interval, path)
        line += 1
    for interval in intervals:
        dir = os.listdir(path + 'bt/' + interval)
        count = 0
        total_price = 0.0
        for d in dir:
            count += 1
            with open(path + 'bt/' + interval + '/' + d, 'r') as f:
                data = f.readlines()
                # total = 0.0
                # for i in range(len(data)):
                #     perc = data[i].strip('\n').strip('{').strip('}').split(', ')[6].split(" ")[2]
                #     total += float(perc)
                lastprice = data[-1].strip('\n').strip('{').strip('}').split(', ')[8].split(" ")[1]
                with open(path + 'bt/' + interval + '.txt', 'a') as f:
                    last = d.split('_')[0] + ':' + str(lastprice)+'\n'
                    f.write(last)
                    total_price += float(lastprice)
                    if count == len(dir):
                        start_money = 1000 * len(dir)
                        f.write('total start money: ' + str(start_money)+ ', end money is: ' + str(total_price))


def job(symbol, intervals, dbname):
    # print("connection is started")
    engine = sqlalchemy.create_engine('sqlite:///E:/Binance/history/DBDEV/' + dbname + '.db')
    # path = '/mnt/e/wsl/e/Binance/indicators/buysell/'
    path = 'E:/Binance/indicators/buysell/'
    # engine = sqlalchemy.create_engine('sqlite:////mnt/e/wsl/e/Binance/history/DBDEV/' + dbname + '.db')
    #
    print("connection is done")
    """this part is for MACD and RSI implemantion together"""
    # indicator.Calculate.MACDRSIcondreal(engine, symbol, intervals, path)
    """this part is for calculations according to RSI over 50 or under."""
    # indicator.Calculate.RSI50(engine, symbol, intervals, path)
    """this part is for backtest calculations according to RSI over 50 or under."""
    backtestRSI(engine, path)

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


