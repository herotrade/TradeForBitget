import datetime
import time

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

def calculate_indicators_and_signals(data, RSI_Period=4, SF=4, QQE=4.238,ATR_Period=5):
    # Calculate difference
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
    data['FastAtrRsiTL'] = np.where(data['RSI'].shift(1) > dar.shift(1), np.maximum(dar.shift(1), data['RsiMa'] - dar), data['RsiMa'] + dar)
    data['QQExlong'] = (data['FastAtrRsiTL'].lt(data['RsiMa'])).astype(int).cumsum()
    data['QQExshort'] = (data['FastAtrRsiTL'].gt(data['RsiMa'])).astype(int).cumsum()
    data['QQExlong'] = data['QQExlong'] * (data['QQExlong'].shift(1) == 0)
    data['QQExshort'] = data['QQExshort'] * (data['QQExshort'].shift(1) == 0)

    # Calculate signals
    threshold = data['ATR'].mean() * 1

    data['buy_signal'] = np.where(
        (data['FastAtrRsiTL'] < data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) >= data['RsiMa'].shift(1)) & (
                data['ATR'] > threshold), 1, 0)
    data['sell_signal'] = np.where(
        (data['FastAtrRsiTL'] > data['RsiMa']) & (data['FastAtrRsiTL'].shift(1) <= data['RsiMa'].shift(1)) & (
                data['ATR'] > threshold), 1, 0)
    return data


### 当前策略判断多空单的时间不能小于5分钟，确认时间10秒钟或者20秒钟，可以高频连环做单
###
###

data = test.getHistory()

timestamp,open, high, low, close, volume = [],[],[],[],[],[]

for item in data:
    timestamp.append(item[0])
    open.append(float(item[1]))
    high.append(float(item[2]))
    low.append(float(item[3]))
    close.append(float(item[4]))
    volume.append(float(item[5]))

stock_data = pd.DataFrame(
    {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume})

result = calculate_indicators_and_signals(stock_data, 5, 5, 4.238,5)
amount = 0
sindex = 0
bindex = 0
cont = 0
win = 0
loss = 0


amount2 = 0

day = 2

flag = 0

for i in range(0,len(data)):
    if result['sell_signal'][i] == True and int(data[i][0]) / 1000 + (86400 * day) > int(time.time()):
        current = datetime.datetime.fromtimestamp(int(data[i][0])/1000)
        scurrent = datetime.datetime.fromtimestamp(int(data[sindex][0])/1000)
        # if sindex > 0 and flag == 1 and abs(current.minute - scurrent.minute) <= 10:
        #     continue
        # if bindex > 0:
        #     btime = datetime.datetime.fromtimestamp(int(data[bindex][0])/1000)
        #     if abs(current.minute - btime.minute) < 3:
        #         continue

        cont += 1
        shortSign = {
            "time": config.time2date(data[i][0]),
            "timestamp": data[i][0],
            "map": data[i][4],
            "sign": True,
            "per": "short"
        }
        sindex = i
        max = 0
        if bindex > 0 and int(shortSign['timestamp']) / 1000 + (86400 * day) > int(time.time()):

            for ii in range(bindex,i):
                if float(data[ii][2]) > max:
                    max = float(data[ii][2])
            if max - float(data[bindex][4]) >= 30:
                amount += 30
                win+=30
            else:
                if float(float(data[i][4]) - float(data[bindex][4])) <= -30:
                    amount -= 30
                    loss -= 30
                    amount2 -= 30
                else:
                    amount += float(float(data[i][4]) - float(data[bindex][4]))
                    loss += float(float(data[i][4]) - float(data[bindex][4]))
                    amount2 += float(float(data[i][4]) - float(data[bindex][4]))

            if float(float(data[i][4]) - float(data[bindex][4])) <= -30:
                amount2 += -30
            else:
                amount2 += float(float(data[i][4]) - float(data[bindex][4]))


        print("有一个做空信号")
        print("与上一个信号的差值：%f 最大差值：%f" % (float(float(data[i][4]) - float(data[bindex][4])),(max - float(data[bindex][4]))))
        print("做多期间最高价格： %f 做多价格：%s " % (max,data[bindex][4]))
        print(shortSign)
        print("\n")
    if result['buy_signal'][i] == True and int(data[i][0]) / 1000 + (86400 * day) > int(time.time()):
        current = datetime.datetime.fromtimestamp(int(data[i][0])/1000)
        bcurrent = datetime.datetime.fromtimestamp(int(data[bindex][0])/1000)
        # if bindex > 0 and flag == 1 and abs(current.minute - bcurrent.minute) <= 5:
        #     continue
        # if sindex > 0:
        #     stime = datetime.datetime.fromtimestamp(int(data[sindex][0])/1000)
        #     if abs(current.minute - stime.minute < 3):
        #         continue
        cont += 1
        longSign = {
            "time": config.time2date(data[i][0]),
            "timestamp": data[i][0],
            "map": data[i][4],
            "sign": True,
            "per": "long",
        }
        bindex = i
        maxs = float(data[i][3])
        if sindex > 0 and int(longSign['timestamp']) / 1000 + (86400 * day) > int(time.time()):
            for ii in range(sindex, i):
                if float(data[ii][3]) < maxs:
                    maxs = float(data[ii][3])
            if (float(data[sindex][4]) - maxs) >= 30:
                amount += 30
                win += 30
            else:
                if float(float(data[sindex][4]) - float(data[i][4])) <= -30:
                    amount -= 30
                    loss -= 30
                else:
                    amount += float(float(data[sindex][4]) - float(data[i][4]))
                    loss += float(float(data[sindex][4]) - float(data[i][4]))
            if float(float(data[sindex][4]) - float(data[i][4])) <= -30:
                amount2 += -30
            else:
                amount2 +=float(float(data[sindex][4]) - float(data[i][4]))

        print("有一个做多信号")
        print("与上一个信号的差值：%f 最大差值：%f" % (float(float(data[sindex][4]) - float(data[i][4])),(float(data[sindex][4]) - maxs)))
        print("做空期间最高价格： %f 做多价格：%s " % (maxs,data[bindex][4]))
        print(longSign)
        print("\n")

print("固定止盈总共赚：%f"% float(amount))
print("做单数量：%d" % cont)
print("固定止盈 : %f 损单 %f " % (float(win),float(loss)))
print("自然止盈:%f" % float(amount2))
print(len(data))
print(config.time2date(data[0][0]))
print(config.time2date(data[-1][0]))