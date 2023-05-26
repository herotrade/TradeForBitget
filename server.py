import hashlib
import hmac
import random
import threading
import time

import requests
import websocket
import json
import ssl
import datetime
import config
from urllib.parse import urlencode
import numpy as np
from celue.RangeFilterBy5Min import getSign
from celue.super import sGetSign
from celue.qqesign import QQEgetSign
from net.Weex import Weex
from test import getHistory


class Rsi():
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

    ON_SHORT = False
    ON_LONG = False

    ON_SHORT_TIME = time.time()
    ON_LONG_TIME = time.time()

    ON_SHORT_SIGN_NUM = 0
    ON_LONG_SIGN_NUM = 0

    ON_START = 0  ##是否启动自动交易

    PROFIT_TYPE = 1
    PROFIT_MULT = 1  ##手续费止盈倍数

    DEFAULT_SIGN = 3  ##信号触发默认参数

    SIGN_DATA = None  ##信号数据
    NEW_PRICE = 0

    CANCEL_TIME = 0

    OPEN_PRICE = 0

    ORDER_AMOUNT = 0
    ###分批止盈数据记录
    PAMOUNT = 0

    session = []

    def __init__(self, _mult=3):
        self.logger = None
        self.mult = _mult
        super().__init__()
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.updateHistory)
        # self.timer.start(20000)

    def changeMode(self, e):
        self.mode = e

    def change(self, _symbol, _interval):
        self.symbol = _symbol
        self.interval = _interval
        self.history = []
        print("rsi 切换参数 %s %d " % (self.symbol, self.interval))
        self.getHistory()
        self.onOpen(self.ws)

    def changeATR(self, v):
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
        result = getHistory()
        print(config.time2date(result[0][0]))
        print(config.time2date(result[-1][0]))
        self.history = []
        self.history = result
        self.last_time = int(float(result[-1][6]) / 1000)
        return self.history
        # 连续合约K线数据
        url = "https://fapi.binance.com/fapi/v1/continuousKlines"
        params = {
            "pair": self.symbol,
            "contractType": "PERPETUAL",
            "interval": "%sm" % str(self.interval),
            "incomeType": "REALIZED_PNL",
            "limit": 1500
        }
        now = datetime.datetime.now()
        params['endTime'] = int(now.timestamp() * 1000)
        params['startTime'] = params['endTime'] - (86400 * 5.15) * 1000
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
            self.history = []
            self.history = result
            self.last_time = int(float(result[-1][6]) / 1000)
        except Exception as e:
            print(e)
            return False
        finally:
            response.close()

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
        ws = websocket.WebSocketApp(
            "wss://fstream.binance.com/stream",
            on_message=self.onMessage,
            on_ping=self.ping,
            on_error=self.error,
            on_pong=self.pong,
            on_close=self.close
        )
        print("rsi 计算网络链接线程")
        ws.on_open = self.onOpen
        ws.run_forever(http_proxy_host='127.0.0.1', http_proxy_port=int(config.PROXY['http'].split(':')[2]),
                       proxy_type='http',
                       sslopt={"cert_reqs": ssl.CERT_NONE, "ssl_version": ssl.PROTOCOL_TLSv1_2})

    def onMessage(self, ws, data):
        try:
            if len(self.history) == 0:
                return
            data = json.loads(data)
            times = int(float(data['data']['E']))
            ##当前时间减去上次的数据时间大于标的间隔时间则更新数据
            price = float(data['data']['p'])
            # print("time : %d last : %d",times,self.last_time)

            lasttimestamp = datetime.datetime.fromtimestamp(int(self.history[-1][0]) / 1000)
            currenttime = datetime.datetime.fromtimestamp(times / 1000)

            flag = 0  # 0更新 1新增
            if int(currenttime.minute) > int(lasttimestamp.minute):
                flag = 1
                self.wsH = price
                self.wsL = price
                print("新时段k线 数量:%d" % len(self.history))
                print("before first : %s " % str(config.time2date(self.history[0][0])))
                print("before last : %s " % str(config.time2date(self.history[-1][0])))
            if currenttime.hour > lasttimestamp.hour:
                flag = 1
                self.wsH = price
                self.wsL = price
                print("新时段k线 数量:%d" % len(self.history))
                print("before first : %s " % str(config.time2date(self.history[0][0])))
                print("before last : %s " % str(config.time2date(self.history[-1][0])))
            if currenttime.day > lasttimestamp.day:
                flag = 1
                self.wsH = price
                self.wsL = price
                print("新时段k线 数量:%d" % len(self.history))
                print("before first : %s " % str(config.time2date(self.history[0][0])))
                print("before last : %s " % str(config.time2date(self.history[-1][0])))

            if not self.init:
                self.init = True
                self.history.pop(0)
                self.history.append([data['data']['E'], 0, price, price, price])
                self.last_time = times
                self.wsH = price
                self.wsL = price
            else:
                if flag == 1:
                    self.history.pop(0)
                    last = self.history[-1]
                    last[0] = times
                    self.history[-1] = last
                    self.history.append([times, 0, price, price, price])
                    print("k线新增完成 数量  :%d" % len(self.history))
                    print("before first : %s " % str(config.time2date(self.history[0][0])))
                    print("before last : %s " % str(config.time2date(self.history[-1][0])))

                    print("最新三根k线价格情况")
                    print(
                        "-2 hight：%f low：%f close：%f" % (self.history[-2][2], self.history[-2][3], self.history[-2][4]))
                    print(
                        "-3 hight：%f low：%f close：%f" % (self.history[-3][2], self.history[-3][3], self.history[-3][4]))
                    print(
                        "-4 hight：%f low：%f close：%f" % (self.history[-4][2], self.history[-4][3], self.history[-4][4]))
                if flag == 0:
                    if price > self.wsH:
                        self.wsH = price
                    if price < self.wsL:
                        self.wsL = price
                    self.history[-1] = [times, 0, self.wsH, self.wsL, price]

            rsi = self.relative_strength()

            try:
                if self.mode == 1:
                    short, long = getSign(self.history, self.mult)
                if self.mode == 2:
                    short, long = sGetSign(self.history, self.atr_mult)
                    short['newprice'] = price
                    long['newprice'] = price
                if self.mode == 3:
                    short, long = QQEgetSign(self.history)
                    short['newprice'] = price
                    long['newprice'] = price
            except Exception as e:
                # print(e)
                short, long = False, False

            rd = {"rsi": rsi[-1], "short": short, "long": long}
            self.order(rd)
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
            sub_data = {
                "method": "UNSUBSCRIBE",
                "params": [f"{self.symbol.lower()}@aggTrade"],
                "id": self.ID
            }
            self.ws.send(json.dumps(sub_data))
            print("取消成功 " + f"{self.symbol.lower()}@aggTrade")
        except:
            pass

    @config.debounce(5)
    def close(self, *args, **kwargs):
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
        self.initLog()
        self.initWeex()
        self.getHistory()
        self.connectWs()

    def initLog(self):
        from net import config
        lp = config.time2date(time.time() * 1000)
        self.logger = config.logger_config(log_path="./signal.txt", logging_name='')
        self.logger.info("信号日志文件初始化成功")

    def initWeex(self):
        weex = Weex()
        self.session.append(weex)

    def order(self, data):
        if data['short']:
            nowtime = datetime.datetime.fromtimestamp(int(time.time()))
            if data['short']['timestamp'] < data['long']['timestamp']:
                # 开多
                if self.ON_LONG:
                    print("已持有多单")
                    if time.time() - self.ON_LONG_TIME > 1800:
                        # self.ON_LONG = False
                        self.ON_LONG = False
                    return
                signTime = datetime.datetime.fromtimestamp(int(data['long']['timestamp']) / 1000)
                if signTime.hour == nowtime.hour and signTime.minute == nowtime.minute and signTime.second > 50 and not self.ON_LONG:
                    self.logger.info("多单下单")
                    self.ON_LONG_TIME = time.time()
                    self.ON_LONG = True  ##改变当前方向的持仓状态
                    self.ON_SHORT = False  ##改变对手单的持仓状态，使其可以开空单
                    self.ON_LONG_SIGN_NUM = 0

                    self.OPEN_PRICE = float(data['long']['newprice'])
                    for i in self.session:
                        threading.Thread(target=i.buyLong, args=(data['long']['newprice'], self.PROFIT_TYPE,)).start()
                    self.logger.info("自动做多 价格：%s" % (
                        str(str(data['long']['newprice']))))
                else:
                    ###如果时间不相等，或者在持仓的状态中 让其30 分钟后可以开同方向的单子
                    if time.time() - self.ON_LONG_TIME > 1800:
                        # self.ON_LONG = False
                        self.ON_LONG_SIGN_NUM = 0
            else:
                if self.ON_SHORT:
                    print("已持有空单")
                    if time.time() - self.ON_SHORT_TIME > 1800:
                        self.ON_SHORT = False
                    return
                ###已持仓的状态下，信号时间太接近不下单
                signTime = datetime.datetime.fromtimestamp(int(data['short']['timestamp']) / 1000)
                if signTime.hour == nowtime.hour and signTime.minute == nowtime.minute and signTime.second > 50 and not self.ON_SHORT:
                    self.logger.info("空单下单")
                    self.ON_SHORT_TIME = time.time()
                    self.ON_SHORT = True
                    self.ON_LONG = False
                    self.ON_SHORT_SIGN_NUM = 0
                    self.OPEN_PRICE = float(data['short']['newprice'])
                    for i in self.session:
                        threading.Thread(target=i.buyShort, args=(data['short']['newprice'], self.PROFIT_TYPE,)).start()
                    self.logger.info("自动做空-价格：%s" % (
                        str(data['short']['newprice'])))
                else:
                    ### 其他时间检查当前状态是否可开空单，或者超过30分钟自动可以开空
                    if time.time() - self.ON_SHORT_TIME > 1800:
                        # self.ON_SHORT = False
                        self.ON_SHORT_SIGN_NUM = 0


if __name__ == "__main__":
    rsi = Rsi()
    rsi.run()
