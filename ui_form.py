# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newlogin.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.setEnabled(True)
        Widget.resize(829, 542)
        self.textBrowser = QTextBrowser(Widget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(200, 250, 411, 192))
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(310, 185, 221, 51))
        self.pushButton.setStyleSheet(u"width:200px")
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)
        self.cookie = QLineEdit(Widget)
        self.cookie.setObjectName(u"cookie")
        self.cookie.setGeometry(QRect(240, 40, 321, 141))

        self.retranslateUi(Widget)

        self.pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"\u5e01\u5b89\u5408\u7ea6\u7b56\u7565\u91cf\u5316\u4ea4\u6613\u673a\u5668\u4eba", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u4e00\u6b65 \u6253\u5f00bitget \u5b98\u65b9\u7f51\u7ad9</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u4e8c\u6b65 \u6253\u5f00\u767b\u5f55\u754c\u9762\uff0c\u8f93\u5165\u8d26\u53f7\u5bc6\u7801\uff0c\u6216\u8005\u626b\u7801\u767b\u5f55</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px"
                        "; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u4e09\u6b65 \u6253\u5f00\u8d44\u4ea7\u4e2d\u5fc3\uff0c\u6309F12 \u6216\u8005\u53f3\u5efa\u70b9\u51fb\u68c0\u67e5</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u56db\u6b65 \u5728\u663e\u793a\u7684\u5e95\u90e8\u6846\u4e2d\u7b2c\u4e00\u884c\u9009\u62e9network</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u4e94"
                        "\u6b65 \u5728\u754c\u9762\u53f3\u5efa\u70b9\u51fb\u91cd\u65b0\u52a0\u8f7d\u9875\u9762</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7b2c\u516d\u6b65 \u5728\u52a0\u8f7d\u7684url\u91cc\u9762\u627e\u4e00\u4e2a \u6253\u5f00header \u5934\u590d\u5236 request header \u7684cookie \u503c\u5230\u4e0a\u9762\u8f93\u5165\u6846\uff0c\u70b9\u51fb\u767b\u5f55\u3002</p></body></html>", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb\u4f7f\u7528\u81ea\u52a8\u4ea4\u6613", None))
    # retranslateUi

