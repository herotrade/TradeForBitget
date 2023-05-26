# Periods = input(title="ATR Period", type=input.integer, defval=10)
# src = input(hl2, title="Source")
# Multiplier = input(title="ATR Multiplier", type=input.float, step=0.1, defval=3.0)
# changeATR= input(title="Change ATR Calculation Method ?", type=input.bool, defval=true)
# showsignals = input(title="Show Buy/Sell Signals ?", type=input.bool, defval=true)
# highlighting = input(title="Highlighter On/Off ?", type=input.bool, defval=true)
# atr2 = sma(tr, Periods)
# atr= changeATR ? atr(Periods) : atr2
# up=src-(Multiplier*atr)
# up1 = nz(up[1],up)
# up := close[1] > up1 ? max(up,up1) : up
# dn=src+(Multiplier*atr)
# dn1 = nz(dn[1], dn)
# dn := close[1] < dn1 ? min(dn, dn1) : dn
# trend = 1
# trend := nz(trend[1], trend)
# trend := trend == -1 and close > dn1 ? 1 : trend == 1 and close < up1 ? -1 : trend
# upPlot = plot(trend == 1 ? up : na, title="Up Trend", style=plot.style_linebr, linewidth=2, color=color.green)
# buySignal = trend == 1 and trend[1] == -1
# plotshape(buySignal ? up : na, title="UpTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.green, transp=0)
# plotshape(buySignal and showsignals ? up : na, title="Buy", text="Buy", location=location.absolute, style=shape.labelup, size=size.tiny, color=color.green, textcolor=color.white, transp=0)
# dnPlot = plot(trend == 1 ? na : dn, title="Down Trend", style=plot.style_linebr, linewidth=2, color=color.red)
# sellSignal = trend == -1 and trend[1] == 1
# plotshape(sellSignal ? dn : na, title="DownTrend Begins", location=location.absolute, style=shape.circle, size=size.tiny, color=color.red, transp=0)
# plotshape(sellSignal and showsignals ? dn : na, title="Sell", text="Sell", location=location.absolute, style=shape.labeldown, size=size.tiny, color=color.red, textcolor=color.white, transp=0)

import pandas as pd
import numpy as np

from net import config
import config
import test


def calculate_atr(data, periods, multiplier, change_atr=True):
    data['tr'] = np.maximum(
        np.maximum(
            data['high'] - data['low'],
            np.abs(data['high'] - data['close'].shift(1))
        ),
        np.abs(data['low'] - data['close'].shift(1))
    )

    if change_atr:
        data['atr'] = data['tr'].rolling(window=periods).mean()
    else:
        data['atr'] = data['tr'].ewm(span=periods, adjust=False).mean()

    data['up'] = data['close'] - multiplier * data['atr']
    data['up1'] = data['up'].shift(1)
    data['up'] = np.where(data['close'].shift(1) > data['up1'], np.maximum(data['up'], data['up1']), data['up'])

    data['dn'] = data['close'] + multiplier * data['atr']
    data['dn1'] = data['dn'].shift(1)
    data['dn'] = np.where(data['close'].shift(1) < data['dn1'], np.minimum(data['dn'], data['dn1']), data['dn'])

    data['trend'] = np.nan
    data.loc[0, 'trend'] = 1

    for i in range(1, len(data)):
        if data.loc[i - 1, 'trend'] == -1 and data.loc[i, 'close'] > data.loc[i, 'dn1']:
            data.loc[i, 'trend'] = 1
        elif data.loc[i - 1, 'trend'] == 1 and data.loc[i, 'close'] < data.loc[i, 'up1']:
            data.loc[i, 'trend'] = -1
        else:
            data.loc[i, 'trend'] = data.loc[i - 1, 'trend']

    data['buy_signal'] = (data['trend'] == 1) & (data['trend'].shift(1) == -1)
    data['sell_signal'] = (data['trend'] == -1) & (data['trend'].shift(1) == 1)
    return data


params = test.getHistory()
print(config.time2date(params[0][0]))
print(config.time2date(params[-1][0]))

high = []
low = []
close = []
for i in params:
    high.append(float(i[2]))
    low.append(float(i[3]))
    close.append(float(i[4]))
pdata = pd.DataFrame({"high": high, "low": low, "close": close})
result = calculate_atr(pdata, 5, 1, True)
long = {}
short = {}
for index, value in enumerate(result['trend']):
    if result['sell_signal'][index]:
        short = {
            "time": config.time2date(params[index][0]),
            "timestamp": params[index][0],
            "map": params[index][4],
            "sign": True,
            "per": "short"
        }
        print("有一个做空信号")
        print(short)

    if result['buy_signal'][index]:
        long = {
            "time": config.time2date(params[index][0]),
            "timestamp": params[index][0],
            "map": params[index][4],
            "sign": True,
            "per": "long"
        }
        print("有一个做多信号")
        print(long)
