# from BASE_ABOUT.needClass import TempleteWindow
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QComboBox,QVBoxLayout,QHBoxLayout
from configparser import RawConfigParser
from needBase import *
import sys
LIST_COMB = ["ObjId","createTime","UserID","AccountEmail","ConfigModule","Result","errcode","description","routermac"
            "router_vender","deviceMac","ip","AppVersion","OSVersion","MobileType","wifiSSID","AUTH","isManualInput",
            "transfromText","free_heap","routerRssi","FirmVersion","step5_qeury_result","step5_network_status",
             "step7_port_result","step4_wifi_code","step4_wifi_desc","wifi_ble_code1","wifi_ble_desc1","wifi_ble_code2",
             "wifi_ble_desc2","date","Insert_info_time","update_info_time"]
CONFIG = RawConfigParser()
CONFIG.read("config.ini")
STYLE = '''
        QPushButton:hover{background-color:#E7EAED;}
'''
class Window(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        if parent:
            self.setParent(parent)
        else:
            self.setWindowTitle("配网日志")
        self.alldata = []
        self.setGeometry(100,100,900,800)
        self.comb0 = QComboBox(self)
        self.comb0.addItems(LIST_COMB)
        self.comb0.setCurrentIndex(2)
        self.comb0.setEditable(True)
        self.box0  = QLineEdit(self)
        self.btn0  = QPushButton("查询sql",self)
        # self.btn0.setStyleSheet(STYLE)
        self.btn0.clicked.connect(self.btnclick)
        self.mainlaoyout = QVBoxLayout()
        self.setLayout(self.mainlaoyout)
        self.topwidget = QWidget(self)
        self.toplauout = QHBoxLayout()
        self.topwidget.setLayout(self.toplauout)
        self.toplauout.addWidget(self.comb0,5)
        self.toplauout.addWidget(self.box0,30)
        self.toplauout.addWidget(self.btn0,5)
        self.table = Tablewidget(self)
        self.mainlaoyout.addWidget(self.topwidget,1)
        self.mainlaoyout.addWidget(self.table,40)

        self.show()

    def btnclick(self):
        text1 = self.comb0.currentText()
        text2 = self.box0.text()
        self.clear()
        if text2 == "":
            pass
        else:
            sql = f'''select * from mongo_config_detail_info where {text1} = "{text2}" order by createTime desc limit 500'''
            MongoConfigDetailInfo.set_cofnig(CONFIG)
            data = MongoConfigDetailInfo.get_data_by_sql(sql)
            if data:
                self.get_table_data(data)

    def clear(self):
        self.alldata.clear()

    def get_table_data(self,data):
        header = eval(CONFIG.get("table","showline"))
        for s in header:
            self.alldata.append([s])
            for d in data:
                self.alldata[-1].append(Dict(d)[s])
        self.table.showdata(self.alldata)


if __name__ == "__main__":
    s = QApplication(sys.argv)
    d = Window()
    s.exec_()