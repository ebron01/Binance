import sys
import requests
import json

class Inform:
    def __init__(self, initialdata=None, message1=None, lastdata=None,  message2=None):
        self.initialdata = initialdata
        self.message1 = message1
        self.lastdata = lastdata
        self.message2 = message2

    def general_notify(self):
        # url = "<Webhook_URL>"
        url = "https://hooks.slack.com/services/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"
        # message = ("A Sample Message")
        # title = (f"New Incoming Message :zap:")
        slack_data = {
            "username": "NotificationBot",
            # "icon_emoji": ":satellite:",
            # "channel" : "#somerandomcahnnel",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            # "title": title,
                            "value": self.message1,  # message['c'] means only current
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

    def notify(self):
        # url = "<Webhook_URL>"
        url = "https://hooks.slack.com/services/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"
        # message = ("A Sample Message")
        # title = (f"New Incoming Message :zap:")
        slack_data = {
            "username": "NotificationBot",
            # "icon_emoji": ":satellite:",
            # "channel" : "#somerandomcahnnel",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            # "title": title,
                            "value": self.message1 + self.initialdata['c'],  # message['c'] means only current
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

    def notifyalarm(self):
        # url = "<Webhook_URL>"
        url = "https://hooks.slack.com/services/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"
        # message = ("A Sample Message")
        # title = (f"New Incoming Message :zap:")
        slack_data = {
            "username": "NotificationBot",
            # "icon_emoji": ":satellite:",
            # "channel" : "#somerandomcahnnel",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            # "title": title,
                            "value": self.message1 + self.initialdata['c'] + ', ' + self.message2 + self.lastdata['c'],
                            # message['c'] means only current
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

    """This must be changed it has hardcoded index in it"""
    def MACD_informer(self):
        # url = "<Webhook_URL>"
        url = "https://hooks.slack.com/services/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"
        # message = ("A Sample Message")
        # title = (f"New Incoming Message :zap:")
        slack_data = {
            "username": "NotificationBot",
            # "icon_emoji": ":satellite:",
            # "channel" : "#somerandomcahnnel",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            # "title": title,
                            "value": 'Buy date is ' + self.message1.macdBuy[41]['MACDdate :'] +
                                     ',\n MACD: ' + str(self.message1.macdBuy[41]['MACD :']) +
                                     ',\n MACDSIGNAL: ' + str(self.message1.macdBuy[41]['MACDSIGNAL :']) +
                                     ',\n MACDHIST: ' + str(self.message1.macdBuy[41]['MACDHIST :']),  # message['c'] means only current
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