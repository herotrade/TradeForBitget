# This Python file uses the following encoding: utf-8
import sys

import requests
from PySide6.QtWidgets import QApplication, QWidget

# Important:
# You need to run the following command to generate the PageLogin.py file
#     pyside6-uic form.ui -o PageLogin.py, or
#     pyside2-uic form.ui -o PageLogin.py
from ui_form import Ui_Widget
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget, QMainWindow, QVBoxLayout, QMessageBox)
import sys
from qt_material import apply_stylesheet
from main import Widget as MainWidget
from net.Weex import Weex
import os


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("基于python3 的高频计算多策略模型全自动量化交易工具 - 开发者Tg @chenmaq")

        self.ui.pushButton.clicked.connect(self.login)

        if os.path.exists("./cookie.info"):
            with open('./cookie.info', 'r') as file:
                cookie = file.read()
                file.close()
                self.ui.cookie.setText(cookie)

    def login(self):
        print("login")
        cookie = self.ui.cookie.text().strip()

        if cookie == '':
            QMessageBox.information(self, "登录提示", "请按照要求输入cookie信息")
        else:
            try:
                result = self.test(cookie)
                if result['code'] == '00000' and result['data']['contractTotalBtc']:
                    with open('./cookie.info', 'w+') as file:
                        file.write(cookie)
                        file.close()
                    QMessageBox.information(self, "登陆提示", "cookie 正确，已自动保存登陆信息。")
                    self.mainWindow = MainWidget()
                    self.mainWindow.show()
                    self.close()
            except Exception as e:
                print(e)
                QMessageBox.information(self, "登陆提示", "cookie 信息不正确")
                return False
            # self.mainWindow = MainWidget({"username": username, "password": password,"proxy":proxy})
            # # self.mainWindow.session = self.weex
            # self.mainWindow.show()
            # self.close()

    def test(self, cookie):
        try:
            url = "https://www.bitget.com/v1/mix/assets"
            header = {"accept": "application/json, text/plain, */*", "accept-language": "zh-CN,zh;q=0.9",
                      "apptheme": "dark", "cache-control": "no-cache", "content-type": "application/json;charset=UTF-8",
                      "devicelanguage": "zh_CN", "fbid": "fb.1.1682417364125.1045559128",
                      "gaclientid": "1131295122.1682417357", "gaid": "GA1.2.1131295122.1682417357",
                      "gasessionid": "1684287807", "language": "zh_CN", "locale": "zh_CN",
                      "origin": "https://www.bitget.com", "terminalcode": "a83f40fd182bf80e8def0cc692a2947f",
                      "terminaltype": "1",
                      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                      'cookie': cookie, 'Cookie': cookie}
            params = {
                "languageType": 1
            }
            response = requests.post(url, headers=header, json=params)
            return response.json()
        except:
            return False

    def ll(self):
        url = "https://www.bitget.com/v1/user/login"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    # apply_stylesheet(app, theme='dark_teal.xml')
    widget.show()
    sys.exit(app.exec())
