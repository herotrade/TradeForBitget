from PySide6.QtCore import QThread, Signal
from net.Binance import Binance

class SyncServerTime(QThread):
    finished = Signal(object)
    data = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = None
        self.cli = None

    def UpdateTime(self):
        try:
            cli = Binance()
            _time = cli.client.time()
            self.finished.emit(_time)
        except:
            pass

    def run(self) -> None:
        self.UpdateTime()
        self.exec()