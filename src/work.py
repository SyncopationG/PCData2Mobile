#!/usr/bin/env python
# -*- coding:utf8 -*-

import bluetooth
from PyQt5.QtCore import pyqtSignal, QThread


class ThreadSearchBluetooth(QThread):
    signalResult = pyqtSignal(list)

    def __init__(self, parent=None, ):
        QThread.__init__(self, parent)
        self.flag = 1

    def __del__(self, ):
        self.flag = 0

    def working(self, ):
        a = bluetooth.discover_devices(lookup_names=True)
        self.signalResult.emit(a)
        self.sleep(1)

    def starting(self):
        self.flag = 1

    def stopping(self):
        self.flag = 0

    def run(self):
        while self.flag == 1:
            self.working()
