import hashlib
import hmac
import random
import time

import requests
from PySide6.QtCore import Signal, QThread,QTimer
import websocket
import json
import ssl
import datetime
import config
from urllib.parse import urlencode
import numpy as np

from bitget.consts import CONTRACT_WS_URL
from bitget.ws.bitget_ws_client import BitgetWsClient, SubscribeReq
from celue.RangeFilterBy5Min import getSign
from celue.super import sGetSign
from celue.qqesign import QQEgetSign
import traceback

class Rsi(QThread):
    signal = Signal(object)
    symbol = 'BTCUSDT'
    history = []
    url = "https://fapi.binance.com",
    last_time = None
    interval = 5
    ws = None
    ID = random.randint(1, 5)
    mult = 3
    atr_mult = 1
    init = False
    mode = 1

    wsH = 0
    wsL = 0

    connecting = False

    def __init__(self, _mult=3):
        self.mult = _mult
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateHistory)
        self.timer.start(20000)


    def changeMode(self, e):
        self.mode = e

    def change(self, _symbol, _interval):
        self.symbol = _symbol
        self.interval = _interval
        self.history = []
        print("rsi 切换参数 %s %d " % (self.symbol, self.interval))
        self.getHistory()
        self.onOpen(self.ws)

    def changeATR(self,v):
        self.atr_mult = float(v)

    def changeMult(self, value):
        self.mult = value

    def updateHistory(self):
        current_time = datetime.datetime.now()
        minutes = current_time.minute
        if minutes % 5 == 0:
            self.getHistory()
            self.init = False
            print("最新历史数据")
            print(self.history[-1])


    def getHistory(self):
        # 连续合约K线数据
        self.history = []
        endtime1 = time.time() * 1000
        start1 = endtime1 - (5 * 60 * 1000 * 1000)
        url1 = "https://api.bitget.com/api/mix/v1/market/candles?symbol=BTCUSDT_UMCBL&granularity=5m&startTime=%d&endTime=%d&limit=1000" % (start1,endtime1)
        response1 = requests.get(url1,proxies=config.PROXY)
        result1 = response1.json()

        endtime2 = start1
        start2 = endtime2 - (5 * 60 * 500 * 1000)
        url2 = "https://api.bitget.com/api/mix/v1/market/candles?symbol=BTCUSDT_UMCBL&granularity=5m&startTime=%d&endTime=%d&limit=1000" % (
        start2, endtime2)
        response2 = requests.get(url2, proxies=config.PROXY)
        result2 = response2.json()
        result2.extend(result1)
        self.history = result2
        print(len(self.history))
        # 解析返回结果
        print(config.time2date(self.history[0][0]))
        print(config.time2date(self.history[-1][0]))
        self.last_time = int(float(self.history[-1][0]) / 1000)

    def relative_strength(self, n=5):
        """
        compute the n period relative strength indicator
        http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
        http://www.investopedia.com/terms/r/rsi.asp
        """
        try:
            prices = [float(entry[4]) for entry in self.history]
            deltas = np.diff(prices)
            seed = deltas[:n + 1]
            up = seed[seed >= 0].sum() / n
            down = -seed[seed < 0].sum() / n
            rs = up / down
            rsi = np.zeros_like(prices)
            rsi[:n] = 100. - 100. / (1. + rs)

            for i in range(n, len(prices)):
                delta = deltas[i - 1]  # cause the diff is 1 shorter

                if delta > 0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up * (n - 1) + upval) / n
                down = (down * (n - 1) + downval) / n

                rs = up / down
                rsi[i] = 100. - 100. / (1. + rs)

            return rsi
        except:
            return [0]

    def connectWs(self):
        self.client = BitgetWsClient(CONTRACT_WS_URL, need_login=False) \
            .api_key("bg_8cbb2f6c33a2bf73290e7dfce84b6a08") \
            .api_secret_key("abc2a12838798d3775582fb30662776aab9bee906f554c63dc0a2c6716c8eb7d") \
            .passphrase("59420mc123") \
            .error_listener(self.error) \
            .build()
        self.channles = [SubscribeReq("mc", "ticker", "BTCUSDT")]
        self.client.subscribe(self.channles, self.onMessage)

        # ws = websocket.WebSocketApp(
        #     "wss://fstream.binance.com/stream",
        #     on_message=self.onMessage,
        #     on_ping=self.ping,
        #     on_error=self.error,
        #     on_pong=self.pong,
        #     on_close=self.close
        # )
        # print("rsi 计算网络链接线程")
        # ws.on_open = self.onOpen
        # ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=int(config.PROXY['http'].split(':')[2]),
        #                proxy_type='http',
        #                sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

    def onMessage(self, data):
        try:
            if len(self.history) == 0:
                return
            data = json.loads(data)
            times = int(float(data['data'][0]['systemTime']) / 1000)
            ##当前时间减去上次的数据时间大于标的间隔时间则更新数据
            price = float(data['data'][0]['last'])
            # print("time : %d last : %d",times,self.last_time)
            if not self.init:
                self.init = True
                self.history.append([data['data'][0]['systemTime'], 0, price, price, price])
                self.last_time = times
                self.wsH = price
                self.wsL = price
            # if times - self.last_time > self.interval * 60:
            #     self.history.pop(0)
            #     self.history.append([times * 1000, 0, price, price, price])
            #     self.last_time = times
            # else:
            if price > self.wsH:
                self.wsH = price
            if price < self.wsL:
                self.wsL = price
            self.history[-1] = [data['data'][0]['systemTime'], 0, self.wsH, self.wsL, price]
            rsi = self.relative_strength()

            try:
                if self.mode == 1:
                    short, long = getSign(self.history, self.mult)
                if self.mode == 2:
                    short, long = sGetSign(self.history,self.atr_mult)
                    short['newprice'] = price
                    long['newprice'] = price
                if self.mode == 3:
                    short,long = QQEgetSign(self.history)
                    short['newprice'] = price
                    long['newprice'] = price
            except Exception as e:
                short, long = False, False

            rd = {"rsi": rsi[-1], "short": short, "long": long}
            self.signal.emit(rd)
            del short, long, rd, rsi
        except Exception as e:
            print(e)
            pass

    def onOpen(self, ws):
        if not self.connecting:
            self.connecting = True
        print(f"rsi 计算数据建立链接 : %s" % self.symbol)
        self.ws = ws
        _symbol = self.symbol.lower()
        sub_data = {
            "method": "SUBSCRIBE",
            "params": [f"{_symbol}@aggTrade"],
            "id": self.ID
        }
        ws.send(json.dumps(sub_data))

        # print(f"rsi 计算数据建立链接 : eth")
        # _symbol = 'ethusdt'
        # sub_data = {
        #     "method": "SUBSCRIBE",
        #     "params": [f"{_symbol}@aggTrade"],
        #     "id": 44
        # }
        # ws.send(json.dumps(sub_data))

    def unSubscription(self):
        try:
            print("取消订阅" + self.symbol)
            self.client.unsubscribe(self.channles)
        except:
            pass
    @config.debounce(5)
    def close(self,*args,**kwargs):
        self.connecting = False
        while not self.connecting:
            print("rsi 计算网络断开链接，正在重新链接")
            try:
                self.getHistory()
                self.init = False
                self.connectWs()
            except:
                pass
            finally:
                time.sleep(5)
        print("rsi计算网络已重新链接")

    def pong(self, ws, data):
        try:
            ws.send(json.dumps({
                "data": "pong"
            }))
            ws.pong(data)
        except:
            pass

    def ping(self, ws, data):
        try:
            ws.send(json.dumps({
                "data": "ping"
            }))
            ws.pong(data)
        except:
            pass

    def error(self, ws, data):
        pass

    # 构造请求参数
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

    def run(self) -> None:
        self.getHistory()
        self.connectWs()
        self.exec()
