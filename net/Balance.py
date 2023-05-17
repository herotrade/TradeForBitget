import threading

from PySide6.QtCore import Signal, QThread
from net import Api
from net import config
from net.Weex import Weex

class Balance(QThread):
    signal = Signal(object, object)
    symbol = 'BTCUSDT'
    weex = None
    session = []
    user = {}

    def __init__(self):
        self.user = []
        super().__init__()
        #self.client = Binance()

        # self.otimer = QTimer(self)
        # self.otimer.timeout.connect(self.get_orders)
        # self.otimer.start(60000)

    def change(self,symbol='BTCUSDT'):
        self.symbol = symbol

    def balance(self):
        print("更新帐户余额信息")
        data = Api.account()#self.client.client.get_all_orders(symbol="BTCUSD_PERP")
        self.signal.emit('balance', data)

    def get_orders(self,symbol = 'BTCUSDT'):
        print("获取订单")
        data = Api.get_orders(self.symbol)
        #data = Api.getCjOrder(self.symbol)
        self.signal.emit('orders',data)

    def get_risk(self,symbol='BTCUSDT'):
        print("获取持仓风险")
        data = Api.positionRisk(self.symbol)
        self.signal.emit('risk',data)

    def get_trade_group(self,symbol = 'BTCUSDT'):
        print("获取盈亏")
        data = Api.trades_group(self.symbol)
        self.signal.emit('group',data)

    def setLever(self,num = 10):
        print("调整开仓杠杆")
        response = Api.setLever(num,self.symbol)
        self.signal.emit('set',response)

    def listenKey(self):
        print("生成key")
        key = Api.listenKey()
        print("生成keyvalue")
        print(key)

    #同一时间的类型数据更新
    @config.debounce(wait=60)
    def update(self):
        pass
        # try:
        #     self.balance()
        #     self.get_trade_group()
        #     self.get_risk()
        # except:
        #     pass

    def getAssets(self):
        weex = Weex()
        self.session.append(weex)

    def run(self):
        self.getAssets()
        # self.balance()
        # self.get_orders()
        # self.get_trade_group()
        # self.get_risk()
        #self.listenKey()
        #self.exec()

