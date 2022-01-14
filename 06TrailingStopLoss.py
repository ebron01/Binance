import pandas as pd
import sqlalchemy
from binance.client import Client
from binance.streams import BinanceSocketManager
import asyncio
from keys import api_keys

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

async def main(pair):
    """connection to Binance real trading account"""
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket(pair)
    """this part until frame.to_sql line writes price of the pair to sqlite database pair table"""
    while True:  # this sends frame to sqldatabase we created under main every second
        await socket.__aenter__()
        msg = await socket.recv()
        if msg['e'] == 'error':
            print('error')
            client.close_connection()
            # close and restart the socket
            bsm = BinanceSocketManager(client)
            socket = bsm.trade_socket(pair)
        else:
            try:
                frame = createframe(msg)
                frame.to_sql(pair, engine, if_exists='append',
                             index=False)  # if we have already written values to pair table, this part appends to it.
            except:
                continue
        print(frame)

if __name__ == '__main__':
    pair = "ADAUSDT"
    engine = sqlalchemy.create_engine('sqlite:///'+pair+'stream.db')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pair))
