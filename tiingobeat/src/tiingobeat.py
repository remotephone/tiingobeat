import json
import socket
import os
from datetime import datetime
from time import sleep

import requests


def get_stocks():
    BASEURL = "https://api.tiingo.com/iex/"
    # Your API key
    TOKEN = os.environ['TOKEN'] 
    # Comma separated list, no spaces, of stocks you want to check
    # Not sure what the limit to the list size is, but its one request, so stack em up.
    # TICKERS = "aapl,zm,amd,amzn,sdc,nvda"
    TICKERS = os.environ["STOCKS"]

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.get("{}?tickers={}&token={}".format(BASEURL, TICKERS, TOKEN), headers=headers)

    # This returns a list of dictionaries with each item a stock
    # [{'prevClose': 7.87, 'mid': None, 'lastSaleTimestamp': '2020-09-02T20:00:00+00:00', 'open': 8.51, 'askPrice': None, 'low': 8.5, 'ticker': 'SDC', 'timestamp': '2020-09-02T20:00:00+00:00', 'lastSize': None, 'tngoLast': 9.8, 'last': 9.8, 'high': 9.99, 'askSize': None, 'quoteTimestamp': '2020-09-02T20:00:00+00:00', 'bidPrice': None, 'bidSize': None, 'volume': 38052031},
    # {'prevClose': 3499.12, 'mid': None, 'lastSaleTimestamp': '2020-09-02T20:00:00+00:00', 'open': 3547.0, 'askPrice': None, 'low': 3486.685, 'ticker': 'AMZN', 'timestamp': '2020-09-02T20:00:00+00:00', 'lastSize': None, 'tngoLast': 3531.45, 'last': 3531.45, 'high': 3552.25, 'askSize': None, 'quoteTimestamp': '2020-09-02T20:00:00+00:00', 'bidPrice': None, 'bidSize': None, 'volume': 3931476}]
    return response.json()

def put_stocks(response):
    elkhost = os.environ["LOGSTASH_HOST"]
    elkport = 5055
    for stock in response:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((elkhost, elkport))
        except:
            print("can't connect")

        try:
            sock.sendall(bytes(json.dumps(stock), encoding="utf-8"))
            sock.close()
        except:
            print("can't send")

def check_time():
    gotime = False
    while gotime == False: 
        d = datetime.now() 
        if (d.isoweekday() in range(1, 6) and d.hour in range(8, 16)):   
            return True
        else:
            print('sleep')
            sleep(60)

def main():
    while True:
        check_time()
        response = get_stocks()
        try:
            put_stocks(response)
            print('putted')
        except:
            print('oops')
        sleep(10)
        
if __name__ == "__main__":
    main()
