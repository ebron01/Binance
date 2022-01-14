from binance.client import Client
from binance.streams import ThreadedWebsocketManager
import os
from time import sleep
from keys import api_keys

#api_key = os.environ.get('binance_api')
#api_secret = os.environ.get('binance_secret')
def btc_trade_history(msg):
    #define how to process incoming WebSocket messages
	if msg['e'] != 'error':
		print(msg['c'])
		btc_price['last'] = msg['c']
		btc_price['bid'] = msg['b']
		btc_price['last'] = msg['a']
		btc_price['error'] = False
	else:
		btc_price['error'] = True

binance_api, binance_secret = api_keys()
client = Client(binance_api, binance_secret)
print(client.get_asset_balance(asset='BTC'))

btc_price = client.get_symbol_ticker(symbol = 'BTCUSDT')
#hnt_price = client.get_symbol_ticker(symbol = 'HNTUSDT')
#coti_price = client.get_symbol_ticker(symbol = 'COTIUSDT')
#print('BTC:', float(btc_price['price']),'HNT:', float(hnt_price['price']),'COTI:', float(coti_price['price']))

btc_price = {'error':False}

# init and start the WebSocket
bsm = ThreadedWebsocketManager()
bsm.start()
#help(ThreadedWebsocketManager)
# subscribe to a stream
bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol='BTCUSDT')
#bsm.start_symbol_ticker_socket(symbol='BTCUSDT')