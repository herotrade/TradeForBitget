import random
import time
from urllib.parse import urlencode

import requests
from binance.cm_futures import CMFutures
from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
import config
import datetime
import pandas as pd
import websocket
import json
import ssl

from bitget.consts import CONTRACT_WS_URL
from bitget.ws.bitget_ws_client import BitgetWsClient, SubscribeReq



class Binance:
    wsUrl = "wss://fstream.binance.com/ws/%s@kline_%s"
    flag = True
    temp = None
    ID = random.randint(6, 9)

    connect = False

    def __init__(self):
        self._symbol = None
        self.callback = None
        self.last_time = None
        self.history = None
        self.client = CMFutures(proxies=config.PROXY, key=config.KEY, secret=config.SECRET)

    def getInstance(self):
        return self.client

    def time2date(self, time):
        obj = datetime.datetime.fromtimestamp(int(float(time)) / 1000)
        formatted_date = obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    def dataFormat(self, data):
        data = pd.DataFrame(data)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index("Date", inplace=True)
        return data

    def getHistory(self, symbol='BTC', interval='5m', limit=200):
        _symbol = symbol + 'USD_PERP'
        print("interval = :" + interval)
        response = self.client.klines(_symbol, interval, limit=limit)
        data = []
        for i in response:
            dic = {"Date": self.time2date(i[6]), "Open": float(i[1]), "High": float(i[2]), "Low": float(i[3]),
                   "Close": float(i[4]),
                   "Volume": int(i[5]), "Timestamp": i[6]}
            data.append(dic)
        print("interval = :" + interval)
        return self.dataFormat(data)

    def createWsClient(self):
        self.ws_client = CMFuturesWebsocketClient()
        self.ws_client.start()
        print("ws client create success")

    def _prepare_params(self, params, special=False):
        return self.encoded_string(self.cleanNoneValue(params), special)

    def encoded_string(self, query, special=False):
        if special:
            return urlencode(query).replace("%40", "@").replace("%27", "%22")
        else:
            return urlencode(query, True).replace("%40", "@")

    def cleanNoneValue(slef, d) -> dict:
        out = {}
        for k in d.keys():
            if d[k] is not None:
                out[k] = d[k]
        return out

    def getHistory(self):
        # 连续合约K线数据
        url = "https://fapi.binance.com/fapi/v1/continuousKlines"
        params = {
            "pair": "BTCUSDT",
            "contractType": "PERPETUAL",
            "interval": "5m",
            "incomeType": "REALIZED_PNL",
            "limit": 1500
        }
        now = datetime.datetime.now()
        past = now - datetime.timedelta(days=5)
        # start = int(past.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        # params['startTime'] = start * 1000
        params['endTime'] = int(now.timestamp() * 1000)
        params['startTime'] = params['endTime'] - (86400 * 5) * 1000
        string = self._prepare_params(params=params)
        signature = hmac.new(config.api_secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).hexdigest()
        params["signature"] = signature
        headers = {"X-MBX-APIKEY": config.api_key}
        response = requests.get(url, headers=headers, params=params, proxies=config.PROXY)
        # 解析返回结果
        try:
            result = json.loads(response.content)
            print(config.time2date(result[0][0]))
            print(config.time2date(result[-1][0]))
            print(result[0][4])
            print(result[-1][4])
            self.history = result
            self.last_time = int(float(result[-1][6]) / 1000)
        except Exception as e:
            print(e)
            return False
        finally:
            response.close()

    def subscriptionContinueData(self, func, _pair='BTC'):

        self.callback = func
        self._symbol = _pair

        self.client = BitgetWsClient(CONTRACT_WS_URL, need_login=False) \
            .api_key("bg_8cbb2f6c33a2bf73290e7dfce84b6a08") \
            .api_secret_key("abc2a12838798d3775582fb30662776aab9bee906f554c63dc0a2c6716c8eb7d") \
            .passphrase("59420mc123") \
            .error_listener(self.error) \
            .build()
        self.channles = [SubscribeReq("mc", "ticker", "BTCUSDT")]
        self.client.subscribe(self.channles, func)
        # ws = websocket.WebSocketApp(
        #     "wss://ws.bitget.com/mix/v1/stream",
        #     on_message=func,
        #     on_ping=self.test,
        #     on_error=self.error,
        #     on_close=self.close
        # )
        # ws.on_open = self.socketOpenSubContinue
        # ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=int(config.PROXY['http'].split(':')[2]),
        #                proxy_type='http',
        #                sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})
        return True

    def bgMessage(self,data):
        print("messaege")
        print(data)


    def socketOpenSubContinue(self, ws):
        if not self.connect:
            self.connect = True
        print(f"### open : {self._symbol} ###")
        _symbol = self._symbol.lower()
        sub_data = {
            "method": "SUBSCRIBE",
            "params": [f"{_symbol}usdt@aggTrade"],
            "id": self.ID
        }
        ws.send(json.dumps(sub_data))
        # lk = listenKey()['listenKey']
        # data = {"method": "SUBSCRIBE", "params": [lk], "id": 3}
        # payload = json.dumps(data)
        # ws.send(payload)
        # print(f"### open : ETH ###")
        #
        # _symbol = 'eth'
        # sub_data = {
        #     "method": "SUBSCRIBE",
        #     "params": [f"{_symbol}usdt@aggTrade"],
        #     "id": 20
        # }
        # ws.send(json.dumps(sub_data))

    def unSubscription(self, ws):
        try:
            self.client.unsubscribe(self.channles)
            print("ws 取消订阅 success")
        except:
            print("ws 取消订阅 error")
            pass
        # try:
        #     print("取消订阅" + self._symbol)
        #     sub_data = {
        #         "method": "UNSUBSCRIBE",
        #         "params": [f"{self._symbol.lower()}usdt@aggTrade"],
        #         "id": self.ID
        #     }
        #     ws.send(json.dumps(sub_data))
        #     print("取消成功 " + f"{self._symbol.lower()}usdt@aggTrade")
        # except:
        #     pass

    def subscriptData(self, func, _symbol='BTCUSD_PERP', _interval='5m'):
        # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',1080)
        # socket.socket = socks.socksocket
        ws = websocket.WebSocketApp(
            "wss://fstream.binance.com/stream",
            on_message=func,
            on_open=self.socketOpen,
            on_ping=self.test,
            on_error=self.error,
            on_pong=self.pong
        )
        print("start open")
        ws.on_open = self.socketOpen
        ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=1087, proxy_type='http',
                       sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

    @config.debounce(5)
    def close(self,*args,**kwargs):
        self.connect = False
        while not self.connect:
            try:
                print("行情数据ws 断开准备重新链接")
                self.subscriptionContinueData(self.callback, self._symbol)
            except:
                pass
            finally:
                time.sleep(5)
        print("已重新建立链接")
    def error(self):
        #print("socket error")
        print("bg socket connect error")
        pass

    def pong(self, ws, data):
        print(ws)
        print(data)
        ws.send(json.dumps({
            "data": "pong"
        }))
        ws.pong(data)

    def test(self, ws, messagteste):
        print("socket test")

    def socketOpen(self, ws):
        print("### open ###")
        sub_data = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@kline_1m"],
            "id": 1
        }
        ws.send(json.dumps(sub_data))

    def onKlineData(self, data):
        print(data)
