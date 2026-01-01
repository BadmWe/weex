import time
import hmac
import hashlib
import base64
import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

WEEX_API_KEY = os.environ.get("WEEX_API_KEY")
WEEX_SECRET_KEY = os.environ.get("WEEX_SECRET_KEY")
WEEX_ACCESS_PASSPHRASE = os.environ.get("WEEX_ACCESS_PASSPHRASE")

url = "https://api-contract.weex.com/"

def generate_signature(secret_key, timestamp, method, request_path, query_string, body):
  message = timestamp + method.upper() + request_path + query_string + str(body)
  signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
  # print(base64.b64encode(signature).decode())
  return base64.b64encode(signature).decode()


def generate_signature_get(secret_key, timestamp, method, request_path, query_string):
  message = timestamp + method.upper() + request_path + query_string
  signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
  # print(base64.b64encode(signature).decode())
  return base64.b64encode(signature).decode()


def send_request_post(api_key, secret_key, access_passphrase, method, request_path, query_string, body):
  timestamp = str(int(time.time() * 1000))
  # print(timestamp)
  body = json.dumps(body)
  signature = generate_signature(secret_key, timestamp, method, request_path, query_string, body)

  headers = {
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": access_passphrase,
        "Content-Type": "application/json",
        "locale": "en-US"
  }

  url = "https://api-contract.weex.com/"  # Please replace with the actual API address
  if method == "GET":
    response = requests.get(url + request_path, headers=headers)
  elif method == "POST":
    response = requests.post(url + request_path, headers=headers, data=body)
  return response

def send_request_get(api_key, secret_key, access_passphrase, method, request_path, query_string):
    timestamp = str(int(time.time() * 1000))
    # print(timestamp)
    signature = generate_signature_get(secret_key, timestamp, method, request_path, query_string)

    headers = {
            "ACCESS-KEY": api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": access_passphrase,
            "Content-Type": "application/json",
            "locale": "en-US"
    }

    response = requests.get(url + request_path + query_string, headers=headers)
    return response

def get():
    # Example of calling a GET request
    request_path = "/capi/v2/account/position/singlePosition"
    query_string = '?symbol=cmt_btcusdt'
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)

def get_BTC():
    # Example of calling a GET request
    response = requests.get("https://api-contract.weex.com/capi/v2/market/ticker?symbol=cmt_btcusdt")
    print(response.status_code)
    print(response.text)

def post():
    # Example of calling a POST request
    request_path = "/capi/v2/order/placeOrder"
    body = {
        "symbol": "cmt_btcusdt",
        "client_oid": "71557515757447",
        "size": "0.0002",
        "type": "1",
        "order_type": "0",
        "match_price": "1",
        #"price": "80000"
    }
    query_string = ""
    response = send_request_post(api_key, secret_key, access_passphrase, "POST", request_path, query_string, body)
    print(response.status_code)
    print(response.text)


def get_trades():
    request_path = "/capi/v2/market/trades"
    query_string = "?symbol=cmt_btcusdt"
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def account_assets():
    request_path = "/capi/v2/account/assets"
    query_string = ""
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def all_positions():
    request_path = "/capi/v2/account/position/allPosition"
    query_string = ""
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def order_info():
    request_path = "/capi/v2/order/detail"
    query_string = "?orderId=701754554575750010"
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def current_orders():
    request_path = "/capi/v2/order/current"
    query_string = "?symbol=cmt_btcusdt"
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def history_orders():
    request_path = "/capi/v2/order/history"
    query_string = "?symbol=cmt_btcusdt"
    response = send_request_get(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "GET", request_path, query_string)
    print(response.status_code)
    print(response.text)


def close_positions():
    request_path = "/capi/v2/order/closePositions"
    body = {
      "symbol": "cmt_btcusdt"
    }
    query_string = ""
    response = send_request_post(WEEX_API_KEY, WEEX_SECRET_KEY, WEEX_ACCESS_PASSPHRASE, "POST", request_path, query_string, body)
    print(response.status_code)
    print(response.text)


if __name__ == '__main__':
    # close_positions()
    get()
    order_info()
    get_trades()
    history_orders()
    account_assets()
    get_BTC()
    all_positions()
