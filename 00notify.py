"""This code sends a slack notification if there happens to be a certain threshold drop at a coin's price"""
import websockets
import asyncio
from binance.client import Client
import json
import sys
import requests
from keys import api_keys
from slackinform import Inform

async def main(symbol):
    async with stream as receiver:
        initialdata = await receiver.recv()
        initialdata = json.loads(initialdata)['data']
        informer = Inform(message1=f'Initial price is {str(initialdata)}')
        Inform.general_notify(informer)
        while True:
            lastdata = await receiver.recv()
            lastdata = json.loads(lastdata)['data']
            if float(initialdata['c']) - float(lastdata['c']) > 100\
                    or float(lastdata['c']) - float(initialdata['c']) > 100:
                informer = Inform(initialdata, "BTC'nin ilk değeri: ", lastdata, 'son değeri:')
                Inform.notifyalarm(informer)
                initialdata = lastdata


if __name__ == '__main__':
    informer = Inform(message1='Notifications open')
    Inform.general_notify(informer)
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    symbol = 'BTCUSDT'
    stream = websockets.connect('wss://stream.binance.com:9443/stream?streams='+symbol.lower()+'@miniTicker')
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(symbol))
    except:
        informer = Inform(message1='bağlantı yenilendi')
        Inform.general_notify(informer)
        binance_api, binance_secret = api_keys()
        client = Client(binance_api, binance_secret)
        symbol = 'BTCUSDT'
        stream = websockets.connect('wss://stream.binance.com:9443/stream?streams=' + symbol.lower() + '@miniTicker')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(symbol))