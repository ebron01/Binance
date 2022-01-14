import websockets
import pandas as pd
import asyncio
from binance.client import Client
import json
from keys import api_keys
import ta
from slackinform import Inform

def createframe(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'c']]
    df.columns = ['symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

async def main(TSL, symbol, profitperc, qty):
    df = pd.DataFrame()
    open_position = False
    """connection to Binance real trading account"""
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    async with stream as receiver:
        while True:
            data = await receiver.recv()
            data = json.loads(data)['data']

            df = df.append(createframe(data))
            print(df)
            if len(df) > 30:
                if not open_position:
                    if ta.momentum.roc(df.Price, 30).iloc[-1] > 0 and \
                            ta.momentum.roc(df.Price, 30).iloc[-2]:
                        order = client.create_order(symbol=symbol,
                                                    side='BUY', type='MARKET',
                                                    quantity=qty)
                        """This part sends via Slack the price  we have bought the asset """
                        informer = Inform(data, symbol + "'nin satın alındığı fiyat: ")
                        Inform.notify(informer)
                        print(order)
                        open_position = True
                        buyprice = float(order['fills'][0]['price'])
                        print('Buy price is ' + buyprice)

                if open_position:
                    subdf = df[df.Time >= pd.to_datetime(order['transactTime'], unit='ms')]
                    if len(subdf) > 1:
                        subdf['highest'] = subdf.Price.cummax()
                        subdf['trailingstop'] = subdf['highest'] * TSL
                        if subdf.iloc[-1].Price < subdf.iloc[-1].trailingstop or \
                            df.iloc[-1] / float(order['fills'][0]['price']) > (profitperc + 1):
                            order = client.create_order(symbol=symbol,
                                                        side='SELL', type='MARKET',
                                                        quantity=qty)
                            """This part sends via Slack the price we have sold the asset """
                            informer = Inform(data, symbol + "'nin satıldığı  fiyat: ")
                            Inform.notify(informer)

                        print(order)
                        sellprice = float(order['fills'][0]['price'])
                        print(f"Sell price is {sellprice}. You made {(sellprice-buyprice)/buyprice} profit")
                        open_position = False
                        """In any case, break the while loop because once open position is set to false again it will start to 
                        search a buy order at a conditional price"""
                        break

if __name__ == '__main__':
    symbol = 'BTCUSDT'
    stream = websockets.connect('wss://stream.binance.com:9443/stream?streams='+symbol.lower()+'@miniTicker')
    """stoploss is the percentage that we let our selling price to drop under highest price achieved after transaction of
    buy order, it will be constantly updated because we calculate it for each time step after buy order is executed. 
    For example, if our buy order is executed at 10 dollars and if we select TSL percentage as 0.995 and current price 
    goes up to 11 then trailing stop price will be elevated from 10*0.995 to 11*0.995 and sell order will be given 
    if price drops under 11*0.995 dollars"""
    stoploss = 0.995
    """profitperc is the percentage with respect to buying price that will be our sell threshold 
    when executing the sell order"""
    profitperc = 0.002
    "qty is the amount we want to buy from that pair"
    qty = 1
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(stoploss, symbol, profitperc, qty))
