import hashlib
import hmac
import json
import time
from datetime import datetime
from urllib.parse import urlencode

import pandas as pd
import requests
from PySide6.QtCore import QThread, Signal
from Binance import Binance
from net import config


class StartKlineLoad(QThread):
    fininshed = Signal(object, object)
    SYMBOL = None
    INTERVAL = None

    def __init__(self, _symbol, _interval):
        super().__init__()
        self.cli = None
        self.SYMBOL = _symbol
        self.INTERVAL = _interval

    def cleanNoneValue(slef, d) -> dict:
        out = {}
        for k in d.keys():
            if d[k] is not None:
                out[k] = d[k]
        return out

    def encoded_string(self, query, special=False):
        if special:
            return urlencode(query).replace("%40", "@").replace("%27", "%22")
        else:
            return urlencode(query, True).replace("%40", "@")

    def _prepare_params(self, params, special=False):
        return self.encoded_string(self.cleanNoneValue(params), special)

    def getHistory(self):
        # 连续合约K线数据
        interval = self.INTERVAL.replace("m", "") + "m"
        symbol = self.SYMBOL.replace("USDT", "") + "USDT"
        endtime = int(time.time()) * 1000
        start = endtime - (5 * 60 * 200 * 1000)
        url = "https://api.bitget.com/api/mix/v1/market/candles?symbol=%s_UMCBL&granularity=5m&startTime=%d&endTime=%d&limit=200" % (symbol,start,endtime)
        response = requests.get(url)
        # 解析返回结果
        try:
            return json.loads(response.content)
        except Exception as e:
            print("history load error : %s" % str(e))
            return []
        finally:
            response.close()

    def changed(self, _symbol, _interval):
        self.SYMBOL = _symbol
        self.INTERVAL = _interval
        self.getHisData()

    def dataFormat(self, data):
        data = pd.DataFrame(data)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index("Date", inplace=True)
        return data

    def time2date(self, time):
        obj = datetime.fromtimestamp(int(float(time)) / 1000)
        formatted_date = obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    def getHisData(self):
        self.cli = Binance()
        # data = self.cli.getHistory(self.SYMBOL, self.INTERVAL, 200)
        data = self.getHistory()
        temp = []
        for i in data:
            dic = {"Date": self.time2date(i[0]), "Open": float(i[1]), "High": float(i[2]), "Low": float(i[3]),
                   "Close": float(i[4]),
                   "Volume": float(i[5]), "Timestamp": i[0]}
            temp.append(dic)
        data = self.dataFormat(temp)

        response = requests.get("https://api.bitget.com/api/mix/v1/market/ticker?symbol=BTCUSDT_UMCBL")
        _today = response.json()
        self.fininshed.emit(data, _today['data'])

    def run(self) -> None:
        self.getHisData()
        # self.exec()
