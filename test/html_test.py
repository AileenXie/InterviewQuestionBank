#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/28 12:01 PM
# @Author : aileen
# @File : html_test.py
# @Software: PyCharm
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("打开网页例子")
        #相当于初始化这个加载web的控件
        self.browser = QWebEngineView()
        #加载外部页面，调用
        # self.browser.load(QUrl("http://www.baidu.com"))
        file = open("file.html", "r", encoding='utf-8')
        html = file.read()
        self.browser.setHtml(html)
        self.setCentralWidget(self.browser)

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())