from needClass import  GetElasticsearchData,Tablewidget,QApplication,QAbstractItemView,get_current_screen_desktop,getbody,\
    getsearchindex,ShowMovieAndOther,sovedict
from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QHBoxLayout,QGridLayout,QTableWidgetItem
from PyQt5.QtGui import  QIcon,QResizeEvent
from PyQt5.QtCore import Qt
# from body import appServerFeedbackBody
from mongo import Mongodb_connect
import sys
import logging
import json


logging.basicConfig(level=logging.INFO)

class Appserverlog():
    def get_feedback(self):
        pass


class AppserverWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.alldata = []
        self.uncertainKeys = []
        self.uncertaomdata = {}
        self.allmongodata  = []
        self.setwindow()

    def setinitdata(self):
        self.time = ["时间"]
        self.email = ["email"]
        self.method = ["method"]
        self.accountid = ["accountID"]
        self.phoneOS = ["PhoneOS"]
        self.appversion = ["Appversion"]
        self.timezone = ["TimeZone"]
    def setwindow(self):
        self.setWindowTitle("appServerFeedback")
        self.setWindowIcon(QIcon("./pic/kibana.png"))
        self.setGeometry(20, 80, int(get_current_screen_desktop().width()*0.9), int(get_current_screen_desktop().height()*0.8))
        self.table = Tablewidget(self)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.table.setGeometry(0, 80, self.width(), self.height() - 100)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置启用右键模式
        self.table.clicked.connect(self.cell_click_event)
        self.table.doubleClicked.connect(self.showContentByAdaptive)
        # self.table.customContextMenuRequested.connect(self.rightmenushow)
        self.lable = QLabel(self)
        self.lable.setText("输入email或者accountid")
        self.textwindow = QLineEdit(self)
        self.db_search  = QPushButton("DBsearch",self)
        self.btn_search = QPushButton("serach",self)
        self.btn_search.setDisabled(True)
        self.db_search.clicked.connect(self.click_DB_search_button)
        self.btn_search.clicked.connect(self.click_search_button)

        self.top = QWidget()
        toplayout = QHBoxLayout()
        toplayout.addWidget(self.lable,1)
        toplayout.addWidget(self.textwindow,8)
        toplayout.addWidget(self.db_search ,1)
        toplayout.addWidget(self.btn_search,1)
        self.top.setLayout(toplayout)

        mainlayout = QGridLayout()
        mainlayout.addWidget(self.top,0,0,1,10)
        mainlayout.addWidget(self.table,1,0,20,10)
        self.setLayout(mainlayout)
        self.show()
    def cell_click_event(self):
        row = self.table.currentRow()
        self.table.textwindow_text = self.allmongodata[row -1]
        logging.debug("self.table.textwindow_text:{}".format(self.table.textwindow_text))
    def click_DB_search_button(self):
        self.table.clear()
        self.alldata.clear()
        self.uncertainKeys.clear()
        self.uncertaomdata.clear()
        ShowMovieAndOther(self, self.deal_mongodb_feedback_data, self.showdata)
    def deal_mongodb_feedback_data(self):
        text = self.textwindow.text().split()[0]
        DB = Mongodb_connect(flags="all")
        s = ""
        if "." not in text:
            s   = {"accountID":"{}".format(text)}
        else:
            s = {"email":"{}".format(text)}
        DB.connect_mongodb(s, collection="feedback_file_log")
        data = DB.getallfeedbackdata()
        logging.info("searching feedback_file_log")
        # DB.connect_mongodb(s, collection="user_feedback_log")
        number = 0
        for s in data:
            self.allmongodata.append(s)
            number += 1
            self.add_uncertain_data(s,number)
        logging.info("searching user_feedback_log")
        DB.connect_mongodb(s, collection= "user_feedback_log")
        data1 = DB.getallfeedbackdata()
        for d in data1:
            self.allmongodata.append(d)
            number += 1
            self.add_uncertain_data(d,number)
        # if "_id" in self.uncertainKeys:
        #     del self.uncertainKeys[self.uncertainKeys.index("_id")]
        #     del self.uncertaomdata["_id"]
        for a in self.uncertainKeys:
            self.alldata.append([])
            self.alldata[-1].append(a)
            for s in self.uncertaomdata[a]:
                self.alldata[-1].append(s)
        logging.info("\nself.alldata:{}".format(self.alldata))

    def click_search_button(self):
        self.table.clear()
        self.alldata.clear()
        self.uncertainKeys.clear()
        self.uncertaomdata.clear()
        self.allmongodata.clear()
        self.setinitdata()
        text = self.textwindow.text()
        logging.debug("self.textwidonw.text:{}".format(text))
        if "must" not in appServerFeedbackBody["query"]["bool"]:
            appServerFeedbackBody["query"]["bool"]["must"] = {"query_string":{"query":""}}
        appServerFeedbackBody["query"]["bool"]["must"]["query_string"]["query"] = "\"{}\"".format(text.split()[0])
        self.body = getbody(appServerFeedbackBody,isFilter=False,sort={"@timestamp": {"order": "desc"}})
        logging.debug("body:{}".format(self.body))
        self.index = getsearchindex("cloud-appserver",days=20)
        ShowMovieAndOther(self,self.get_allsearch_data,self.showdata)

    def get_allsearch_data(self):
        result = GetElasticsearchData(self.body,self.index).getalldata()
        logging.debug("Elasticsearch_result:{}".format(result))
        datanumber = 0
        for d in result["hits"]["hits"]:
            logging.debug("data:{}".format(d["_source"]))
            self.time.append(sovedict(d["_source"],"@timestamp"))
            self.method.append(sovedict(d["_source"],"request.context.method"))
            self.phoneOS.append(sovedict(d["_source"],"request.context.phoneOS"))
            self.appversion.append(sovedict(d["_source"],"request.context.appVersion"))
            self.timezone.append(sovedict(d["_source"],"request.context.timeZone"))
            datanumber += 1
            if self.method[-1] != "getUserFeedbacks":
                dd = "request.data"
                try:
                    self.add_uncertain_data(json.loads(sovedict(d["_source"], dd)), datanumber)
                except:
                    raise
            else:
                k = "response.result"
                s = json.loads(sovedict(d["_source"],k))
                for a in s["userFeedbacks"]:
                    if a["accountID"] == self.textwindow.text().split()[0] or a["email"] == self.textwindow.text().split()[0]:
                        try:
                            self.add_uncertain_data(a, datanumber)
                            break
                        except:
                            raise
            # try:
            #     self.add_uncertain_data(json.loads(sovedict(d["_source"],dd)),datanumber)
            # except:
            #     raise
        self.addAllData()

    def add_uncertain_data(self,data,number):
        '''
        :param data: request.data转换的字典
        :param number: 第几条request.data
        :return: None
        '''
        logging.debug("add_uncertain_data.data:{}".format(data))
        logging.debug("add_uncertain_data.data.type:{}".format(type(data)))
        logging.debug("number:{}".format(number))
        if number == 1:
            for d in data.keys():
                self.uncertainKeys.append(d)
                self.uncertaomdata[d] = []
                self.uncertaomdata[d].append(str(data[d]))
        else:
            for d in data.keys():
                if d not in self.uncertainKeys:
                    self.uncertainKeys.append(d)
                    self.uncertaomdata[d] = []
                    for s in range(number-1):
                        self.uncertaomdata[d].append("")
                    self.uncertaomdata[d].append(data[d])
            for k in self.uncertainKeys:
                try:
                    self.uncertaomdata[k].append(str(data[k]))
                except KeyError:
                    self.uncertaomdata[k].append("")
        logging.debug("self.uncertainKeys:{}".format(self.uncertainKeys))
        logging.debug("self.uncertaomdata:{}".format(self.uncertaomdata))

    def addAllData(self):
        self.alldata.append(self.time)
        self.alldata.append(self.method)
        self.alldata.append(self.phoneOS)
        self.alldata.append(self.appversion)
        self.alldata.append(self.timezone)
        for s in self.uncertainKeys:
            self.alldata.append(self.uncertaomdata[s])
        logging.info("\nself.alldata:{}".format(self.alldata))

    def showContentByAdaptive(self):
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()

    def showdata(self):
        data = self.alldata
        if len(data) != 0:
            self.table.setRowCount(len(data[0]) - 1)
            self.table.setColumnCount(len(data))
            for i in range(0, len(data)):  # 总列数,显示所有数据
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(data[i][0]))
                for j in range(1, len(data[0])):  # 总数据行数
                    ss = QTableWidgetItem(data[i][j])
                    self.table.setItem(j - 1, i, ss)
                    ss.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置所有单元格对齐方式

if __name__ == "__main__":
    d = QApplication(sys.argv)
    s = []
    s.append(AppserverWindow())
    d.exec_()
