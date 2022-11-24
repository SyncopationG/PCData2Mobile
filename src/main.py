import bluetooth
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from . import Name, RandomData, ThreadSearchBluetooth
from .ui import Ui_MainWindow


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, ):
        QMainWindow.__init__(self)
        self.sock = bluetooth.BluetoothSocket()
        self.para = {}
        self.thread_search_bluetooth = ThreadSearchBluetooth()
        self.setupUi(self)
        self.func_data_type = int
        self.func_data = RandomData.int_type
        self.childQMessageBox = QMessageBox()
        self.comboBoxSelectBluetooth.currentIndexChanged.connect(self.on_change_select_bluetooth)
        self.comboBoxDataType.currentIndexChanged.connect(self.on_change_data_type)
        self.spinBoxNumbers.valueChanged.connect(self.on_change_numbers)
        self.lineEditMinValue.textChanged.connect(self.on_change_value_min)
        self.lineEditMaxValue.textChanged.connect(self.on_change_value_max)
        self.do_init()
        self.pushButtonSearchBluetooth.clicked.connect(self.on_clicked_search_bluetooth)
        self.pushButtonConnectBluetooth.clicked.connect(self.on_clicked_connect_bluetooth)
        self.pushButtonSendData.clicked.connect(self.on_clicked_send_data)

    def closeEvent(self, event):
        reply = self.childQMessageBox.question(self, '消息', '退出？')
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_change_select_bluetooth(self):
        a = self.comboBoxSelectBluetooth.currentText()
        self.para[Name.bluetooth] = {
            Name.name: a[:-18],
            Name.addr: a[-17:],
        }
        print(self.para)

    def on_change_data_type(self):
        self.para[Name.data_type] = self.comboBoxDataType.currentText()
        if self.para[Name.data_type] == Name.data_int:
            self.func_data_type = int
            self.func_data = RandomData.int_type
        else:
            self.func_data_type = float
            self.func_data = RandomData.float_type
        print(self.para)

    def on_change_numbers(self, val):
        self.para[Name.data_numbers] = val
        print(self.para)

    def data_yes_no(self, val):
        if self.para[Name.data_type] == Name.data_int:
            try:
                int(val)
            except ValueError:
                return False
        return True

    def message_waning(self, title="提醒", message="检查输入数据！"):
        self.childQMessageBox.information(self, title, message)

    def message_status_bar(self, msg):
        self.statusbar.showMessage(msg)

    def message_waning_data(self):
        if self.para[Name.data_value_min] > self.para[Name.data_value_max]:
            self.message_waning()
            return False
        return True

    def on_change_value_min(self, val):
        if self.data_yes_no(val):
            self.para[Name.data_value_min] = self.func_data_type(val)
            print(self.para)
        else:
            self.message_waning()

    def on_change_value_max(self, val):
        if self.data_yes_no(val):
            self.para[Name.data_value_max] = self.func_data_type(val)
            print(self.para)
        else:
            self.message_waning()

    def do_init(self):
        self.para[Name.data_type] = self.comboBoxDataType.currentText()
        self.para[Name.data_numbers] = self.spinBoxNumbers.value()
        self.para[Name.data_value_min] = self.func_data_type(self.lineEditMinValue.text())
        self.para[Name.data_value_max] = self.func_data_type(self.lineEditMaxValue.text())
        print(self.para)

    def update_select_bluetooth(self, val):
        self.comboBoxSelectBluetooth.clear()
        for addr, name in val:
            self.comboBoxSelectBluetooth.addItem(f"{name}-{addr}")
        self.message_status_bar("蓝牙搜索完成！")
        self.thread_search_bluetooth.stopping()

    def on_clicked_search_bluetooth(self):
        self.thread_search_bluetooth.start()
        self.thread_search_bluetooth.starting()
        self.thread_search_bluetooth.signalResult.connect(self.update_select_bluetooth)
        self.message_status_bar("蓝牙搜索中……")

    def on_clicked_connect_bluetooth(self):
        addr = self.para[Name.bluetooth][Name.addr]
        self.sock.connect((addr, 1))
        self.message_status_bar("连接完成！")

    def on_clicked_send_data(self):
        if self.message_waning_data():
            self.para[Name.data] = self.func_data(
                self.para[Name.data_numbers],
                self.para[Name.data_value_min],
                self.para[Name.data_value_max],
            )
            print(self.para)
        self.message_status_bar("数据已生成！")
        self.sock.send(self.para[Name.data])
        self.message_status_bar("数据发送成功！")
        self.sock.close()
