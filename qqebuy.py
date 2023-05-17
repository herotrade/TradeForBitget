# RSI_Period = input(14, title='RSI Length')
# SF = input(5, title='RSI Smoothing')
# QQE = input(4.238, title='Fast QQE Factor')
# ThreshHold = input(10, title="Thresh-hold")
#
# src = close
# Wilders_Period = RSI_Period * 2 - 1
#
# Rsi = rsi(src, RSI_Period)
# RsiMa = ema(Rsi, SF)
# AtrRsi = abs(RsiMa[1] - RsiMa)
# MaAtrRsi = ema(AtrRsi, Wilders_Period)
# dar = ema(MaAtrRsi, Wilders_Period) * QQE
#
# longband = 0.0
# shortband = 0.0
# trend = 0
#
# DeltaFastAtrRsi = dar
# RSIndex = RsiMa
# newshortband = RSIndex + DeltaFastAtrRsi
# newlongband = RSIndex - DeltaFastAtrRsi
# longband := RSIndex[1] > longband[1] and RSIndex > longband[1] ? max(longband[1], newlongband) : newlongband
# shortband := RSIndex[1] < shortband[1] and RSIndex < shortband[1] ? min(shortband[1], newshortband) : newshortband
# cross_1 = cross(longband[1], RSIndex)
# trend := cross(RSIndex, shortband[1]) ? 1 : cross_1 ? -1 : nz(trend[1], 1)
# FastAtrRsiTL = trend == 1 ? longband : shortband
#
# QQExlong = 0
# QQExlong := nz(QQExlong[1])
# QQExshort = 0
# QQExshort := nz(QQExshort[1])
# QQExlong := FastAtrRsiTL < RSIndex ? QQExlong + 1 : 0
# QQExshort := FastAtrRsiTL > RSIndex ? QQExshort + 1 : 0
#
#
# qqeLong = QQExlong == 1 ? FastAtrRsiTL[1] - 50 : na
# qqeShort = QQExshort == 1 ? FastAtrRsiTL[1] - 50 : na

import pandas as pd
import ta

import config
import test

import numpy as np
import talib

import numpy as np
import pandas as pd
from talib import RSI, EMA


def qqe(data, rsi_period=5, sf=3, qqe_factor=4.238):
    close = data['close']
    rsi = RSI(close, timeperiod=rsi_period)
    rsi_ma = EMA(rsi, timeperiod=sf)

    wilders_period = rsi_period * 2 - 1
    atr_rsi = np.abs(np.array(rsi_ma[1:]) - np.array(rsi_ma[:-1]))
    ma_atr_rsi = EMA(atr_rsi, timeperiod=wilders_period)
    dar = EMA(ma_atr_rsi, timeperiod=wilders_period) * qqe_factor

    longband = [0.0]
    shortband = [0.0]
    trend = [0]

    for i in range(1, len(rsi_ma)):
        newshortband = rsi_ma[i] + dar[i - 1]
        newlongband = rsi_ma[i] - dar[i - 1]

        if rsi_ma[i - 1] > longband[-1] and rsi_ma[i] > longband[-1]:
            longband.append(max(longband[-1], newlongband))
        else:
            longband.append(newlongband)

        if rsi_ma[i - 1] < shortband[-1] and rsi_ma[i] < shortband[-1]:
            shortband.append(min(shortband[-1], newshortband))
        else:
            shortband.append(newshortband)

        cross_1 = longband[-2] < rsi_ma[i]
        trend.append(1 if shortband[-2] > rsi_ma[i] else -1 if cross_1 else trend[-1])

    fast_atr_rsi_tl = [longband[i] if trend[i] == 1 else shortband[i] for i in range(len(trend))]
    qqexlong = [0]
    qqexshort = [0]

    for i in range(1, len(fast_atr_rsi_tl)):
        qqexlong.append(1 if fast_atr_rsi_tl[i] < rsi_ma[i] else 0)
        qqexshort.append(1 if fast_atr_rsi_tl[i] > rsi_ma[i] else 0)

    qqe_long = [fast_atr_rsi_tl[i - 1] - 60 if qqexlong[i] == 1 else np.nan for i in range(1, len(qqexlong))]
    qqe_short = [fast_atr_rsi_tl[i - 1] - 50 if qqexshort[i] == 1 else np.nan for i in range(1, len(qqexshort))]

    return qqe_long, qqe_short


history = test.getHistory()
print(config.time2date(history[0][0]))
print(config.time2date(history[-1][0]))
print(len(history))
# exit()
timestamp = []
open = []
high = []
low = []
close = []
volume = []
for item in history:
    timestamp.append(item[0])
    open.append(float(item[1]))
    high.append(float(item[2]))
    low.append(float(item[3]))
    close.append(float(item[4]))
    volume.append(float(item[5]))

stock_data = pd.DataFrame(
    {"timestamp": timestamp, "open": open, "high": high, "low": low, "close": close, "volume": volume})

# 调用函数计算交易信号
buy_signals,sell_signals = qqe(stock_data,5,3,4.0)

# print(buy_signals)
# exit()

###信号有连续性，在获取到新信号后判断

print()

for i in range(len(buy_signals)):
    if not np.isnan(buy_signals[i]) and buy_signals[i] > 0:
        print(f"在第 {i } 个时刻有一个做多信号。")
        print(buy_signals[i])
        history[i][1] = config.time2date(history[i][0])
        print(history[i])
exit()

print(sell_signals)
for i in range(len(sell_signals)):
    if not np.isnan(sell_signals[i]) :
        print(f"在第 {i } 个时刻有一个做空信号。")
        print(sell_signals[i])
        history[i][1] = config.time2date(history[i][0])
        print(history[i])
