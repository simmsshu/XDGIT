from PyQt5.QtWidgets import  QWidget,QLabel,QLineEdit,QPushButton,QComboBox,QTableWidget,QTableWidgetItem,QApplication,\
    QHBoxLayout,QVBoxLayout,QGridLayout,QFrame,QTextEdit,QCheckBox
from PyQt5.Qt import QIcon,QAbstractItemView
from PyQt5.QtCore import Qt,QThread
from needClass import ShowMovieAndOther,ShowMovie,GetElasticsearchData,getsearchindex,GetOpsData,ThreadMethod
import sys,logging,json,re
# logging.basicConfig(level=logging.INFO)
fnclicked = 0
class UserOnOffline(QWidget):
    def __init__(self):
        self.CIDS=[]
        self.alldata={}
        self.datasort=[]
        self.rows=0
        self._7ACID=[]
        self.logstart=0
        self.deviceName = {}
        super().__init__()
        self.showWindow()
    def showWindow(self):
        self.setGeometry(200,200,QApplication.desktop().width()-300,QApplication.desktop().height()-300)
        self.setGeometry(200, 100,1200,QApplication.desktop().height()-150)
        self.setWindowTitle("用户设备掉线查询")
        self.setWindowIcon(QIcon("./pic/kibana.png"))
        # self.setStyleSheet(
        #                    "QPushButton{border-radius:2px;background-color:gray;height:20px;width:60px}")
        # self.setWindowIcon(QIcon("./kibana.png"))

        self.topwidget = QWidget(self)
        self.toplayout = QHBoxLayout()
        self.topwidget.setLayout(self.toplayout)

        self.middlewidget = QWidget(self)
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.setStretch(0, 0)
        # 设置主布局和子布局
        self.lab0 = QLabel("UserID查询",self)
        self.linetext0 = QLineEdit(self)
        self.linetext0.setPlaceholderText("输入查询条件")
        self.combox0 = QComboBox(self)
        self.combox0.addItems(["today", "7 days", "30 days"])
        self.combox0.setCurrentIndex(1)
        self.btn0  = QPushButton("查询", self)
        self.btn0.clicked.connect(self.showWaitingAndGetdata)
        self.lab01 = QLabel("CID")
        self.combox01=QComboBox(self)
        self.combox01.currentTextChanged.connect(self.wetherShowreason)
        self.lab02 = QLabel("重连原因")
        self.checkbox0  =   QCheckBox(self)
        self.checkbox0.setChecked(True)
        self.checkbox0.stateChanged.connect(self.wetherShowreason)
        self.lab03 = QLabel("connect")
        self.checkbox01 = QCheckBox(self)
        self.checkbox01.setChecked(True)
        self.checkbox01.stateChanged.connect(self.wetherShowreason)

        self.lab04 = QLabel("掉线")
        self.checkbox02 = QCheckBox(self)
        self.checkbox02.setChecked(True)
        self.checkbox02.stateChanged.connect(self.wetherShowreason)

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.table.setGeometry(0, 0, 880, 800)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textwindow = QTextEdit(self)
        self.textwindow.setVisible(False)

        self.Frame = QFrame(self)
        self.Frame.resize(self.width(), 100)
        self.buttomlayout = QHBoxLayout()
        self.Frame.setLayout(self.buttomlayout)
        self.lable3 = QLabel(self.Frame)
        self.lable3.setGeometry(0, 0, 10, 40)

        self.btn31 = QPushButton("上一页", self.Frame)
        self.btn31.setEnabled(False)
        self.btn31.clicked.connect(self.frontOrNextPage)
        self.btn32 = QPushButton("下一页", self.Frame)
        self.btn32.setEnabled(False)
        self.btn32.clicked.connect(self.frontOrNextPage)

        self.frame3 = QFrame(self.Frame)
        self.buttomlayout.addWidget(self.lable3, Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.btn31, Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.btn32, Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.frame3, Qt.AlignVCenter)
        self.buttomlayout.setStretchFactor(self.lable3, 4)
        self.buttomlayout.setStretchFactor(self.btn31, 1)
        self.buttomlayout.setStretchFactor(self.btn32, 1)
        self.buttomlayout.setStretchFactor(self.frame3, 4)

        self.toplayout.addWidget(self.lab0, Qt.AlignTop)
        self.toplayout.addWidget(self.linetext0, Qt.AlignTop)
        self.toplayout.addWidget(self.combox0, Qt.AlignTop)
        self.toplayout.addWidget(self.btn0, Qt.AlignTop)
        self.toplayout.addWidget(self.lab01, Qt.AlignTop,Qt.AlignRight)
        self.toplayout.addWidget(self.combox01, Qt.AlignTop)
        self.toplayout.addWidget(self.lab02, Qt.AlignTop,Qt.AlignRight)
        self.toplayout.addWidget(self.checkbox0, Qt.AlignTop)
        self.toplayout.addWidget(self.lab03, Qt.AlignTop,Qt.AlignRight)
        self.toplayout.addWidget(self.checkbox01, Qt.AlignTop)
        self.toplayout.addWidget(self.lab04, Qt.AlignTop,Qt.AlignRight)
        self.toplayout.addWidget(self.checkbox02, Qt.AlignTop)

        self.toplayout.setStretchFactor(self.lab0, 1)
        self.toplayout.setStretchFactor(self.linetext0,2)
        self.toplayout.setStretchFactor(self.combox0, 1)
        self.toplayout.setStretchFactor(self.btn0, 1)
        self.toplayout.setStretchFactor(self.lab01, 1)
        self.toplayout.setStretchFactor(self.combox01, 4)
        self.toplayout.setStretchFactor(self.lab02, 1)
        self.toplayout.setStretchFactor(self.checkbox0, 1)
        self.toplayout.setStretchFactor(self.lab03,1)
        self.toplayout.setStretchFactor(self.checkbox01,1)
        self.toplayout.setStretchFactor(self.lab04,1)
        self.toplayout.setStretchFactor(self.checkbox02,1)

        self.mainlayout.addWidget(self.topwidget, 1, Qt.AlignTop)
        self.mainlayout.addWidget(self.table, 30)
        self.mainlayout.addWidget(self.Frame, 1, Qt.AlignBottom)

        self.show()
    def wetherShowreason(self):
        list_cid_rows=[]
        try:
            if self.combox01.currentText() == "ALL":
                for row in range(self.table.rowCount()):
                    self.table.setRowHidden(row,False)
                self.hideofshoreason(range(self.table.rowCount()),self.checkbox0.isChecked(),self.checkbox01.isChecked(),self.checkbox02.isChecked())
            else:
                for row1 in range(self.table.rowCount()):
                    if self.table.item(row1,3).text() != self.combox01.currentText():
                        self.table.setRowHidden(row1,True)
                    else:
                        self.table.setRowHidden(row1,False)
                        list_cid_rows.append(row1)
                self.hideofshoreason(list_cid_rows,self.checkbox0.isChecked(),self.checkbox01.isChecked(),self.checkbox02.isChecked())
        except AttributeError:
            pass

    def hideofshoreason(self,interrable,flag1,flag2,flag3):
        for row in interrable:
            a   =   self.table.item(row,4).text()
            if a != "connect" and a != "die":
                self.table.setRowHidden(row, not flag1)
            if a == "connect":
                self.table.setRowHidden(row, not flag2)
            if a == "die":
                self.table.setRowHidden(row, not flag3)

    def frontOrNextPage(self):
        self.btn31.setEnabled(False)
        self.btn32.setEnabled(False)
        sender=self.sender()
        global fnclicked
        if   sender.text() == "上一页":
            if fnclicked >= 1:
                fnclicked -= 1
                self.logstart = fnclicked * 1000
                self.showGIF = ShowMovieAndOther(self, self.getalldata, self.showdata)

            else:
                self.btn31.setEnabled(True)
                self.btn32.setEnabled(True)
        elif sender.text() == "下一页":
            if self._7Adata["hits"]["total"] <= 1000*(fnclicked+1) and  self.un7Adata["hits"]["total"]<= 1000*(fnclicked+1):
                self.btn31.setEnabled(True)
                self.btn32.setEnabled(True)
            else:
                fnclicked += 1
                self.logstart = fnclicked * 1000
                self.showGIF=ShowMovieAndOther(self, self.getalldata, self.showdata)


    def showWaitingAndGetdata(self):
        if self.linetext0.text() == "":
            pass
        else:
            self.checkbox0.setChecked(True)
            self.checkbox01.setChecked(True)
            self.checkbox02.setChecked(True)
            self.logstart=0
            self.showGIF = ShowMovieAndOther(self, self.getalldata, self.showdata)
    def getalldata(self):
        self.alldata.clear()
        self.datasort.clear()
        self.userid=self.linetext0.text().split()[0]
        if   self.combox0.currentText() == "today":
            self.days=1
        elif self.combox0.currentText() == "7 days":
            self.days = 7
        elif self.combox0.currentText() == "30 days":
            self.days = 30
        if self.userid == "":
            pass
        else:
            uslessinfo = GetOpsData(self.userid).getdata()
            self.CIDS.clear()
            self._7ACID.clear()
            try:
                for s in uslessinfo["otherDevicelist"]:
                    self.CIDS.append([s["device_cid"],s["device_model"]])
                    self.deviceName[s["device_cid"]] = s["device_name"]
                self.un7Adata = self.get7AWithUn7AData(cids=self.CIDS,start=self.logstart)

            except KeyError:
                self.un7Adata   =   {"hits":{"total":0,"hits":[]}}
            try:
                for y in uslessinfo["listDeviceInfo"]:
                    self._7ACID.append(y["id"])
                    self.deviceName[y["id"]] = y["alias"]
            except KeyError:
                self._7Adata = []
            self._7Adata =  self.get7AWithUn7AData(Userid=self.userid,start=self.logstart)
            self.rows   =   self.getLimitTotal(self._7Adata["hits"]["total"],500)+self.getLimitTotal(self.un7Adata["hits"]["total"],500)
            # print( self._7Adata["hits"]["total"],self.un7Adata["hits"]["total"])

            # if self._7Adata["hits"]["total"] != 0 and self.un7Adata["hits"]["total"] != 0:
            #     x=0
            #     #内层循环遍历数量
            #     v=0
            #     #外层循环遍历数量
            #     k=0
            #     for a in self._7Adata["hits"]["hits"]:
            #         time = self.getdictdata(a["_source"],"T").replace("T","  ")
            #         cid  = self.getdictdata(a["_source"],"cid")
            #         M    = self.get7AMData(self.getdictdata(a["_source"],"M"),a)
            #         host = self.getdictdata(a["_source"]["host"],"name")
            #         model= "7AOutlet"
            #         list1=[time,model,cid,M,host]
            #         if x >= self.un7Adata["hits"]["total"]:
            #             #如果内层循环跑完，则外层直接赋值给alldata
            #             self.alldata.append(list1)
            #             v+=1
            #             k+=1
            #             print("内层循环结束"+str(v),str(k),str(x))
            #         else:
            #             v+=1
            #             # print(str(v),str(k),str(x))
            #         for b in self.un7Adata["hits"]["hits"][x:]:
            #             k+=1
            #             time1   =   self.getdictdata(b["_source"],"T").replace("T","  ")
            #             cid1    =   ""
            #             model1  =   ""
            #             for cids in self.CIDS:
            #                 if cids[0] in self.getdictdata(b["_source"],"M"):
            #                     cid1    =   cids[0]
            #                     model1  =   cids[1]
            #                 else:
            #                     pass
            #             host1   =   self.getdictdata(b["_source"]["host"],"name")
            #             M1      =   self.getVdmpOnOfflinedata(self.getdictdata(b["_source"],"M"))
            #             list2   =   [time1,model1,cid1,M1,host1]
            #             if v == self._7Adata["hits"]["total"]:
            #             # 如果外层最小值大于内层某值，直接将内层值给alldata
            #                 self.alldata.append(list2)
            #                 print("外层循环结束" + str(v), str(k), str(x))
            #             if time <=  time1:
            #                 self.alldata.append(list2)
            #                 print("外层小于内层" + str(v), str(k), str(x))
            #                 x   +=  1
            #                 if x == self.un7Adata["hits"]["total"]:
            #                     self.alldata.append(list1)
            #             else:
            #                 self.alldata.append(list1)
            #                 print("外层大于内层" + str(v), str(k), str(x))
            #                 if v >= self._7Adata["hits"]["total"]:
            #                     print("外层循环结束"+str(v))
            #                     # 如果外层最小值大于内层某值，不跳出循环
            #                     pass
            #                 else:
            #                     break
            keyflag=0
            # if self._7Adata["hits"]["total"] != 0 and self.un7Adata["hits"]["total"] != 0:
            for a in self._7Adata["hits"]["hits"]:
                time = self.getdictdata(a["_source"],"T").replace("T","  ")
                cid  = self.getdictdata(a["_source"],"cid")
                M    = self.get7AMData(self.getdictdata(a["_source"],"M"),a)
                host = self.getdictdata(a["_source"]["host"],"name")
                model= "7AOutlet"
                try:
                    routermac = self.getRegexData(self.getdictdata(a["_source"],"data"),re.compile(r'"routerMac":"(.*?)"'))
                    wifiName  = self.getRegexData(self.getdictdata(a["_source"],"data"),re.compile(r'"wifiName":"(.*?)"'))
                    rssi = self.getRegexData(self.getdictdata(a["_source"], "data"),
                                                 re.compile(r'"rssi":(.*?),'))
                except KeyError:
                    routermac = ""
                    wifiName  = ""
                try:
                    self.alldata[time+str(keyflag)] = [time,model,self.deviceName[cid],cid,M,wifiName,rssi,routermac,host]
                except KeyError:
                    pass
                keyflag += 1
            for b in self.un7Adata["hits"]["hits"]:
                # print(b["_source"]["M"])
                time1   =   self.getdictdata(b["_source"],"T").replace("T","  ")
                cid1    =   ""
                model1  =   ""
                for cids in self.CIDS:
                    if cids[0] in self.getdictdata(b["_source"],"M"):
                        cid1    =   cids[0]
                        model1  =   cids[1]
                    else:
                        pass
                host1   =   self.getdictdata(b["_source"]["host"],"name")
                M1      =   self.getVdmpOnOfflinedata(self.getdictdata(b["_source"],"M"))
                rssi1 = self.getRegexData(b["_source"]["M"], re.compile(r'"rssi":(.*?),'))
                routermac1 = self.getRegexData(b["_source"]["M"], re.compile(r'"routerMac":"(.*?)"'))
                wifiName1  = self.getRegexData(b["_source"]["M"], re.compile(r'"wifiName":"(.*?)"'))
                self.alldata[time1 + str(keyflag)] = [time1, model1, self.deviceName[cid1], cid1, M1,wifiName1,rssi1, routermac1, host1]
                keyflag += 1
            # for key in self.alldata.keys():
            #     print(self.alldata[key])


            # elif self._7Adata["hits"]["total"] == 0 and self.un7Adata["hits"]["total"] != 0:
            #     for b in self.un7Adata["hits"]["hits"]:
            #         time1 = self.getdictdata(b["_source"], "T")
            #         cid1 = ""
            #         model1 = ""
            #         for cids in self.CIDS:
            #             if cids[0] in self.getdictdata(b["_source"], "M"):
            #                 cid1 = cids[0]
            #                 model1 = cids[1]
            #             else:
            #                 pass
            #         host1 = self.getdictdata(b["_source"]["host"], "name")
            #         M1 = self.getVdmpOnOfflinedata(self.getdictdata(b["_source"], "M"))
            #         self.alldata[time1 + str(keyflag)] = [time1, model1, cid1, M1, host1]
            #         keyflag += 1
            #
            # elif self._7Adata["hits"]["total"] != 0 and self.un7Adata["hits"]["total"] == 0:
            #     for a in self._7Adata["hits"]["hits"]:
            #         time = self.getdictdata(a["_source"],"T")
            #         cid  = self.getdictdata(a["_source"],"cid")
            #         M    = self.get7AMData(self.getdictdata(a["_source"],"M"),a)
            #         host = self.getdictdata(a["_source"]["host"],"name")
            #         model= "7AOutlet"
            #         self.alldata[time + str(keyflag)] = [time, model, cid, M, host]
            #         keyflag += 1
            # else:
            #     pass
            self.datasort = sorted(self.alldata.keys(),reverse = True)

    def getLimitTotal(self,total,limit):
        if total > limit:
            return limit
        else:
            return total
    # def keyPressEvent(self, QKeyEvent):
    #     a=self.combox01.currentIndex()
    #     if QKeyEvent == Qt.Key_Down:
    #         if a < self.combox01.count() - 1:
    #             self.combox01.setCurrentIndex(a+1)
    #         else:
    #             pass
    #     elif QKeyEvent == Qt.Key_Up:
    #         if a > 0:
    #             self.combox01.setCurrentIndex(a - 1)
    #         else:
    #             pass
    #     else:
    #         print(QKeyEvent)
    def get7AMData(self,Mdata,alldata):
        if Mdata    ==  "Registration Successful":
            return "connect"
        elif Mdata  ==  "close connect":
            return "die"
        elif Mdata  ==  "device login info":
            return self.getRegexData(alldata["_source"]["data"],re.compile(r'"initState":"(.*?)"'))
        else:
            return ""

    def getVdmpOnOfflinedata(self,data):
        if "die with" in data:
            return "die"
        elif "ConnectPacket" in data:
            return "connect"
        elif "initState" in data:
            a   =   self.getRegexData(data,re.compile(r'"initState":"(.*?)"'))
            b   =   self.getRegexData(data,re.compile(r'"retry":"(.*?)"'))
            return a+" "+b
        else:
            return ""
    def getRegexData(self,regexdata,finddata):
        s   =   finddata.search(regexdata)
        if isinstance(s,type(None)):
            return ""
        else:
            return s.group(1)
    def getdictdata(self,dictinfo,key):
        try:
            return dictinfo[key]
        except KeyError:
            return ""
    def showdata(self):
        self.combox01.clear()
        self.table.clear()
        self.combox01.addItem("ALL")
        self.btn31.setEnabled(True)
        self.btn32.setEnabled(True)
        for cid in self.CIDS:
            self.combox01.addItem(cid[0])
        self.combox01.addItems(self._7ACID)
        self.table.setColumnCount(9)
        self.table.setRowCount(len(self._7Adata["hits"]["hits"]) + len(self.un7Adata["hits"]["hits"]))
        self.table.setHorizontalHeaderItem(0,QTableWidgetItem("time"))
        self.table.setHorizontalHeaderItem(1, QTableWidgetItem("model"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("设备名"))
        self.table.setHorizontalHeaderItem(3, QTableWidgetItem("CID"))
        self.table.setHorizontalHeaderItem(4, QTableWidgetItem("连接状态"))
        self.table.setHorizontalHeaderItem(5, QTableWidgetItem("wifiName"))
        self.table.setHorizontalHeaderItem(6, QTableWidgetItem("rssi"))
        self.table.setHorizontalHeaderItem(7, QTableWidgetItem("routerMac"))
        self.table.setHorizontalHeaderItem(8, QTableWidgetItem("host"))
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 250)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 50)
        self.table.setColumnWidth(7, 150)
        self.table.setColumnWidth(8, 200)

        for a in range(len(self.datasort)):
            for b in range(9):
                self.table.setItem(a,b,QTableWidgetItem(self.alldata[self.datasort[a]][b]))

    def get7AWithUn7AData(self,cids=[[]],Userid="",start=0):
        if Userid != "":
            body1 = {
                "size": 500,  # 返回查询条数
                "from": start,  # 返回起始页
                "sort": {"T": {"order": "desc"}},  # 排序
                "_source": ["data", "T", "host.name","M","cid"],  # 返回指定字段
                "query": {
                    "bool": {
                        "minimum_should_match": 2,
                        "should": [
                            {
                                "match_phrase": {
                                    "M": "close connect"
                                }
                            },
                            {
                                "match_phrase": {
                                    "M": "Registration Successful"
                                }
                            },
                            {
                                "match_phrase": {
                                    "M": {
                                        "query": "device login info"
                                    }
                                }
                            },
                            {"match_phrase": {
                                "accountId": {
                                    "query": "{}".format(Userid)
                                }
                            }}
                        ]
                    }
                }
            }
            index=getsearchindex("cloud-wifioutlet7a",days=self.days)
            logging.debug("7A elasticsearch info")
            logging.debug("7A request Elasticsearch body")
            logging.debug(str(body1))
            logging.debug("7A request Elasticsearch index")
            logging.debug(str(index))
            return GetElasticsearchData(body1,index).getalldata()

        else:
            body = {
                "size": 500,  # 返回查询条数
                "from": start,  # 返回起始页
                "sort": {"T": {"order": "desc"}},  # 排序
                "_source": ["M", "T", "host.name"],  # 返回指定字段
                "query": {
                    "bool": {
                        "minimum_should_match": 1,
                        "should": [
                            {
                                "match_phrase": {
                                    "M": "die with"
                                }
                            },
                            {
                                "match_phrase": {
                                    "M": "connectPacket"
                                }
                            },
                            {
                                "match": {
                                    "M": {
                                        "operator": "and",
                                        "query": "initstate publish received"
                                    }
                                }
                            }

                        ],
                        "must": {
                            "bool": {
                                "minimum_should_match": 1,
                                "should": []
                            }
                        }
                    }
                }

            }
            for cid in cids:
                body["query"]["bool"]["must"]["bool"]["should"].append({
                    "match_phrase":{
                        "M":{
                            "query":"{}".format(cid[0])
                        }
                    }
                })
            index=getsearchindex("vdmp-online",days=self.days)
            return GetElasticsearchData(body, index).getalldata()



if __name__ == "__main__":
    pass