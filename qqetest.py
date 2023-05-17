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

import pandas as pd
import numpy as np
import talib as ta


def qqe(data, rsi_period=14, sf=5, qqe=4.238):
    data['rsi'] = ta.RSI(data['close'], timeperiod=rsi_period)
    data['rsi_ma'] = ta.EMA(data['rsi'], timeperiod=sf)
    data['atr_rsi'] = abs(data['rsi_ma'].shift(1) - data['rsi_ma'])
    wilders_period = rsi_period * 2 - 1
    data['ma_atr_rsi'] = ta.EMA(data['atr_rsi'], timeperiod=wilders_period)
    data['dar'] = ta.EMA(data['ma_atr_rsi'], timeperiod=wilders_period) * qqe

    data['longband'] = np.nan
    data['shortband'] = np.nan
    data['trend'] = 0

    for i in range(1, len(data)):
        if data.loc[i - 1, 'rsi_ma'] > data.loc[i - 1, 'longband'] and data.loc[i, 'rsi_ma'] > data.loc[
            i - 1, 'longband']:
            data.loc[i, 'longband'] = max(data.loc[i - 1, 'longband'], data.loc[i, 'rsi_ma'] - data.loc[i, 'dar'])
        else:
            data.loc[i, 'longband'] = data.loc[i, 'rsi_ma'] - data.loc[i, 'dar']

        if data.loc[i - 1, 'rsi_ma'] < data.loc[i - 1, 'shortband'] and data.loc[i, 'rsi_ma'] < data.loc[
            i - 1, 'shortband']:
            data.loc[i, 'shortband'] = min(data.loc[i - 1, 'shortband'], data.loc[i, 'rsi_ma'] + data.loc[i, 'dar'])
        else:
            data.loc[i, 'shortband'] = data.loc[i, 'rsi_ma'] + data.loc[i, 'dar']

        if data.loc[i, 'rsi_ma'] < data.loc[i, 'shortband'] and data.loc[i - 1, 'rsi_ma'] > data.loc[
            i - 1, 'shortband']:
            data.loc[i, 'trend'] = 1
        elif data.loc[i, 'rsi_ma'] > data.loc[i, 'longband'] and data.loc[i - 1, 'rsi_ma'] < data.loc[
            i - 1, 'longband']:
            data.loc[i, 'trend'] = -1
        else:
            data.loc[i, 'trend'] = data.loc[i - 1, 'trend']

    data['fast_atr_rsi_tl'] = np.where(data['trend'] == 1, data['longband'], data['shortband'])
    data['qqe_long'] = np.where(
        (data['fast_atr_rsi_tl'].shift(1) < data['rsi_ma'].shift(1)),
        data['fast_atr_rsi_tl'].shift(1) - 50, np.nan)
    data['qqe_short'] = np.where(
        (data['fast_atr_rsi_tl'].shift(1) > data['rsi_ma'].shift(1)),
        data['fast_atr_rsi_tl'].shift(1) - 50, np.nan)

    return data

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
singal = qqe(stock_data, 5, 3, 4.238)

print(singal['qqe_long'])
for i in singal['qqe_long']:
    print(i)
print(config.time2date(history[-1][0]))
exit()

###信号有连续性，在获取到新信号后判断

# for i in range(len(buy_signals)):
#     if not np.isnan(buy_signals[i]) and buy_signals[i] > 10:
#         print(f"在第 {i } 个时刻有一个做多信号。")
#         print(buy_signals[i])
#         history[i][1] = config.time2date(history[i][0])
#         print(history[i])
# exit()

print(singal['qqe_short'])
for i in range(len(singal['qqe_long'])):
    # print(singal['qqe_long'][i])
    if not np.isnan(singal['qqe_long'][i]):
        print(f"在第 {i} 个时刻有一个做多信号。")
        print(singal['qqe_long'][i])
        history[i][1] = config.time2date(history[i][0])
        print(history[i])
