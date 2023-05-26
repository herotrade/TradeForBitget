import config
import test


import pandas as pd
import numpy as np
import talib


def generate_signals(df):
    RSI_Period = 5
    SF = 5
    QQE = 4.238

    src = df['close']  # Assuming 'close' is the name of a column in your DataFrame
    Wilders_Period = RSI_Period * 2 - 1

    Rsi = talib.RSI(src, timeperiod=RSI_Period)
    RsiMa = talib.EMA(Rsi, timeperiod=SF)
    AtrRsi = np.abs(RsiMa.shift(1) - RsiMa)
    MaAtrRsi = talib.EMA(AtrRsi, timeperiod=Wilders_Period)
    dar = talib.EMA(MaAtrRsi, timeperiod=Wilders_Period) * QQE

    longband = np.zeros_like(Rsi)
    shortband = np.zeros_like(Rsi)

    DeltaFastAtrRsi = dar
    RSIndex = RsiMa
    newshortband = RSIndex + DeltaFastAtrRsi
    newlongband = RSIndex - DeltaFastAtrRsi
    longband = np.where((RSIndex.shift(1) > longband.shift(1)) & (RSIndex > longband.shift(1)),
                        np.maximum(longband.shift(1), newlongband), newlongband)
    shortband = np.where((RSIndex.shift(1) < shortband.shift(1)) & (RSIndex < shortband.shift(1)),
                         np.minimum(shortband.shift(1), newshortband), newshortband)
    cross_1 = np.where(longband.shift(1) < RSIndex, 1, 0)
    trend = np.where(RSIndex < shortband.shift(1), 1,
                     np.where(cross_1 == 1, -1,
                              np.where(pd.notna(trend.shift(1)), trend.shift(1), 1)))
    FastAtrRsiTL = np.where(trend == 1, longband, shortband)

    # Find all the QQE Crosses
    QQExlong = np.zeros_like(Rsi)
    QQExshort = np.zeros_like(Rsi)
    QQExlong = np.where(pd.notna(QQExlong.shift(1)), QQExlong.shift(1), 0)
    QQExshort = np.where(pd.notna(QQExshort.shift(1)), QQExshort.shift(1), 0)
    QQExlong = np.where(FastAtrRsiTL < RSIndex, QQExlong + 1, 0)
    QQExshort = np.where(FastAtrRsiTL > RSIndex, QQExshort + 1, 0)

    # Conditions
    qqeLong = np.where(QQExlong == 1, FastAtrRsiTL.shift(1), np.nan)
    qqeShort = np.where(QQExshort == 1, FastAtrRsiTL.shift(1), np.nan)

    df['qqeLong'] = qqeLong
    df['qqeShort'] = qqeShort

    return df


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

sell_signal,buy_signal = generate_signals(stock_data)
for item in sell_signal['qqeLong']:
    print(item)
exit()
for i,v in enumerate(history):
    if singal['sell_signal'][i] == 1:
        print(f"在第 {i} 个时刻有一个做空信号。--------------------")
        print("fast rsi : %f" % singal['FastAtrRsiTL'][i])
        print("rsi ma : %f" % singal['RsiMa'][i])
        print("sub rsi - ma : %f" % float(singal['FastAtrRsiTL'][i] - singal['RsiMa'][i]))
        history[i][1] = config.time2date(history[i][0])
        print(history[i][1])
    if singal['buy_signal'][i] == 1:
        print(f"在第 {i} 个时刻有一个做多信号。-------------------")
        print("fast rsi : %f" % singal['FastAtrRsiTL'][i])
        print("rsi ma : %f" % singal['RsiMa'][i])
        print("sub ma -  rsi: %f" % float(singal['RsiMa'][i] - singal['FastAtrRsiTL'][i]))
        history[i][1] = config.time2date(history[i][0])
        print(history[i][1])

print("-----------------------")
print(config.time2date(history[0][0]))
print(config.time2date(history[-1][0]))