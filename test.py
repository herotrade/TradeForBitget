# Periods = input(title="ATR Period", type=input.integer, defval=10)
# src = input(hl2, title="Source")
# Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
# changeATR= input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
# showsignals = input(title="Show Buy/Sell Signals ?", type=input.bool, defval=true)
# highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)
# atr2 = sma(tr, Periods)
# atr= changeATR ? atr(Periods) : atr2
# up=src-(Multiplier*atr)
# up1 = nz(up[1],up)
# up := close[1] > up1 ? max(up,up1) : up
# dn=src+(Multiplier*atr)
# dn1 = nz(dn[1], dn)
# dn := close[1] < dn1 ? min(dn, dn1) : dn
# trend = 1
# trend := nz(trend[1], trend)
# trend := trend == -1 and close > dn1 ? 1 : trend == 1 and close < up1 ? -1 : trend
# upPlot = plot(trend == 1 ? up : na, title="Up Trend", style=plot.style_linebr, linewidth=2, color=color.green)
# buySignal = trend == 1 and trend[1] == -1
# plotshape(buySignal ? up : na, title="UpTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.green, transp=0)
# plotshape(buySignal and showsignals ? up : na, title="Buy", text="Buy", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.green, textcolor=color.white, transp=0)
# dnPlot = plot(trend == 1 ? na : dn, title="Down Trend", style=plot.style_linebr, linewidth=2, color=color.red)
# sellSignal = trend == -1 and trend[1] == 1
# plotshape(sellSignal ? dn : na, title="DownTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.red, transp=0)
# plotshape(sellSignal and showsignals ? dn : na, title="Sell", text="Sell", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.red, textcolor=color.white, transp=0)
import datetime
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import pandas as pd
import numpy as np
import requests

from net import config
import xlwt


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


def getHistory():
    history = []
    # 连续合约K线数据
    url = "https://fapi.binance.com/fapi/v1/continuousKlines"
    params = {
        "pair": 'BTCUSDT',
        "contractType": "PERPETUAL",
        "interval": "1m",
        "incomeType": "REALIZED_PNL",
        "limit": 1500
    }
    now = datetime.datetime.now()
    params['endTime'] = int(now.timestamp() * 1000)
    params['startTime'] = params['endTime'] - (1 * 60 * 1500) * 1000
    string = _prepare_params(params=params)
    signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MBX-APIKEY": config.api_key}
    response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)
    # 解析返回结果
    try:
        # print(config.time2date(params['startTime']))
        # print(config.time2date(params['endTime']))
        # print(params)
        result = response.json()
        # print(config.time2date(result[0][0]))
        # print(config.time2date(result[-1][0]))
        history.extend(response.json())
        response.close()

        s = params['startTime']
        params['startTime'] = int(s - (1 * 60 * 1500) * 1000)
        params['endTime'] = int(s)
        string = _prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)

        r2 = response.json()
        r2.extend(history)


        s = params['startTime']
        params['startTime'] = int(s - (1 * 60 * 1500) * 1000)
        params['endTime'] = int(s)
        string = _prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)
        # print(config.time2date(params['startTime']))
        # print(config.time2date(params['endTime']))
        # print(params)
        # print(config.time2date(response.json()[0][0]))
        # print(config.time2date(response.json()[-1][0]))
        temp = response.json()
        temp.extend(r2)

        s = params['startTime']
        params['startTime'] = int(s - (1 * 60 * 1500) * 1000)
        params['endTime'] = int(s)
        string = _prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)

        r3 = response.json()
        r3.extend(temp)

        s = params['startTime']
        params['startTime'] = int(s - (1 * 60 * 1500) * 1000)
        params['endTime'] = int(s)
        string = _prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)

        r4 = response.json()
        r4.extend(r3)

        s = params['startTime']
        params['startTime'] = int(s - (1 * 60 * 1500) * 1000)
        params['endTime'] = int(s)
        string = _prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)

        r5 = response.json()
        r5.extend(r4)

        return r5

    except Exception as e:
        print(e)
        return False
    finally:
        response.close()


def calculate_atr(data, periods, multiplier, change_atr=True):
    data['tr'] = np.maximum(
        np.maximum(
            data['high'] - data['low'],
            np.abs(data['high'] - data['close'].shift(1))
        ),
        np.abs(data['low'] - data['close'].shift(1))
    )

    if change_atr:
        data['atr'] = data['tr'].rolling(window=periods).mean()
    else:
        data['atr'] = data['tr'].ewm(span=periods, adjust=False).mean()

    data['up'] = data['close'] - (multiplier * data['atr'])
    data['up1'] = data['up'].shift(1)
    data['up'] = np.where(data['close'].shift(1) > data['up1'], np.maximum(data['up'], data['up1']), data['up'])

    data['dn'] = data['close'] + (multiplier * data['atr'])
    data['dn1'] = data['dn'].shift(1)
    data['dn'] = np.where(data['close'].shift(1) < data['dn1'], np.minimum(data['dn'], data['dn1']), data['dn'])

    data['trend'] = np.nan
    data.loc[0, 'trend'] = 1

    for i in range(1, len(data)):
        if data.loc[i - 1, 'trend'] == -1 and data.loc[i, 'close'] > data.loc[i, 'dn1']:
            data.loc[i, 'trend'] = 1
        elif data.loc[i - 1, 'trend'] == 1 and data.loc[i, 'close'] < data.loc[i, 'up1']:
            data.loc[i, 'trend'] = -1
        else:
            data.loc[i, 'trend'] = data.loc[i - 1, 'trend']

    data['buy_signal'] = (data['trend'] == 1) & (data['trend'].shift(1) == -1)
    data['sell_signal'] = (data['trend'] == -1) & (data['trend'].shift(1) == 1)
    return data


if __name__ == "__main__":
    kline = getHistory()
    print(config.time2date(kline[0][0]))
    print(config.time2date(kline[-1][0]))
    print(len(kline))
    high = []
    low = []
    close = []
    for i in kline:
        high.append(float(i[2]))
        low.append(float(i[3]))
        # src = (float(i[2]) + float(i[3])) / 2
        close.append(float(i[4]))
    params = pd.DataFrame({"high": high, "low": low, "close": close})
    data = calculate_atr(params, 10, 1, False)  ##经过验证的 参数1.1
    longSign = {}
    shortSign = {}
    for i, v in enumerate(data['trend']):
        if data['sell_signal'][i]:
            print("做空")
            kline[i][0] = config.time2date(kline[i][0])
            print(kline[i])
        if data['buy_signal'][i]:
            print("做多")
            kline[i][0] = config.time2date(kline[i][0])
            print(kline[i])
