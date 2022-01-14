import pandas as pd
import sqlalchemy
from binance.client import Client
from keys import api_keys

def TLSstrategy(entry, stoploss, lookback, qty, open_position=False):
    while True:
        df = pd.read_sql(pair, engine)
        """this brings rows of lookback window from the database"""
        lookbackperiod = df.iloc[-lookback:]
        """this brings cumulated return as the price change in the window by considering two entries as s, s+1"""
        cumreturn = (lookbackperiod.Price.pct_change()+1).cumprod()-1
        """cumreturn[-1] means last valid entry of this cumulative return of lookback window"""
        if cumreturn[cumreturn.last_valid_index()] < entry:
            order = client.create_order(symbol=pair,
                                        side='BUY',
                                        type='MARKET',
                                        quantity=qty)
            print(order)
            open_position = True
            break
    """Trailing Stop Loss part from here on"""
    if open_position:
        while True:
            """we have to retreat only the prices after the buy order's transaction instant, 
            this SQLite command is for that reason. Now returned df is the prices after order transaction instant"""
            df = pd.read_sql(f""""SELECT * FROM {pair} WHERE \
            Time >= '{pd.to_datetime(order['transactTime'], unit='ms')}'""", engine)

            """this cummax function from pd lib finds the highest price recorded to database 
            read with line above. If table has more then one coin type then it will find highest for each pair"""
            df['Benchmark'] = df.Price.cummax()
            """TSL:trailing stop loss like 0.995 of the highest price after order transaction time"""
            df['TSL'] = df['Benchmark'] * stoploss

            """checking if current price is smaller than trailing stop loss price"""
            if df[df.Price < df.TSL].first_valid_index():
                    order = client.create_order(symbol=pair,
                                            side='SELL',
                                            type='MARKET',
                                            quantity= qty)
                    print(order)
                    break

if __name__ == '__main__':
    """connection to Binance real trading account"""
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    pair = "ADAUSDT"
    engine = sqlalchemy.create_engine('sqlite:///'+pair+'stream.db')

    """if the price drops with entry percentage, the order will be placed.If entry is negative then it will trigger buy 
    order if new price is lover than the price a timestamp ago. If positive it will need price to be getting higher."""
    entry = -0.0015
    """stoploss is the percentage that we let our selling price to drop under highest price achieved until sell order, 
    it will be constantly updated because we calculate it for each time step after buy order is executed. For example, 
    if our buy order is executed at 10 dollars and if we select TSL percentage as 0.995 and current price goes up to 11 
    then trailing stop price will be elevated from 10*0.995 to 11*0.995 and sell order will be given if price drops 
    under 11*0.995 dollars"""
    stoploss = 0.995
    "lookback is the window that we will use to calculate the drop in the prices before executing the buy order"
    lookback = 60
    "qty is the amount we want to buy from that pair"
    qty = 1
    TLSstrategy(entry, stoploss, lookback, qty)
