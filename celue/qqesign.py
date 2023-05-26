### qqesign 做超高频率
import pandas as pd
import numpy as np

import config


def calculate_indicators_and_signals(data, RSI_Period=5, SF=5, QQE=4.238, ATR_Period=5):
    delta = data['close'].diff()
    # RSI Calculation
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=RSI_Period, min_periods=RSI_Period).mean()
    avg_loss = loss.rolling(window=RSI_Period, min_periods=RSI_Period).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # ATR Calculation
    high_low = data['high'] - data['low']
    high_close = np.abs(data['high'] - data['close'].shift())
    low_close = np.abs(data['low'] - data['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    data['ATR'] = true_range.rolling(ATR_Period).mean()

    # EMA Calculation
    def ema(series, span):
        return series.ewm(span=span, adjust=False).mean()

    data['RsiMa'] = ema(data['RSI'], SF)

    # Rest of the calculations
    Wilders_Period = RSI_Period * 2 - 1
    AtrRsi = abs(data['RsiMa'].shift(1) - data['RsiMa'])
    MaAtrRsi = ema(AtrRsi, Wilders_Period)
    dar = ema(MaAtrRsi, Wilders_Period) * QQE
    data['FastAtrRsiTL'] = np.where(data['RSI'].shift(1) > dar.shift(1), np.maximum(dar.shift(1), data['RsiMa'] - dar),
                                    data['RsiMa'] + dar)
    data['QQExlong'] = (data['FastAtrRsiTL'].lt(data['RsiMa'])).astype(int).cumsum()
    data['QQExshort'] = (data['FastAtrRsiTL'].gt(data['RsiMa'])).astype(int).cumsum()
    data['QQExlong'] = data['QQExlong'] * (data['QQExlong'].shift(1) == 0)
    data['QQExshort'] = data['QQExshort'] * (data['QQExshort'].shift(1) == 0)

    # Calculate signals
    # data['buy_signal'] = np.where(
    #     (data['FastAtrRsiTL'] < data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) >= data['RsiMa'].shift(1)), 1, 0)
    # data['sell_signal'] = np.where(
    #     (data['FastAtrRsiTL'] > data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) <= data['RsiMa'].shift(1)), 1, 0)
    threshold = data['ATR'].mean() * 1

    data['buy_signal'] = np.where(
        (data['FastAtrRsiTL'] < data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) >= data['RsiMa'].shift(1)) & (
                data['ATR'] > threshold), 1, 0)
    data['sell_signal'] = np.where(
        (data['FastAtrRsiTL'] > data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) <= data['RsiMa'].shift(1)) & (
                data['ATR'] > threshold), 1, 0)

    return data


### 当前策略判断多空单的时间不能小于5分钟，确认时间10秒钟或者20秒钟，可以高频连环做单

@config.debounce(1)
def QQEgetSign(params, mul=3):
    close = []
    hight = []
    low = []
    for i in params:
        close.append(float(i[4]))
        hight.append(float(i[2]))
        low.append(float(i[3]))
    stock_data = pd.DataFrame({"close": close, "high": hight, "low": low})
    result = calculate_indicators_and_signals(stock_data, 5, 5, 4.238,5)
    long = {}
    short = {}

    longSignList = []
    shortSignList = []

    for index, value in enumerate(close):
        if result['sell_signal'][index] == 1:
            short = {
                "time": config.time2date(params[index][0]),
                "timestamp": int(params[index][0]),
                "map": params[index][4],
                "sign": True,
                "per": "short"
            }
            # shortSignList.append(index)
        if result['buy_signal'][index] == 1:
            long = {
                "time": config.time2date(params[index][0]),
                "timestamp": int(params[index][0]),
                "map": params[index][4],
                "sign": True,
                "per": "long"
            }
            # longSignList.append(index)
    # params[shortSignList[-2]][0] = int(params[shortSignList[-2]][0])
    # if short['timestamp'] - int(params[shortSignList[-2]][0]) < (600 * 1000):
    #     short['time'] = config.time2date(params[shortSignList[-2]][0])
    #     short['timestamp'] = params[shortSignList[-2]][0]
    #     short['map'] = params[shortSignList[-2]][4]
    # if long['timestamp'] - int(params[longSignList[-2]][0]) < (600 * 1000):
    #     long['time'] = config.time2date(params[longSignList[-2]][0])
    #     long['timestamp'] = int(params[longSignList[-2]][0])
    #     long['map'] = params[longSignList[-2]][4]
    return short, long
