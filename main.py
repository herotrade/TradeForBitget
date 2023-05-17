# This Python file uses the following encoding: utf-8
import datetime
import json
import os
import time
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from net.WsKlineSubscription import WsKlineDataSubscription
from newui import Ui_Widget
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout)
from PySide6.QtGui import QGuiApplication
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import mplfinance as mpf
from Binance import Binance
from PySide6.QtCore import QTimer, Slot, QUrl
import config
import pandas as pd
from net.HistoryLine import StartKlineLoad
from net.Balance import Balance
from net.Rsi import Rsi
import threading


class Widget(QWidget):
    data = None
    init = 0  ##初始化
    initTime = 0  ##初始化
    WsInit = 0  ##初始化
    ExTime = 0
    _time = 0

    ##默认参数
    SYMBOL = "BTC"
    INTERVAL = "5m"

    ##form参数
    FORM = {
        "LEVER": 10,
        "MAX": 0,
        "SELL": 80,
        "BUY": 20,
        "TYPE": None,
        "_SELL": 5,
        "_BUY": 5,
        "AUTO": 50,
        "RATE": 5
    }

    BALANCE = {}
    ORDER = []
    login = {},
    session = None
    cookie = None

    ON_SHORT = False
    ON_LONG = False

    ON_SHORT_TIME = time.time()
    ON_LONG_TIME = time.time()

    ON_SHORT_SIGN_NUM = 0
    ON_LONG_SIGN_NUM = 0

    ON_START = 0  ##是否启动自动交易

    PROFIT_TYPE = 0
    PROFIT_MULT = 1  ##手续费止盈倍数

    DEFAULT_SIGN = 3  ##信号触发默认参数

    SIGN_DATA = None  ##信号数据
    NEW_PRICE = 0

    CANCEL_TIME = 0

    def __init__(self, parent=None):
        super().__init__(parent)

        self.insert = 0
        # if login is not None:
        #     self.login = [login]
        # if login is not None:
        #     config.PROXY['http'] = login['proxy']
        config.PROXY['http'] = "http://127.0.0.1:1087"

        self.worker = None
        self.axes = None
        self.canvas = None
        self.fig = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        # self.setFixedSize(1300, 1000)
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        center_point = screen_geometry.center()
        widget_geometry = self.geometry()
        widget_geometry.moveCenter(center_point)
        self.setGeometry(widget_geometry)
        self.setWindowTitle("基于python3 的高频计算多策略模型全自动量化交易工具 - 开发者Tg @chenmaq ")
        ##初始化k线图表
        self.KlineGen()
        ##订阅k线行情数据
        self.wsworker = WsKlineDataSubscription(self.SYMBOL, self.INTERVAL)
        self.wsworker.countChanged.connect(self.WsKileData)
        self.wsworker.start()
        ##同步币安服务器时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.execTime)
        self.timer.start(1000)
        ##加载个人数据
        self.balance = Balance()
        self.balance.signal.connect(self.updateBalance)
        self.balance.start()

        ##初始化rsi计算数据和网络
        self.rsi = Rsi(self.DEFAULT_SIGN)
        self.rsi.signal.connect(self.rsiValue)
        self.rsi.start()

        # ##切换币种事件
        self.ui.comboBox.currentTextChanged.connect(self.setSymbol)
        self.ui.comboBox_2.currentTextChanged.connect(self.setHourse)
        self.ui.comboBox_3.currentTextChanged.connect(self.setMode)
        # self.ui.label_7.setText(str(self.SYMBOL) + '/USDT')

        # self.ui.autocost.setText(str(self.FORM['AUTO']))
        self.ui.autocost.textChanged.connect(self.setAuto)
        self.ui.radioButton.clicked.connect(self.setProfitOne)
        self.ui.radioButton_2.clicked.connect(self.setProfitTwo)
        self.ui.lineEdit.textChanged.connect(self.setMult)
        self.ui.lineEdit_2.textChanged.connect(self.setAtrMult)
        self.ui.autocost_2.textChanged.connect(self.setProfitMult)
        self.ui.autocost_3.textChanged.connect(self.setPoint)
        # self.ui.pushButton.move(90,215)
        # self.ui.checkBox.stateChanged.connect(self.switchType)
        ###获取交易对，没必要

        self.ui.autobutton_2.clicked.connect(self.nowbuy)  ##现价做多
        self.ui.autobutton_5.clicked.connect(self.nowshot)  ##现价做空
        self.ui.autobutton_3.clicked.connect(self.nowpshort)  ##现价平空
        self.ui.autobutton_4.clicked.connect(self.nowplong)  ##现价平多

        self.ui.rate.textChanged.connect(self.setRate)  ##设置开仓比例

        self.ui.autobutton.clicked.connect(self.setState)

        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()  # 不能实例化为临时变量，否则被自动回收导致无法播放
        self.player.setAudioOutput(self.audioOutput)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.playbackStateChanged.connect(self.stateChanged)
        self.player.errorOccurred.connect(self._player_error)
        self.audioOutput.setVolume(1)
        self.play()

    def setRate(self, v):
        for i in self.balance.session:
            i.setRate(float(v))
            config.log(self.ui.loglist, "设置比例 %f" % (float(v)))
    def setPoint(self,v):
        for i in self.balance.session:
            i.setPoint(float(v))
        config.log(self.ui.loglist,"盈亏点位：%s" % str(v))
    def setProfitMult(self, v):
        self.PROFIT_MULT = float(v)
        for i in self.balance.session:
            i.setProfitMult(v)
        config.log(self.ui.loglist,"止盈比例：%f " % self.PROFIT_MULT)
        # self.balance.weex.setProfitMult(v)

    def setProfitOne(self, v):
        self.PROFIT_TYPE = 0
        config.log(self.ui.loglist, "已切换到分批止盈")

    def setProfitTwo(self, v):
        self.PROFIT_TYPE = 1
        config.log(self.ui.loglist, "已切换到手续费止盈")

    def setState(self):
        text = self.ui.autobutton.text()
        if text == "开始交易":
            self.ON_START = 1
            self.ui.autobutton.setText("停止交易")
            self.ui.label_2.setText("已开启自动交易")
        else:
            self.ui.autobutton.setText("开始交易")
            self.ON_START = 0

    def setAuto(self, val):
        try:
            for i in self.balance.session:
                i.setLossRate(val)
        except:
            pass

    def setAtrMult(self,v):
        self.rsi.changeATR(v)
        config.log(self.ui.loglist,"atr信号参数：%s" % str(v))

    def setMult(self, val):
        config.log(self.ui.loglist, "信号参数更改：%s" % str(val))
        self.rsi.changeMult(float(val))

    ##现价进场
    def nowbuy(self):
        try:
            t = "现价做多最新价格 %f" % self.NEW_PRICE
            config.log(self.ui.loglist, t)
            for i in self.balance.session:
                threading.Thread(target=i.buyLong, args=(self.NEW_PRICE, self.PROFIT_TYPE,)).start()
                # res = i.buyLong(self.FORM['AUTO'], self.NEW_PRICE, self.PROFIT_TYPE)
                config.log(self.ui.loglist, "手动做多" )
            self.play2()
        except Exception as e:
            config.log(self.ui.loglist, "现价做多执行错误 %s " % str(e))
            pass

    def nowshot(self):
        try:
            t = "现价做空最新价格 %f" % self.NEW_PRICE
            config.log(self.ui.loglist, t)
            for i in self.balance.session:
                threading.Thread(target=i.buyShort, args=(self.NEW_PRICE, self.PROFIT_TYPE,)).start()
                # res = i.buyShort(self.FORM['AUTO'], self.NEW_PRICE, self.PROFIT_TYPE)
                config.log(self.ui.loglist, "手动做空")
            self.play2()
        except Exception as e:
            config.log(self.ui.loglist, "现价做空执行错误 %s " % str(e))

    ##现价平空
    def nowpshort(self):
        try:
            print("现价平空")
            for i in self.balance.session:
                threading.Thread(target=i.pshort).start()
                # res = self.balance.weex.pshort(self.FORM['AUTO'])
                config.log(self.ui.loglist, "现价平空")
            self.ON_SHORT = False
        except Exception as e:
            config.log(self.ui.loglist, "现价平空执行错误 %s " % str(e))
            pass

    ##现价平多
    def nowplong(self):
        try:
            print("现价平多")
            for i in self.balance.session:
                threading.Thread(target=i.plong).start()
                # res = self.balance.weex.plong(self.FORM['AUTO'])
                config.log(self.ui.loglist, "现价平多")
            self.ON_LONG = False
        except Exception as e:
            config.log(self.ui.loglist, "现价平多执行错误 %s " % str(e))

    def rsiValue(self, data):
        self.ui.label_6.setText("RSI：" + str(config.num2(data['rsi'])))
        if float(data['rsi']) >= self.FORM['SELL'] - self.FORM['_SELL'] or float(data['rsi']) <= self.FORM['BUY'] + \
                self.FORM['_BUY']:
            self.play2()

        if data['short']:
            self.ui.siginList.setText("")
            self.SIGN_DATA = data
            self.ui.siginList.insertPlainText("最新信号：时间：%s 信号类型：%s 进场价格：%s 最新价格：%f" % (
                data['short']['time'], '做空', data['short']['map'], data['short']['newprice']) + "\r\n")
            self.ui.siginList.insertPlainText("最新信号：时间：%s 信号类型：%s 进场价格：%s  最新价格：%f" % (
                data['long']['time'], '做多', data['long']['map'], data['long']['newprice']))

            if self.ON_START == 0:
                self.ui.label_2.setText("未开启自动交易，已忽略信号")
                return

            ###检查当前信号方向和持仓是否匹配，若不匹配则平掉反方向的订单
            if data['long']['timestamp'] > data['short']['timestamp']:
                ##多单信号，则平掉空单，给60秒确认时间
                if self.ON_SHORT and self.CANCEL_TIME >= 60:
                    for hand in self.balance.session:
                        threading.Thread(target=hand.pshort).start()
                        self.CANCEL_TIME = 0
                        self.ON_SHORT = False
                        config.log(self.ui.loglist,"持仓方向与信号不符合，自动平掉空单")
                else:
                    if self.ON_SHORT:
                        print("持仓方向不一致，正在取消：%s" % (str(self.CANCEL_TIME)))
                        self.CANCEL_TIME += 1
            else:
                if self.ON_LONG and self.CANCEL_TIME >= 60:
                    for hand in self.balance.session:
                        threading.Thread(target=hand.plong).start()
                        self.CANCEL_TIME = 0
                        self.ON_LONG = False
                        config.log(self.ui.loglist, "持仓方向与信号不符合，自动平掉多单")
                else:
                    if self.ON_LONG:
                        print("持仓方向不一致，正在取消：%s" % (str(self.CANCEL_TIME)))
                        self.CANCEL_TIME += 1


            ###信号相差时间不能低于3分钟 ， 在信号确认里面也是
            if abs(data['short']['timestamp'] - data['long']['timestamp']) / 1000 <= 250:
                print("双信号时间过于接近: %d" % (
                        (int(data['long']['timestamp']) - int(data['short']['timestamp'])) / 1000))
                self.ON_LONG_SIGN_NUM = 0
                self.ON_SHORT_SIGN_NUM = 0
                return
            if data['short']['timestamp'] < data['long']['timestamp']:
                # 开多
                print("多单进入流程1")
                if self.ON_LONG:
                    print("已持有多单")
                    if time.time() - self.ON_LONG_TIME > 1800:
                        # self.ON_LONG = False
                        self.ON_LONG = False
                    return
                if config.equalDate(data['long']['timestamp'] / 1000, int(time.time())):
                    print("多单进入流程2")
                    if self.ON_LONG_SIGN_NUM < 50:
                        print("等待多单信号确认：%d" % self.ON_LONG_SIGN_NUM)
                        self.ON_LONG_SIGN_NUM += 1
                        return
                    if time.time() - self.ON_LONG_TIME >= 300:
                        print("多单进入下单流程")
                        for i in self.balance.session:
                            threading.Thread(target=i.buyLong, args=(data['long']['newprice'], self.PROFIT_TYPE,)).start()
                            # res = self.balance.weex.buyLong(self.FORM['AUTO'], data['long']['newprice'], self.PROFIT_TYPE)
                            config.log(self.ui.loglist, "自动做多 价格：%s" % (
                                str(str(data['long']['newprice']))))

                        self.ON_LONG_TIME = time.time()
                        self.ON_LONG = True  ##改变当前方向的持仓状态
                        self.ON_SHORT = False  ##改变对手单的持仓状态，使其可以开空单
                        self.ON_LONG_SIGN_NUM = 0
                        self.play2()
                else:
                    ###如果时间不相等，或者在持仓的状态中 让其30 分钟后可以开同方向的单子
                    if time.time() - self.ON_LONG_TIME > 1800:
                        # self.ON_LONG = False
                        self.ON_LONG_SIGN_NUM = 0
            else:
                print("进入空单流程")
                if self.ON_SHORT:
                    print("已持有空单")
                    if time.time() - self.ON_SHORT_TIME > 1800:
                        self.ON_SHORT = False
                    return
                ###已持仓的状态下，信号时间太接近不下单
                if config.equalDate(data['short']['timestamp'] / 1000, int(time.time())):
                    print("进入空单流程1")
                    if self.ON_SHORT_SIGN_NUM < 50:
                        print("等待空信号确认 ：%d" % self.ON_SHORT_SIGN_NUM)
                        self.ON_SHORT_SIGN_NUM += 1
                        return
                    if time.time() - self.ON_SHORT_TIME >= 300:
                        print("进入空单流程2")
                        for i in self.balance.session:
                            threading.Thread(target=i.buyShort, args=(data['short']['newprice'], self.PROFIT_TYPE,)).start()
                            # res = self.balance.weex.buyShort(self.FORM['AUTO'], data['short']['newprice'], self.PROFIT_TYPE)
                            config.log(self.ui.loglist, "自动做空-价格：%s" % (
                                 str(data['short']['newprice'])))
                        self.ON_SHORT_TIME = time.time()
                        self.ON_SHORT = True
                        self.ON_LONG = False
                        self.ON_SHORT_SIGN_NUM = 0
                        self.play2()
                else:
                    ### 其他时间检查当前状态是否可开空单，或者超过30分钟自动可以开空
                    if time.time() - self.ON_SHORT_TIME > 1800:
                        print("进入空单流程4，等待时间已过")
                        # self.ON_SHORT = False
                        self.ON_SHORT_SIGN_NUM = 0

    def updateBalance(self, type, data):
        if type == "assets":
            if int(data['code']) == 0:
                self.ui.loglist.insertPlainText("weex 登陆成功，开始自动交易\n")
            self.ui.label_25.setText(data['data']['contract']['totalUsdt'])
        # if type == "balance":
        #     usdt_balance = next(item for item in data['assets'] if item['asset'] == 'USDT')
        #     # print(usdt_balance)
        #     self.ui.label_25.setText(str(usdt_balance['availableBalance']))
        #     # self.ui.label_26.setText(str(usdt_balance['initialMargin']))
        #     # self.ui.label_29.setText(str(usdt_balance['unrealizedProfit']))
        #     # self.ui.label_27.setText(str('100 %'))
        #     self.BALANCE = usdt_balance

    @config.debounce(wait=0.3)
    def setLever(self, value):
        self.FORM['LEVER'] = value
        self.ui.label_19.setText(str(self.FORM['LEVER']))
        t = threading.Thread(target=self.balance.setLever, args=(int(value),))
        t.start()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # self._timer.start(1000)

    def setMode(self,v):
        if "ATR" in v:
            self.rsi.changeMode(2)
        if "QQE" in v:
            self.rsi.changeMode(3)
        if "MOVE" in v:
            self.rsi.changeMode(1)
        config.log(self.ui.loglist,"切换策略为 %s " % v)

    def setHourse(self, string):
        self.INTERVAL = string.replace("分钟", "").replace("小时", "")
        interval = int(self.INTERVAL)
        if int(self.INTERVAL) == 1:
            self.INTERVAL = str(1) + 'h'
        else:
            self.INTERVAL = str(self.INTERVAL) + 'm'
        config.log(self.ui.loglist, "交易时段切换为:" + self.INTERVAL.replace("m", "分钟").replace("h", "小时"))
        # self.wsworker.changed(self.SYMBOL,self.INTERVAL)
        self.data = []
        self.worker.changed(self.SYMBOL, self.INTERVAL)
        self.wsworker.changed(self.SYMBOL, self.INTERVAL)
        symbol = self.SYMBOL + "USDT"
        self.rsi.change(symbol, interval)

    ##切换币种事件
    def setSymbol(self, string):
        self.SYMBOL = str(string).replace("USDT", "")
        config.log(self.ui.loglist, "交易币种已切换为：" + self.SYMBOL)
        self.ui.label_7.setText(str(self.SYMBOL) + '/USDT')
        self.wsworker.changed(self.SYMBOL, self.INTERVAL)
        self.data = []
        self.worker.changed(self.SYMBOL, self.INTERVAL)
        self.rsi.unSubscription()
        symbol = self.SYMBOL + "USDT"
        interval = int(self.INTERVAL.replace('h','').replace('m',''))
        self.rsi.change(symbol, interval)
        for i in self.balance.session:
            i.setSymbol(self.SYMBOL.upper())
        # self.balance = Balance()
        # self.balance.change(self.SYMBOL + 'USDT')
        # self.balance.start()

    def getSymbolList(self):
        print("开始获取币种列表")
        ins = Binance()
        data = ins.client.exchange_info()
        print(data)
        assets = data['assets']
        symbols = data['symbols']
        for i in symbols:
            print(i)

    ##全局软件退出事件
    def closeEvent(self, event) -> None:
        print("be quite")
        try:
            self.wsworker.stop()
            self.rsi.unSubscription()
            # self.timer.stop()
            event.accept()
        except:
            pass

    def execTime(self):
        # self.dataWorker = SyncServerTime()
        # self.dataWorker.finished.connect(self.UpdateTime)
        # self.dataWorker.start()
        currentDateAndTime = datetime.datetime.now()
        self.ui.label.setText(currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S"))

    def UpdateTime(self, _time):
        self.ui.label.setText(config.time2dateM(_time['serverTime']))
        try:
            if self.initTime == 0:
                self.initTime = 1
                self.ui.loglist.insertPlainText(
                    "币安服务器时间同步完成：" + config.time2dateM(_time['serverTime']) + "\n")
        except:
            config.log(self.ui, "币安服务时间同步失败")
            pass

    ##接收ws的数据
    ##根据stream type 类型做分发处理
    def WsKileData(self, data):
        try:
            data = json.loads(data)
            self.WsInit = 1
            self.NEW_PRICE = float(data['data'][0]['last'])
            self.ui.label_5.setText("最新：" + str(data['data'][0]['last']))
            self.receptKlineTrade(data)
            #self.caluOrder(data['data']['p'])
        except:
            pass

    ##计算持仓的订单盈亏
    # @config.debounce(3)
    # def caluOrder(self, price):
    #     if len(self.ORDER) == 0:
    #         return
    #     sum = 0.0
    #     if abs(float(self.ORDER[0]['positionAmt']) * 10000) > 0:
    #         income = config.num2(
    #             float(self.ORDER[0]['positionAmt']) * (float(price) - float(self.ORDER[0]['entryPrice'])))
    #         self.ui.tableWidget.setItem(0, 6, QTableWidgetItem(income))
    #         sum += abs(float(income))
    #         print("1:" + str(income))
    #     if abs(float(self.ORDER[1]['positionAmt']) * 10000) > 0:
    #         income = config.num2(
    #             float(self.ORDER[1]['positionAmt']) * (float(price) - float(self.ORDER[1]['entryPrice'])))
    #         index = 0
    #         if abs(float(self.ORDER[0]['positionAmt'])) > 0:
    #             index = 1
    #         self.ui.tableWidget.setItem(index, 6, QTableWidgetItem(str(income)))
    #         sum += abs(float(income))
    #     self.ui.tableWidget.show()
    #     self.ui.label_29.setText(str(sum))

    def receptKlineTrade(self, data):

        try:
            # if data['arg']['instId'].lower() != self.SYMBOL.lower():
            #     return

            if int(time.time()) - self.ExTime >= 2:
                self.ExTime = int(time.time())
                self.update_data(data['data'][0])
                # print("重新渲染k线图：")
                # print("触发限流")
        except Exception as e:
            print(e)
            pass

    @config.debounce(1)
    ### 时时更新最新价格
    def update_data(self, data):
        timestamp = data['systemTime']

        price = float(data['last'])
        volume = float(data['quoteVolume'])

        lastData = self.data.iloc[-1]

        lastDate = config.time2date(lastData['Timestamp'])
        # lastDateArr = str(lastDate).split(':')

        nowDate = config.time2date(timestamp)
        # nowDateArr = str(nowDate).split(':')
        interval = self.INTERVAL.replace("m", "").replace("h", "")
        # print(abs(int(nowDateArr[1]) - int(lastDateArr[1])))
        # print()

        flag = 1  # 1更新 0 新增
        if float(timestamp) > float(lastData['Timestamp']):
            flag = 0
        if flag == 1:
            ###update
            self.data.loc[lastDate, 'Close'] = price
            self.data.loc[lastDate, 'Volume'] = volume + lastData['Volume']
            self.data.loc[lastDate, 'Open'] = lastData['Open']
            if lastData['High'] < price:
                self.data.loc[lastDate, 'High'] = price
            else:
                self.data.loc[lastDate, 'High'] = lastData['High']

            if lastData['Low'] > price:
                self.data.loc[lastDate, 'Low'] = price
            else:
                self.data.loc[lastDate, 'Low'] = lastData['Low']

            self.data.loc[lastDate, 'Timestamp'] = lastData['Timestamp']
            self.data.index.values[-1] = nowDate
            # print("update kline")
        else:
            self.data = self.data.iloc[1:]
            newData = {
                "Close": price,
                "Volume": volume,
                "Open": price,
                "High": price,
                "Low": price,
                "Timestamp": timestamp + (int(interval) * 60 * 1000),
                "Date": nowDate
            }
            d2 = pd.DataFrame(newData, index=[pd.to_datetime(nowDate)])
            self.data = pd.concat([self.data, d2])
            # print("insert kline")

        # 添加新数据
        # 获取最后一条数据，判断日期和分钟数是否和 分时做减大于等5 为新增，小于则更新
        self.CreateKile(self.data, None)

    ###生成k线
    def KlineGen(self):
        self.worker = StartKlineLoad(self.SYMBOL, self.INTERVAL)
        self.worker.fininshed.connect(self.CreateKile)
        self.worker.start()

    def CreateKile(self, data, today=None):
        try:
            self.data = data
            color = mpf.make_marketcolors(
                up='r',
                down='g',
                edge='inherit',
                wick='inherit',
                volume='inherit'
            )
            dstyle = mpf.make_mpf_style(
                base_mpf_style='binance',
                marketcolors=color,
            )
            if self.init == 0:
                print("kline init ")
                self.ui.loglist.insertPlainText("k线图表初始化完成\n")
                self.ui.label_3.setText('24H最高：$' + str(today['high24h']))
                self.ui.label_4.setText('24H最低：$' + str(today['low24h']))
                self.ui.kline.setContentsMargins(0, 0, 0, 0)
                layout = QVBoxLayout(self.ui.kline)
                layout.setContentsMargins(0, 0, 0, 0)

                self.fig = plt.Figure()
                self.fig.subplots_adjust(left=0.0, bottom=0, right=1, top=1)
                self.fig.set_facecolor("#eeeeee")

                self.canvas = FigureCanvas(self.fig)
                # canvas.setFixedSize(1000, 400)

                self.axes = self.fig.add_subplot(1, 1, 1)

                layout.addWidget(self.canvas)
                self.init = 1
                mpf.plot(data,
                         type="candle", ax=self.axes, style=dstyle, volume=False,
                         mav=(5, 10)
                         )
            else:
                if today is not None:
                    self.ui.label_3.setText('24H最高：$' + str(today['high24h']))
                    self.ui.label_4.setText('24H最低：$' + str(today['low24h']))
                self.axes.clear()
                mpf.plot(data,
                         type="candle", ax=self.axes, style=dstyle, volume=False,
                         mav=(5, 10)
                         )
                self.canvas.draw()
        except:
            pass

    @Slot()
    def positionChanged(self, position):
        pass

    @Slot()
    def durationChanged(self, duration):
        pass

    @Slot()
    def stateChanged(self, state):
        pass

    @Slot()
    def _player_error(self, error, error_string):
        print(error, error_string)

    @config.debounce(wait=15)
    def play(self):
        file = os.getcwd() + '/static/usenote.mp3'
        self.player.setSource(QUrl.fromLocalFile(file))
        self.player.play()

    @config.debounce(wait=15)
    def play2(self):
        file = os.getcwd() + '/static/y1201.wav'
        self.player.setSource(QUrl.fromLocalFile(file))
        self.player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    # apply_stylesheet(app, theme='dark_teal.xml')
    widget.show()
    sys.exit(app.exec())
