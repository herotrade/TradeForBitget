from binance.cm_futures import CMFutures
from binance.websocket.cm_futures.websocket_client import CMFuturesWebsocketClient
import config
import datetime
import pandas as pd
import websocket
import json
import ssl

class Binance:
    wsUrl = "wss://fstream.binance.com/ws/%s@kline_%s"
    flag = True
    temp = None

    def __init__(self):
        self.client = CMFutures(proxies=config.PROXY, key=config.KEY, secret=config.SECRET)

    def getInstance(self):
        return self.client

    def time2date(self, time):
        obj = datetime.datetime.fromtimestamp(int(float(time))/1000)
        formatted_date = obj.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    def dataFormat(self,data):
        data = pd.DataFrame(data)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index("Date", inplace=True)
        return data


    def getHistory(self,symbol='BTC',interval='5m',limit=100):
        _symbol = symbol + 'USD_PERP'
        response = self.client.klines(_symbol, interval,limit=limit)
        data = []
        for i in response:
            dic = {"Date": self.time2date(i[6]), "Open": float(i[1]), "High": float(i[2]), "Low": float(i[3]), "Close": float(i[4]),
                   "Volume": int(i[5]),"Timestamp":i[6]}
            data.append(dic)
        print(data[-1])
        return self.dataFormat(data)

    def createWsClient(self):
        self.ws_client = CMFuturesWebsocketClient()
        self.ws_client.start()
        print("ws client create success")

    def subscriptionContinueData(self,func,_pair='BTC'):
        self._symbol = _pair

        ws = websocket.WebSocketApp(
            "wss://fstream.binance.com/stream",
            on_message=func,
            on_ping=self.test,
            on_error=self.error
        )
        print("start open")
        ws.on_open = self.socketOpenSubContinue
        ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=1087, proxy_type='http',
                       sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

    def socketOpenSubContinue(self,ws):
        print(f"### open : {self._symbol} ###")
        _symbol = self._symbol.lower()
        sub_data = {
            "method": "SUBSCRIBE",
            "params": [f"{_symbol}usdt@aggTrade"],
            "id": 2
        }
        ws.send(json.dumps(sub_data))

    def unSubscription(self,ws):
        try:
            print("取消订阅" + self._symbol)
            sub_data = {
                "method": "UNSUBSCRIBE",
                "params": [f"{self._symbol.lower()}usdt@aggTrade"],
                "id": 2
            }
            ws.send(json.dumps(sub_data))
            print("取消成功 " + f"{self._symbol.lower()}usdt@aggTrade")
        except:
            pass

    def subscriptData(self,func,_symbol='BTCUSD_PERP',_interval='5m'):
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
        ws.run_forever(http_proxy_host='127.0.0.1',http_proxy_port=1087,proxy_type='http',sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

    def error(self,a,b):
        print("socket error")

    def pong(self,ws,data):
        print(ws)
        print(data)
        ws.send(json.dumps({
            "data": "pong"
        }))
        ws.pong(data)

    def test(self,ws,message):
        print("socket test")


    def socketOpen(self,ws):
        print("### open ###")
        sub_data = {
            "method": "SUBSCRIBE",
            "params": ["btcusdt@kline_1m"],
            "id": 1
        }
        ws.send(json.dumps(sub_data))

    def onKlineData(self,data):
        print(data)

