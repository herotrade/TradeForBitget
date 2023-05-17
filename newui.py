# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'f3.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1185, 725)
        self.horizontalLayout_3 = QHBoxLayout(Widget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Widget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(885, 0))
        self.widget_2.setStyleSheet(u"background-color: rgb(199, 255, 242);")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.canvas = QWidget(self.widget_2)
        self.canvas.setObjectName(u"canvas")
        self.canvas.setMinimumSize(QSize(0, 0))
        self.canvas.setStyleSheet(u"background-color: rgb(100, 100, 100);")
        self.verticalLayout_3 = QVBoxLayout(self.canvas)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.kline = QWidget(self.canvas)
        self.kline.setObjectName(u"kline")
        self.kline.setMinimumSize(QSize(0, 500))
        self.kline.setStyleSheet(u"background-color:rgb(255, 255, 255)")

        self.verticalLayout_3.addWidget(self.kline)

        self.widget_4 = QWidget(self.canvas)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.label = QLabel(self.widget_4)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label)

        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(150, 0))
        self.label_4.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label_4)

        self.label_5 = QLabel(self.widget_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(150, 0))
        self.label_5.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label_5)

        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label_6)

        self.label_7 = QLabel(self.widget_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color: #ddd;")

        self.horizontalLayout.addWidget(self.label_7)


        self.verticalLayout_3.addWidget(self.widget_4)


        self.verticalLayout_2.addWidget(self.canvas)

        self.orders = QWidget(self.widget_2)
        self.orders.setObjectName(u"orders")
        self.orders.setEnabled(False)
        self.verticalLayout = QVBoxLayout(self.orders)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.siginList = QTextEdit(self.orders)
        self.siginList.setObjectName(u"siginList")
        self.siginList.setLayoutDirection(Qt.LeftToRight)
        self.siginList.setStyleSheet(u"color: rgb(171, 171, 171);\n"
"text-align:center;\n"
"padding:20px;\n"
"font-size:16px")
        self.siginList.setLineWrapMode(QTextEdit.WidgetWidth)

        self.verticalLayout.addWidget(self.siginList)


        self.verticalLayout_2.addWidget(self.orders)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.tools = QWidget(self.widget)
        self.tools.setObjectName(u"tools")
        self.tools.setMinimumSize(QSize(300, 0))
        self.tools.setStyleSheet(u"background-color: rgb(100, 100, 100)")
        self.verticalLayout_4 = QVBoxLayout(self.tools)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.tools)
        self.widget_5.setObjectName(u"widget_5")
        self.widget_5.setMinimumSize(QSize(0, 87))
        self.widget_5.setMaximumSize(QSize(16777215, 100))
        self.label_8 = QLabel(self.widget_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(25, 20, 58, 16))
        self.label_8.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size:14px")
        self.label_9 = QLabel(self.widget_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(123, 20, 58, 16))
        self.label_9.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size:14px")
        self.comboBox = QComboBox(self.widget_5)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 50, 103, 32))
        self.comboBox.setStyleSheet(u"color:#ddd")
        self.comboBox_2 = QComboBox(self.widget_5)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(120, 50, 70, 32))
        self.comboBox_2.setStyleSheet(u"color:#ddd")
        self.comboBox_3 = QComboBox(self.widget_5)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(200, 50, 80, 32))
        self.comboBox_3.setStyleSheet(u"color:#ddd")
        self.label_10 = QLabel(self.widget_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(200, 20, 58, 16))
        self.label_10.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size:14px")

        self.verticalLayout_4.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.tools)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_5 = QVBoxLayout(self.widget_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox = QGroupBox(self.widget_6)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 80))
        self.groupBox.setStyleSheet(u"color:#ddd")
        self.autobutton_2 = QPushButton(self.groupBox)
        self.autobutton_2.setObjectName(u"autobutton_2")
        self.autobutton_2.setGeometry(QRect(30, 30, 100, 41))
        self.autobutton_2.setStyleSheet(u"color:#666;\n"
"background-color: rgb(255, 164, 156);")
        self.autobutton_3 = QPushButton(self.groupBox)
        self.autobutton_3.setObjectName(u"autobutton_3")
        self.autobutton_3.setGeometry(QRect(150, 90, 100, 41))
        self.autobutton_3.setStyleSheet(u"color:#666;\n"
"background-color: rgb(255, 164, 156);")
        self.autobutton_4 = QPushButton(self.groupBox)
        self.autobutton_4.setObjectName(u"autobutton_4")
        self.autobutton_4.setGeometry(QRect(30, 90, 100, 41))
        self.autobutton_4.setStyleSheet(u"color:#666;\n"
"background-color: rgb(255, 164, 156);")
        self.autobutton_5 = QPushButton(self.groupBox)
        self.autobutton_5.setObjectName(u"autobutton_5")
        self.autobutton_5.setGeometry(QRect(150, 30, 100, 41))
        self.autobutton_5.setStyleSheet(u"color:#666;\n"
"background-color: rgb(255, 164, 156);")

        self.verticalLayout_5.addWidget(self.groupBox)


        self.verticalLayout_4.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.tools)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_6 = QVBoxLayout(self.widget_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_2 = QGroupBox(self.widget_7)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 257))
        self.groupBox_2.setStyleSheet(u"color:#ddd")
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(20, 40, 58, 16))
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 70, 71, 16))
        self.autocost = QLineEdit(self.groupBox_2)
        self.autocost.setObjectName(u"autocost")
        self.autocost.setGeometry(QRect(80, 38, 41, 21))
        self.autocost.setStyleSheet(u"border:none;\n"
"border-bottom:solid 1px #ddd")
        self.rate = QLineEdit(self.groupBox_2)
        self.rate.setObjectName(u"rate")
        self.rate.setGeometry(QRect(91, 67, 41, 21))
        self.rate.setStyleSheet(u"border:none;\n"
"border-bottom:solid 1px #ddd")
        self.autobutton = QPushButton(self.groupBox_2)
        self.autobutton.setObjectName(u"autobutton")
        self.autobutton.setGeometry(QRect(80, 181, 100, 41))
        self.autobutton.setStyleSheet(u"color:#666;\n"
"background-color: rgb(255, 164, 156);")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 220, 251, 31))
        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(20, 95, 81, 20))
        self.radioButton.setChecked(True)
        self.radioButton_2 = QRadioButton(self.groupBox_2)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(110, 95, 91, 20))
        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(100, 150, 113, 21))
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(30, 150, 58, 16))
        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(30, 120, 58, 16))
        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(100, 120, 113, 21))
        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(110, 40, 58, 16))
        self.autocost_2 = QLineEdit(self.groupBox_2)
        self.autocost_2.setObjectName(u"autocost_2")
        self.autocost_2.setGeometry(QRect(180, 38, 51, 21))
        self.autocost_2.setStyleSheet(u"border:none;\n"
"border-bottom:solid 1px #ddd")
        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(120, 70, 58, 16))
        self.autocost_3 = QLineEdit(self.groupBox_2)
        self.autocost_3.setObjectName(u"autocost_3")
        self.autocost_3.setGeometry(QRect(176, 67, 51, 21))
        self.autocost_3.setStyleSheet(u"border:none;\n"
"border-bottom:solid 1px #ddd")

        self.verticalLayout_6.addWidget(self.groupBox_2)


        self.verticalLayout_4.addWidget(self.widget_7)

        self.widget_8 = QWidget(self.tools)
        self.widget_8.setObjectName(u"widget_8")
        self.widget_8.setMinimumSize(QSize(0, 0))
        self.verticalLayout_7 = QVBoxLayout(self.widget_8)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_3 = QGroupBox(self.widget_8)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"color:#ddd")
        self.loglist = QTextEdit(self.groupBox_3)
        self.loglist.setObjectName(u"loglist")
        self.loglist.setGeometry(QRect(0, 20, 271, 341))
        self.loglist.setMinimumSize(QSize(0, 341))
        self.loglist.setStyleSheet(u"border:none")

        self.verticalLayout_7.addWidget(self.groupBox_3)


        self.verticalLayout_4.addWidget(self.widget_8)


        self.horizontalLayout_2.addWidget(self.tools)


        self.horizontalLayout_3.addWidget(self.widget)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"2023-03-25 13:25:11", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"24H\u6700\u9ad8\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"24H\u6700\u4f4e\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"\u6700\u65b0\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"RSI\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"BTC / USDT", None))
        self.siginList.setDocumentTitle(QCoreApplication.translate("Widget", u"\u4fe1\u53f7\u680f", None))
        self.siginList.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><title>\u4fe1\u53f7\u680f</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:16px; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'.AppleSystemUIFont'; font-size:18pt;\">\u65e5\u5fd7\u4fe1\u606f\uff1a</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Widget", u"\u4ea4\u6613\u5bf9", None))
        self.label_9.setText(QCoreApplication.translate("Widget", u"\u65f6\u6bb5", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Widget", u"BTCUSDT", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Widget", u"ETHUSDT", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("Widget", u"5\u5206\u949f", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Widget", u"15\u5206\u949f", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Widget", u"30\u5206\u949f", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Widget", u"MOVE-AVERAGE", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Widget", u"ATR-TRADE", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Widget", u"QQE-TRADE", None))

        self.label_10.setText(QCoreApplication.translate("Widget", u"\u7b56\u7565\u6a21\u5f0f", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"\u4ea4\u6613\u4fe1\u606f", None))
        self.autobutton_2.setText(QCoreApplication.translate("Widget", u"\u73b0\u4ef7\u505a\u591a", None))
        self.autobutton_3.setText(QCoreApplication.translate("Widget", u"\u73b0\u4ef7\u5e73\u7a7a", None))
        self.autobutton_4.setText(QCoreApplication.translate("Widget", u"\u73b0\u4ef7\u5e73\u591a", None))
        self.autobutton_5.setText(QCoreApplication.translate("Widget", u"\u73b0\u4ef7\u505a\u7a7a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"\u7b56\u7565\u53c2\u6570", None))
        self.label_16.setText(QCoreApplication.translate("Widget", u"\u6b62\u635f\u6bd4\u4f8b", None))
        self.label_17.setText(QCoreApplication.translate("Widget", u"\u6570\u91cfBTC", None))
        self.autocost.setText(QCoreApplication.translate("Widget", u"1", None))
        self.autocost.setPlaceholderText(QCoreApplication.translate("Widget", u"\u81ea\u52a8\u4e0b\u5355\u7684\u6700\u5927\u5f20\u6570", None))
        self.rate.setText(QCoreApplication.translate("Widget", u"1.0", None))
        self.rate.setPlaceholderText(QCoreApplication.translate("Widget", u"\u98ce\u9669\u63a7\u5236\u767e\u5206\u6bd4", None))
        self.autobutton.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb\u4ea4\u6613", None))
        self.label_2.setText("")
        self.radioButton.setText(QCoreApplication.translate("Widget", u"\u5206\u6279\u6b62\u76c8", None))
        self.radioButton_2.setText(QCoreApplication.translate("Widget", u"\u624b\u7eed\u8d39\u6b62\u76c8", None))
        self.lineEdit.setText(QCoreApplication.translate("Widget", u"3", None))
        self.label_11.setText(QCoreApplication.translate("Widget", u"\u79fb\u52a8\u53c2\u6570", None))
        self.label_12.setText(QCoreApplication.translate("Widget", u"ATR\u53c2\u6570", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Widget", u"1", None))
        self.label_18.setText(QCoreApplication.translate("Widget", u"\u6b62\u76c8\u6bd4\u4f8b", None))
        self.autocost_2.setText(QCoreApplication.translate("Widget", u"2", None))
        self.autocost_2.setPlaceholderText(QCoreApplication.translate("Widget", u"\u81ea\u52a8\u4e0b\u5355\u7684\u6700\u5927\u5f20\u6570", None))
        self.label_19.setText(QCoreApplication.translate("Widget", u"\u6b62\u76c8\u70b9\u4f4d", None))
        self.autocost_3.setText(QCoreApplication.translate("Widget", u"35", None))
        self.autocost_3.setPlaceholderText(QCoreApplication.translate("Widget", u"\u81ea\u52a8\u4e0b\u5355\u7684\u6700\u5927\u5f20\u6570", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"\u7cfb\u7edf\u65e5\u5fd7", None))
        self.loglist.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'.AppleSystemUIFont'; font-size:13pt;\"><br /></p></body></html>", None))
        self.loglist.setProperty("markdown", "")
    # retranslateUi

