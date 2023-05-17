from urllib.parse import urlencode

import requests
import json
import hashlib
import hmac

import config
from config import *
import datetime
import ssl
from requests.packages import urllib3

urllib3.disable_warnings()

# 币安API Key和Secre
api_key = "nXM2eE1D57gojrHTto1BJDa0JD3NCFRXr4fjoZQs5K1Wz2Nfhe92b8kIadOJroqV"
api_secret = "LS075wB1lOOzIb58OYsiOYdadAfmYe1uEbzAcnJo3zQw4HdFZqMZ7oEpsgoFyqQ4"

# API请求地址
url = "https://fapi.binance.com"

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)


# 构造请求参数
def cleanNoneValue(d) -> dict:
    out = {}
    for k in d.keys():
        if d[k] is not None:
            out[k] = d[k]
    return out


def encoded_string(query, special=False):
    if special:
        return urlencode(query).replace("%40", "@").replace("%27", "%22")
    else:
        return urlencode(query, True).replace("%40", "@")


def _prepare_params(params, special=False):
    return encoded_string(cleanNoneValue(params), special)


def account():
    # 查询合约账户信息的API
    endpoint = "/fapi/v2/account"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000"
    }
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=PROXY, verify=False)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        return result
    except:
        return False
    finally:
        response.close()


def balance():
    # 查询合约账户信息的API
    endpoint = "/fapi/v2/balance"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000"
    }
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        return result
    except:
        return False
    finally:
        response.close()


def get_orders(symbol="BTCUSDT"):
    # 查询所有订单(包括历史订单) (USER_DATA)
    endpoint = "/fapi/v1/allOrders"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        "symbol": symbol
    }
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day)
    start = int(start_of_today.timestamp()) * 1000
    params['startTime'] = start
    params['endTime'] = start + 86400000
    signature = hmac.new(api_secret.encode("utf-8"), _prepare_params(params=params).encode("utf-8"),
                         hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        response.close()
        return result
    except:
        return False


def getOrderInfo(orderId, symbol='BTCUSDT'):
    # 查询订单 (USER_DATA)
    endpoint = "/fapi/v1/order"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        "symbol": symbol,
        "orderId": int(orderId)
    }
    signature = hmac.new(api_secret.encode("utf-8"), _prepare_params(params=params).encode("utf-8"),
                         hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        response.close()
        return result
    except:
        return False


def getCjOrder(symbol='BTCUSDT'):
    # 账户成交历史 (USER_DATA)
    endpoint = "/fapi/v1/userTrades"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        # "symbol": symbol
    }
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day)
    start = int(start_of_today.timestamp()) * 1000
    params['startTime'] = start
    params['endTime'] = start + 86400000
    signature = hmac.new(api_secret.encode("utf-8"), _prepare_params(params=params).encode("utf-8"),
                         hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    result = json.loads(response.content)
    response.close()
    if result:
        for index in range(len(result)):
            order_info = getOrderInfo(result[index]['orderId'], result[index]['symbol'])
            result[index]['info'] = order_info
    return result


def positionRisk(symbol='BTCUSDT'):
    # 用户持仓风险V2 (USER_DATA)
    endpoint = "/fapi/v2/positionRisk"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        "symbol": symbol
    }
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        response.close()
        return result
    except:
        return False


def trades_group(symbol='BTCUSDT'):
    # 获取账户损益资金流水 (USER_DATA)
    endpoint = "/fapi/v1/income"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        # "symbol": symbol,
        "incomeType": "REALIZED_PNL"
    }
    now = datetime.datetime.now()
    start_of_today = datetime.datetime(now.year, now.month, now.day)
    start = int(start_of_today.timestamp()) * 1000
    params['startTime'] = start
    params['endTime'] = start + 86400000
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": api_key}
    response = requests.get(url + endpoint, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        result = json.loads(response.content)
        return result
    except:
        return False
    finally:
        response.close()


def setLever(num, symbol):
    # 调整开仓杠杆 (TRADE)
    endpoint = "/fapi/v1/leverage"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
        "symbol": symbol,
        "leverage": num
    }
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    # params['signature'] = signature
    headers = {"X-MBX-APIKEY": api_key}
    headers['Content-Type'] = "application/json"
    urls = url + endpoint + f'?{string}&signature=' + signature
    response = requests.post(urls, headers=headers, proxies=config.PROXY)
    try:
        result = json.loads(response.content)
        return result
    except:
        return False
    finally:
        response.close()


def listenKey():
    ##{'listenKey': 'yJ0zWkaPkgBrTCRSDSrb6Gn0AEswd6DgbfoLsKp5Ulsb1OTFi7UsKykDzh9hyQL1'}
    # 生成listenKey (USER_STREAM)
    endpoint = "/fapi/v1/listenKey"
    params = {
        "timestamp": int(time.time() * 1000),
        "recvWindow": "5000",
    }
    string = _prepare_params(params=params)
    signature = hmac.new(api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    # params['signature'] = signature
    headers = {"X-MBX-APIKEY": api_key}
    headers['Content-Type'] = "application/json"
    urls = url + endpoint + f'?{string}&signature=' + signature
    response = requests.post(urls, headers=headers, proxies=config.PROXY)
    try:
        result = json.loads(response.content)
        return result
    except:
        return False
    finally:
        response.close()
