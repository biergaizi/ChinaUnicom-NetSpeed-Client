#!/usr/bin/python3
import sys
import os
sys.path.append(os.getcwd() + "/ui")
from PyQt4 import QtCore, QtGui
from main_ui import Ui_MainWindow
from netspeed import NetSpeed


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
            self.label.setText('<html><head/><body><p align="center">你未处于提速状态</p><p align="center">提速前：%s %s；提速后：%s Mbps</p><p align="center">剩余提速时长：%s 小时</p></body></html>'
                    % (self.myNetSpeed.old_speed, self.myNetSpeed.old_speed_unit_name,
                       self.myNetSpeed.new_speed, self.myNetSpeed.hours))
            self.btnSpeedChange.setText("提速")
            self.btnSpeedChange.setEnabled(self.myNetSpeed.hours)
        else:
            self.label.setText('<html><head/><body><p align="center">你已处于提速状态</p><p align="center">提速前：%s %s；提速后：%s Mbps</p><p align="center">剩余提速时长：%s 小时</p></body></html>'
                    % (self.myNetSpeed.old_speed, self.myNetSpeed.old_speed_unit_name,
                       self.myNetSpeed.new_speed, self.myNetSpeed.hours))
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


App = QtGui.QApplication(sys.argv)
App.setApplicationName("联通提速客户端")

Translate = QtCore.QTranslator()
Translate.load("translates/qt_zh_CN.qm")

Main = MainWindow()
Main.show()
App.exec()
