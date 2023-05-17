import numpy as np
import pandas as pd

import config


def ema(series, period):
    return series.ewm(span=period).mean()


def smoothrng(x, t, m):
    wper = t * 2 - 1
    avrng = x.diff().abs().ewm(span=t).mean()
    smoothrng = avrng.ewm(span=wper).mean() * m
    return smoothrng


def rngfilt(x, r):
    rngfilt = x.copy()
    for i in range(1, len(x)):
        rngfilt.iloc[i] = x.iloc[i] - r.iloc[i] if x.iloc[i] > rngfilt.iloc[i - 1] and x.iloc[i] - r.iloc[i] > \
                                                   rngfilt.iloc[i - 1] else rngfilt.iloc[i - 1]
        rngfilt.iloc[i] = x.iloc[i] + r.iloc[i] if x.iloc[i] + r.iloc[i] < rngfilt.iloc[i - 1] else rngfilt.iloc[i]
    return rngfilt


def get_signals(src, per, mult):
    sm_rng = smoothrng(src, per, mult)
    filt = rngfilt(src, sm_rng)

    upward = (filt > filt.shift(1)).cumsum()
    downward = (filt < filt.shift(1)).cumsum()

    longCond = ((src > filt) & (src > src.shift(1)) & (upward > 0)) | (
            (src > filt) & (src < src.shift(1)) & (upward > 0))
    shortCond = ((src < filt) & (src < src.shift(1)) & (downward > 0)) | (
            (src < filt) & (src > src.shift(1)) & (downward > 0))

    CondIni = longCond.astype(int) - shortCond.astype(int)
    CondIni = CondIni.shift(1).fillna(0)

    longCondition = longCond & (CondIni == -1)
    shortCondition = shortCond & (CondIni == 1)

    return longCondition, shortCondition


@config.debounce(1)
def getSign(data, _per=1500, _mult=3):
    # src = pd.Series([float(entry[4]) for entry in data])
    close = []
    timestamp = []
    for entry in data:
        close.append(float(entry[4]))
        timestamp.append(int(entry[0]))
    # src = pd.DataFrame({'close': [float(entry[4]) for entry in data], 'timestamp': [float(entry[0]) for entry in data]})
    src = pd.DataFrame({'close': close, 'timestamp': timestamp})
    long_condition, short_condition = get_signals(src['close'], _per, _mult)
    short = []
    longSign = {}
    shortSign = {}
    for i in range(0, len(short_condition)):
        if short_condition.iloc[i] == True:
            shortSign = {
                "time": config.time2date(data[i][0]),
                "timestamp": int(data[i][0]),
                "map": data[i][4],
                "sign": True,
                "per": "short"
            }
    long = []
    for i in range(0, len(long_condition)):
        if long_condition.iloc[i] == True:
            longSign = {
                "time": config.time2date(data[i][0]),
                "timestamp": int(data[i][0]),
                "map": data[i][4],
                "sign": True,
                "per": "long",
            }
    longSign['newprice'] = data[-1][4]
    shortSign['newprice'] = data[-1][4]
    del close,timestamp,data
    return shortSign,longSign
