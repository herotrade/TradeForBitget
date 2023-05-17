# binanceRobot
基于币安交易所的加密数字货币合约量化交易机器人
请自动添加config.py 文件，位于根目录下面，文件内容，必须添加apikey 与secret 才能正常运行软件
######
######
import datetime
import pandas as pd
import time

KEY = ''  #币安api key
SECRET = '' #币安apisecret

PROXY = {
    'http': 'http://127.0.0.1:1087' ##fgw 内网络代理配置
}

###一些常用的函数

def time2date(time):
    obj = datetime.datetime.fromtimestamp(int(float(time)) / 1000)
    formatted_date = obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def time2dateM(_time):
    obj = datetime.datetime.fromtimestamp(int(int(_time) / 1000))
    return str(obj.date()) + ' ' + str(obj.time())


def dataFormat(data):
    data = pd.DataFrame(data)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index("Date", inplace=True)
    return data


def log(ui, msg):
    obj = datetime.datetime.fromtimestamp(int(float(time.time())))
    ui.insertPlainText(f"{msg}：" + str(obj.date()) + ' ' + str(obj.time()) + "\n")


def debounce(wait):
    def decorator(fn):
        last_time = 0

        def debounced(*args, **kwargs):
            nonlocal last_time
            now = time.monotonic()
            if now - last_time >= wait:
                last_time = now
                return fn(*args, **kwargs)

        return debounced

    return decorator


def num2(number):
    formt_ed = "{:.2f}".format(float(number))
    return formt_ed
#####  公共参数信息
# PERPETUAL 永续合约标识
# FUTURE 期货
# PENDING_TRADING 待上市
# TRADING 交易中
# PRE_DELIVERING 预交割
# DELIVERING 交割中
# DELIVERED 已交割
# PRE_SETTLE 预结算
# SETTLING 结算中
# CLOSE 已下架

##订单状态
# NEW 新建订单
# PARTIALLY_FILLED 部分成交
# FILLED 全部成交
# CANCELED 已撤销
# REJECTED 订单被拒绝
# EXPIRED 订单过期(根据timeInForce参数规则)


# 订单种类
# LIMIT 限价单
# MARKET 市价单
# STOP 止损限价单
# STOP_MARKET 止损市价单
# TAKE_PROFIT 止盈限价单
# TAKE_PROFIT_MARKET 止盈市价单
# TRAILING_STOP_MARKET 跟踪止损单

# 订单方向
# BUY 买入
# SELL 卖出

# 持仓方向
# BOTH 单一持仓方向
# LONG 多头(双向持仓下)
# SHORT 空头(双向持仓下)

# 有效方式
# GTC - Good Till Cancel 成交为止
# IOC - Immediate or Cancel 无法立即成交(吃单)的部分就撤销
# FOK - Fill or Kill 无法全部立即成交就撤销
# GTX - Good Till Crossing 无法成为挂单方就撤销
