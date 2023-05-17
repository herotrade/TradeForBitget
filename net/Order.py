from PySide6.QtCore import Signal, QThread

#自动下单的信号策略处理
class Order(QThread):
    ### 当接收到rsi 的入场信号后 属于超卖，则平仓多单，市价做多，实时获取盈亏持仓订单，根据盈亏比实时保证风险
    ### poitionrisk 接口的数据要放入线程进行实时计算盈亏
    ### 多单合约盈亏计算公式 开仓数量  / 开仓比特币价格 * (最新价格 - 开仓价格)
    ### 在positionrsik 接口有获取到成交数量， 通过成交数量 * （最新价格-开仓价格） = 实时盈亏
    ### 做空 空单的计算 成交量 * (开仓价格 - 最新价格) = 实时盈亏
    ### 低多 高空的策略 严格按照1：1的盈亏比例进行开单平仓 或者1:1.5 盈亏比例
    ### 计算持仓保证金公式  持仓数量(开仓金额 / 市场单价) * 开仓价格 / 合约倍数 = 保证金

    rsiValue = 0

    def __init__(self):
        super().__init__()

    def setRsi(self, value):
        self.rsiValue = value
