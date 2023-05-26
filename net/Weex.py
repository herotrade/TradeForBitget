## 基于weex 的api 通信
##
##
import math
import os.path
import time

import requests
from net import config


class Weex:
    baseApi = "https://www.bitget.com"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "apptheme": "dark",
        # "cookie": "locale=zh-CN; _ga=GA1.2.1235430122.1681972705; _gid=GA1.2.962719412.1682215450; BITGET_LOCAL_COOKIE={%22bitget_lang%22:%22zh-CN%22%2C%22bitget_unit%22:%22CNY%22%2C%22bitget_showasset%22:true%2C%22bitget_theme%22:%22dark%22%2C%22bitget_layout%22:%22right%22%2C%22bitget_valuationunit%22:1%2C%22bitgt_login%22:false}; bt_newsessionid=; bt_sessonid=; bt_rtoken=; _ga_VJ1TZQ4HKS=GS1.1.1682218523.7.1.1682219022.0.0.0",
        "language": "zh_CN",
        "locale": "zh_CN",
        "origin": "https://www.bitget.com",
        "devicelanguage": "zh_CN",
        "fbid": "fb.1.1682417364125.1045559128",
        "gaclientid": "1131295122.1682417357",
        "gaid": "GA1.2.1131295122.1682417357",
        "gasessionid": "1684287807",
        "terminalcode": "a83f40fd182bf80e8def0cc692a2947f",
        "terminaltype": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    cookie = None

    session = None
    logger = None

    PROFIT_MULT = 1

    info = {}

    RATE = 0.1  ##开仓比例

    balance = 0  ##账户余额

    LOSS_RATE = 1  ##止损倍数

    POINT = 30  ##默认盈亏点位

    SYMBOL = "BTC"

    BTC_USDT = 0
    ETH_USDT = 0

    cookie = None

    def __init__(self):
        self.session = requests.session()
        self.initlog()
        with open('./cookie.info', 'r') as file:
            self.cookie = file.read()
            self.headers['cookie'] = self.cookie
            self.headers['Cookie'] = self.cookie
            file.close()
            self.logger.info("cookie 信息已设置")
            self.getAssets()

    def initlog(self):
        lp = config.time2date(time.time() * 1000)
        self.logger = config.logger_config(log_path="./log-%s.txt" % (str(lp)), logging_name='')
        self.logger.info("日志文件初始化成功")

    def setLossRate(self, value):
        self.LOSS_RATE = float(value)
        self.logger.info("止损倍数：%s" % str(self.LOSS_RATE))

    def setSymbol(self, _symbol):
        self.SYMBOL = _symbol

    def setRate(self, v):
        self.RATE = float(v)

    def getZhang(self):
        print(self.BTC_USDT)
        avaAmount = math.ceil(float(self.BTC_USDT) * self.RATE / 100)
        return int(avaAmount)

    def setPoint(self, v):
        self.POINT = v

    def setProfitMult(self, v):
        self.PROFIT_MULT = float(v)

    ##登陆weex 系统
    def login(self, username, password):
        self.info = {
            "username": username,
            "password": password
        }

        path = self.baseApi + "/v1/user/login"
        form = {
            "areaCode": "86",
            "languageType": "1",
            "loginName": username,
            "pwd": password
        }
        response = self.session.post(path, headers=self.headers, json=form)
        if int(response.json()['code']) == 0:
            self.cookie = self.cookie
            self.logger.info("账号:%s 登陆成功：%s" % (str(username), str(response.json())))
            self.getAssets()
            return response.json()
        else:
            return False

    ##获取账户资产
    def getAssets(self):
        api = self.baseApi + "/v1/mix/assets"
        response = self.session.post(api, headers=self.headers, json={"languageType": 1})
        self.balance = float(response.json()['data']['contractTotalUsdt'])
        self.logger.info(str(response.json()['data']['professionalContract']))
        self.BTC_USDT = float(response.json()['data']['professionalContract']['totalUsdt'])
        self.logger.info("合约账户可用余额：%s" % str(self.BTC_USDT))

        return response.json()

    ##设置合约杠杆倍数
    def setLeverLevel(self, num, symbol='btc', position=0):
        api = self.baseApi + "/v1/if/contract/levelRate"
        data = {
            "languageType": 1,
            "levelRate": int(num),
            "positionType": position,  ##0多头  1空头
            "productCode": "cmt_%susdt" % symbol
        }
        response = self.session.post(api, headers=self.headers, json=data)
        return response.json()

    ###计算止盈策略
    def calucProfit(self, amount, price, type):
        try:
            amount = self.getZhang()
            bzj = amount * 0.001 * price / 100
            camount = bzj / price

            win = bzj / 100 / camount  ##保证金1：1的平仓价格
            if type == 1:
                ###做多
                side = 1
                winStep1 = price + win * 2  ###第一步平掉百分之50，剩下的盈利交由信号处理
            else:
                ##做空
                winStep1 = price - win * 2
                side = 2
            api = self.baseApi + '/v1/if/contract/v2/place'
            data = {
                "amount": str(int(amount) / 2),
                "languageType": 1,
                "matchType": 0,
                "productCode": "cmt_btcusdt",
                "side": side,
                "tradePrice": str(winStep1),
                "type": 2
            }
            self.session.post(api, headers=self.headers, json=data)
        except:
            pass

    ##多单的止盈止损
    def LongStopPlan(self, amount, price, per=0):
        ##per = 0 止损
        ##per = 1 止盈
        amount = self.getZhang()
        if per == 0:
            ptype = 2
        else:
            ptype = 1
        api = self.baseApi + '/v1/if/contract/newStopPlan'
        data = {
            "delegateCount": str(amount),
            "languageType": 1,
            "matchType": 1,
            "planType": ptype,
            "productCode": "cmt_btcusdt",
            "side": 1,
            "stopPrice": str(price)
        }
        response = self.session.post(api, headers=self.headers, json=data)
        self.logger.info("多单止盈止损：%s" % str(data))
        self.logger.info("多单方法 longstopplan 执行返回结果：%s " % str(response.json()))
        return response.json()

    ##开多
    def buyLong(self, price, ptype):
        try:
            api = self.baseApi + "/v1/mcp/order/openContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "delegateCount": str(self.RATE),
                "delegateType": 1,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                # "presetStopLossPrice":"",
                # "presetTakeProfitPrice":"",
                "pricedSymbol": "USDT",
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            if ptype != 0:
                lw = self.POINT
                loss = price - (lw * self.LOSS_RATE)
                win = price + (lw * self.PROFIT_MULT)
                data['presetStopLossPrice'] = str(int(loss))
                data['presetTakeProfitPrice'] = str(int(win))
            else:
                lw = price / self.RATE / 125
                data['presetStopLossPrice'] = str(int(price - lw))
                data['presetTakeProfitPrice'] = str(int(price + (lw * 2)))
            self.logger.info("做多参数 buyLong：%s" % str(data))
            response = self.session.post(api, headers=self.headers, json=data)
            if ptype != 0:
                res = self.pshort()
                self.logger.info("平空接口返回 pshort 执行返回结果：%s " % str(res))
            self.logger.info("做多方法 buyLong 执行返回结果：%s " % str(response.json()))
            return response.json()
        except Exception as e:
            return e

    ###空单止盈止损设置
    def ShortStopPlan(self, amount, price, per=0):
        ##per = 0 空单止损  ptype = 2
        ##per = 1 空单止盈  ptype = 1
        amount = self.getZhang()
        if per == 0:
            ptype = 2
        else:
            ptype = 1
        api = self.baseApi + '/v1/if/contract/newStopPlan'
        data = {
            "delegateCount": str(amount),
            "languageType": 1,
            "matchType": 1,
            "planType": ptype,
            "productCode": "cmt_btcusdt",
            "side": 2,
            "stopPrice": str(price)
        }
        response = self.session.post(api, headers=self.headers, json=data)
        self.logger.info("空单止盈止损参数：%s" % str(data))
        self.logger.info("空单止盈止损 ShortStopPlan 执行返回结果：%s " % str(response.json()))
        return response.json()

    ##开空
    def buyShort(self, price, ptype):
        try:
            api = self.baseApi + "/v1/mcp/order/openContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "delegateCount": str(self.RATE),
                # "presetStopLossPrice": str(int(loss)),
                # "presetTakeProfitPrice": str(int(win)),
                "delegateType": 2,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                "pricedSymbol": "USDT",
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            if ptype != 0:
                lw = self.POINT
                loss = price + (lw * self.LOSS_RATE)
                win = price - (lw * self.PROFIT_MULT)
                data['presetStopLossPrice'] = str(int(loss))
                data['presetTakeProfitPrice'] = str(int(win))
            else:
                lw = price / self.RATE / 125
                data['presetStopLossPrice'] = str(int(price + lw))
                data['presetTakeProfitPrice'] = str(int(price - (lw * 2)))
            self.logger.info("做空参数：%s" % str(data))
            response = self.session.post(api, headers=self.headers, json=data)
            if ptype != 0:
                res = self.plong()
                self.logger.info("平多接口 plong 执行返回结果：%s " % str(res))
            self.logger.info("做空 buyShort 执行返回结果：%s " % str(response.json()))
            return response.json()
        except Exception as e:
            print(e)
            return e

    ##空单的平仓
    def pshort(self):
        try:
            api = self.baseApi + "/v1/mcp/order/closeContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "cancelOrder": True,
                "delegateCount": str(self.RATE),
                "delegateType": 4,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            response = self.session.post(api, headers=self.headers, json=data)
            self.logger.info("平空：%s" % (str(response.json())))
            return response.json()
        except Exception as e:
            print(e)
            return False

    ##多单的平仓
    def plong(self):
        try:
            api = self.baseApi + "/v1/mcp/order/closeContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "cancelOrder": True,
                "delegateCount": str(self.RATE),
                "delegateType": 3,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            response = self.session.post(api, headers=self.headers, json=data)
            self.logger.info("平多：%s" % (str(response.json())))
            return response.json()
        except:
            return False

        ##空单的平仓
    def pshortByamount(self,amount):
        try:
            api = self.baseApi + "/v1/mcp/order/closeContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "cancelOrder": True,
                "delegateCount": str(amount),
                "delegateType": 4,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            response = self.session.post(api, headers=self.headers, json=data)
            self.logger.info("平空：%s" % (str(response.json())))
            return response.json()
        except Exception as e:
            print(e)
            return False

    ##多单的平仓
    def plongByamount(self,amount):
        try:
            api = self.baseApi + "/v1/mcp/order/closeContract"
            data = {
                "businessLine": 10,
                "businessSource": 10,
                "cancelOrder": True,
                "delegateCount": str(amount),
                "delegateType": 3,
                "enterPointSource": 1,
                "languageType": 1,
                "orderType": 1,
                "secondBusinessLine": "N/A",
                "symbolId": "BTCUSDT_UMCBL",
                "timeInForceValue": 0,
                "tokenId": "USDT"
            }
            response = self.session.post(api, headers=self.headers, json=data)
            self.logger.info("平多：%s" % (str(response.json())))
            return response.json()
        except:
            return False
