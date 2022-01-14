import websockets
import asyncio
from binance.client import Client
import json
import sys
import requests
from keys import api_keys

def slackinformer(data, message ):
    #url = "<Webhook_URL>"
    url = "https://hooks.slack.com/services/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"
    #message = ("A Sample Message")
    #title = (f"New Incoming Message :zap:")
    slack_data = {
        "username": "NotificationBot",
        #"icon_emoji": ":satellite:",
        # "channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        #"title": title,
                        "value": message + data['c'], #message['c'] means only current
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

async def main(symbol, price):
    async with stream as receiver:
        while True:
            data = await receiver.recv()
            data = json.loads(data)['data']
            if float(data['c']) > price:
                slackinformer(data, "BTC'nin değeri: ")
                break


if __name__ == '__main__':
    binance_api, binance_secret = api_keys()
    client = Client(binance_api, binance_secret)
    stream = \
        websockets.connect('wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(symbol='BTCUSDT', price=41600))