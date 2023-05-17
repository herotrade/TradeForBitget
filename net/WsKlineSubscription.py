from PySide6.QtCore import QThread, Signal
from net.Binance import Binance

class WsKlineDataSubscription(QThread):
    countChanged = Signal(object)
    is_running = True
    SYMBOL = None
    INTERVAL = None

    def __init__(self, _symbol, _interval):
        super().__init__()
        self.ws = None
        self.SYMBOL = _symbol
        self.INTERVAL = _interval

    def changed(self, _symbol, _interval):
        self.SYMBOL = _symbol
        self.INTERVAL = _interval
        self.is_running = False
        self.cli.unSubscription(self.ws)
        self.cli._symbol = _symbol
        self.cli.socketOpenSubContinue(self.ws)
        self.is_running = True

    def getKlineData(self):
        pass

    def onMessage(self, data):
        if not self.is_running:
            print("ws close")
            return
        self.countChanged.emit(data)

    def run(self):
        self.cli = Binance()
        # cli.subscriptData(self.onMessage)
        self.cli.subscriptionContinueData(self.onMessage, self.SYMBOL)
        self.exec()

    def stop(self):
        self.cli.unSubscription(self.ws)
        self.is_running = False