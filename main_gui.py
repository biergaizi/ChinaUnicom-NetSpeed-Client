#!/usr/bin/python3
import sys
import os
sys.path.append(os.getcwd() + "/ui")
import random
import httplib2
from bs4 import BeautifulSoup
from PyQt4 import QtCore, QtGui
from main_ui import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnSpeedChange.clicked.connect(self.speedChanged)
        self.btnRefresh.clicked.connect(self.refresh)
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.load)
        self.timer.start(10)

    def load(self):
        self.timer.stop()
        self.myNetSpeed = NetSpeed()
        self.status_display()
        self.timer.start(32 * 60 * 1000) 
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.refresh)

    def status_display(self):
        if not self.myNetSpeed.status:
            self.label.setText('<html><head/><body><p align="center">你未处于提速状态</p><p align="center">提速前：%s M；提速后：%s M</p><p align="center">剩余提速时长：%s 小时</p></body></html>' 
                    % (self.myNetSpeed.old_speed, self.myNetSpeed.new_speed, self.myNetSpeed.hours))
            self.btnSpeedChange.setText("提速")
            self.btnSpeedChange.setEnabled(self.myNetSpeed.hours)
        else:
            self.label.setText('<html><head/><body><p align="center">你已处于提速状态</p><p align="center">提速前：%s M；提速后：%s M</p><p align="center">剩余提速时长：%s 小时</p></body></html>' 
                    % (self.myNetSpeed.old_speed, self.myNetSpeed.new_speed, self.myNetSpeed.hours))
            self.btnSpeedChange.setText("降速")

    def speedChanged(self):
        if not self.myNetSpeed.status:
            status = self.myNetSpeed.speed_up()
            self.btnSpeedChange.setText("提速中……")
        else:
            status = self.myNetSpeed.speed_down()
            self.btnSpeedChange.setText("降速中……")

        if status:
            QtGui.QMessageBox.information(None, "成功", "操作成功！")
        else:
            QtGui.QMessageBox.warning(None, "错误", "操作失败！")

        self.status_display()

    def refresh(self):
        self.myNetSpeed.get_info()
        self.status_display()


class NetSpeed(object):
    def __init__(self):
        self.get_info()

    def parse_info(self, html):
        def clean_html(html):
            soup = BeautifulSoup(html)
            result = soup.find(id="webcode").string

            # Remove unexcepted ";" under OS X.
            return result.replace(";", "")

        html = clean_html(html)
        html = html.split('&')
        info = {}
        for i in html:
            tag, value = i.split('=')
            info[tag] = value

        return info

    def speed_up(self):
        h = httplib2.Http()
        resp, content = \
                h.request("http://bj.wokuan.cn/web/improvespeed.php?ContractNo=%s&up=%s&old=%s&round=%s"
                        % (self.id, self.new_speed_id, self.old_speed_id, random.randint(0, 100)))

        self.get_info()
        content = content.decode("utf-8")
        return "success&00000000" in content

    def speed_down(self):
        h = httplib2.Http()
        resp, content = \
                h.request("http://bj.wokuan.cn/web/lowerspeed.php?ContractNo=%s&round=%s"
                        % (self.id, random.randint(0, 100)))

        self.get_info()
        content = content.decode("utf-8")
        return "success&00000000" in content

    def get_info(self):
        h = httplib2.Http()
        resp, content = h.request("http://bj.wokuan.cn/web/startenrequest.php")

        content = content.decode("utf-8")
        info = self.parse_info(content)

        self.id = info['cn']
        self.status = int(info['stu'])
        self.old_speed = info['os']
        self.old_speed_id = info['old']
        self.new_speed = info['up']
        self.new_speed_id = info['gus']
        self.hours = float(info['glst'])


App = QtGui.QApplication(sys.argv)
App.setApplicationName("联通提速客户端")

Translate = QtCore.QTranslator()
Translate.load("translates/qt_zh_CN.qm")

Main = MainWindow()
Main.show()
App.exec()
