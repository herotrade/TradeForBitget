import pandas as pd
import ta

import config
import test


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


import pandas as pd
import numpy as np

def calculate_indicators_and_signals(data, RSI_Period=14, SF=5, QQE=4.238):
    # Calculate difference
    delta = data['close'].diff()

    # RSI Calculation
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=RSI_Period, min_periods=RSI_Period).mean()
    avg_loss = loss.rolling(window=RSI_Period, min_periods=RSI_Period).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # EMA Calculation
    def ema(series, span):
        return series.ewm(span=span, adjust=False).mean()

    data['RsiMa'] = ema(data['RSI'], SF)

    # Rest of the calculations
    Wilders_Period = RSI_Period * 2 - 1
    AtrRsi = abs(data['RsiMa'].shift(1) - data['RsiMa'])
    MaAtrRsi = ema(AtrRsi, Wilders_Period)
    dar = ema(MaAtrRsi, Wilders_Period) * QQE
    data['FastAtrRsiTL'] = np.where(data['RSI'].shift(1) > dar.shift(1), np.maximum(dar.shift(1), data['RsiMa'] - dar), data['RsiMa'] + dar)
    data['QQExlong'] = (data['FastAtrRsiTL'].lt(data['RsiMa'])).astype(int).cumsum()
    data['QQExshort'] = (data['FastAtrRsiTL'].gt(data['RsiMa'])).astype(int).cumsum()
    data['QQExlong'] = data['QQExlong'] * (data['QQExlong'].shift(1) == 0)
    data['QQExshort'] = data['QQExshort'] * (data['QQExshort'].shift(1) == 0)

    # Calculate signals
    data['buy_signal'] = np.where((data['FastAtrRsiTL'] < data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) >= data['RsiMa'].shift(1)), 1, 0)
    data['sell_signal'] = np.where((data['FastAtrRsiTL'] > data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) <= data['RsiMa'].shift(1)), 1, 0)

    return data


### 当前策略判断多空单的时间不能小于5分钟，确认时间10秒钟或者20秒钟，可以高频连环做单
###
###

history = test.getHistory()


timestamp,open, high, low, close, volume = [],[],[],[],[],[]

for item in history:
    timestamp.append(item[0])
    open.append(float(item[1]))
    high.append(float(item[2]))
    low.append(float(item[3]))
    close.append(float(item[4]))
    volume.append(float(item[5]))

stock_data = pd.DataFrame(
    {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume})

singal = calculate_indicators_and_signals(stock_data, 5, 1, 4.238)
print(singal)
for i,v in enumerate(history):
    if singal['sell_signal'][i] == 1:
        print(f"在第 {i} 个时刻有一个做空信号。")
        print(singal['sell_signal'][i])
        history[i][1] = config.time2date(history[i][0])
        print(history[i])
    if singal['buy_signal'][i] == 1:
        print(f"在第 {i} 个时刻有一个做多信号。")
        print(singal['buy_signal'][i])
        history[i][1] = config.time2date(history[i][0])
        print(history[i])
print(config.time2date(history[0][0]))
print(config.time2date(history[-1][0]))