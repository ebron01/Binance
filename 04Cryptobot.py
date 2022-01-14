"""This code reads the BTC values from Binance api with BinanceSocketManager and writes them instantaneously to a sqlite
database. The code in 05Cryptolivetrading.py uses this database. For this reason, while running 05Cryptolivetrading.py,
this code must be running beforehand"""

import pandas as pd
import sqlalchemy
from binance.client import Client
from binance.streams import BinanceSocketManager
import asyncio
from keys import api_keys

def createframe(msg):
    try:
        df = pd.DataFrame([msg])
        df = df.loc[:, ['s', 'E', 'p']]
        df.columns = ['symbol', 'Time', 'Price']
        df.Price = df.Price.astype(float)
        df.Time = pd.to_datetime(df.Time, unit='ms')
    except:
        df = pd.DataFrame([msg])
        print('df error')
    return df

async def main():
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket('BTCUSDT')
    while True:#this sends frame to sqldatabase we created under main every second
        await socket.__aenter__()
        msg = await socket.recv()
        if msg['e'] == 'error':
            print('error')
            client.close_connection()
        # close and restart the socket
            bsm = BinanceSocketManager(client)
            socket = bsm.trade_socket('BTCUSDT')
        else:
            try:
                frame = createframe(msg)
                frame.to_sql('BTCUSDT', engine, if_exists='append', index=False)#if we have already written values to BTCUSDT table, this part appends to it.
            except:
                continue
        print(frame)


if __name__ == '__main__':
    engine = sqlalchemy.create_engine('sqlite:///sqldatabase/BTCUSDTstream.db')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
