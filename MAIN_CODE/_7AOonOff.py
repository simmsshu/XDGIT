from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication,QGridLayout,QPushButton,QLineEdit,QLabel
from needClass import getsearchindex,getbody,Tablewidget,GetElasticsearchData,addKeyAndValeToDict,\
    ShowMovie,ShowMovieAndOther
from body import _7AOnOffbody
import sys,re

class UI():
    def __init__(self):
        self.body = {}
        self.alldata = []
        self.T = ["时间"]
        self.acocuntid = ["accountid"]
        self.cid = ["cid"]
        self.onoffsource = ["开关来源"]
        self.sendOrRevicedata = ["数据"]
        self.Traceid = ["traceid"]
        self.dellistvalue = int
        self.traceid = ""
        self.showUI()
    def showUI(self):
        self.win = MainWindow()
        self.win.setTitle("7A开关查询")
        mainlayout = QGridLayout(self.win)
        self.win.client.setLayout(mainlayout)
        self.lab1 = QLabel("请输入CID或accountid",self.win)
        self.line1 = QLineEdit(self.win)
        self.btn1 = QPushButton("确认",self.win)
        self.btn1.clicked.connect(self.searchandshow)
        self.table = Tablewidget(self.win)
        self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:transparent;color: white;}")
        self.table.verticalHeader().setVisible(False)
        mainlayout.addWidget(self.lab1,0,0,1,3)
        mainlayout.addWidget(self.line1,0,3,1,10)
        mainlayout.addWidget(self.btn1,0,13,1,2)
        mainlayout.addWidget(self.table,1,0,30,15)

        self.win.show()
    def searchandshow(self):
        self.table.clear()
        ShowMovieAndOther(self.win,self.searchdata,self.showDataByTable)
    def searchdata(self):
        cid = self.line1.text()
        index = getsearchindex(index="cloud-wifioutlet7a", days=15)
        self.body = getbody(_7AOnOffbody, isFilter=False)
        if cid != "":
            self.body["query"]["bool"] = addKeyAndValeToDict(self.body["query"]["bool"],"must",{"query_string":{"query":"\"{}\"".format(cid)}})
            rs = GetElasticsearchData(self.body, index).getalldata()
            if isinstance(re,type(None)):
                pass
            else:
                self.getonoffdata(rs,cid)
        else:
            pass
    def getgroup(self,pat,data):
        try:
            return pat.search(data).group(1)
        except:
            return ""

    def getonoffdata(self, data, cid):
        pat1 = re.compile(r"} {((.*?) (.*?))}}")
        if data:
            for logdata in data["hits"]["hits"]:
                self.T.append(logdata["_source"]["@timestamp"].replace("T","\t"))
                self.acocuntid.append(logdata["_source"]["accountId"])
                if "cid" in logdata["_source"].keys():
                    self.cid.append(logdata["_source"]["cid"])
                else:
                    self.cid.append("")
                if "traceId" in logdata["_source"].keys():
                    self.Traceid.append(logdata["_source"]["traceId"])
                else:
                    self.Traceid.append("")
                if logdata["_source"]["iName"] == "OnUserRequest" and "relay" in logdata["_source"]["msg"]:
                    self.onoffsource.append("app开关")
                    self.dellistvalue = len(self.onoffsource)
                    self.sendOrRevicedata.append(logdata["_source"]["msg"])
                    self.traceid = logdata["_source"]["traceId"]

                elif "trigger" in logdata["_source"]["M"]:
                    self.onoffsource.append("trigger")
                    self.sendOrRevicedata.append(logdata["_source"]["M"])
                elif "got state report" in logdata["_source"]["M"]:
                    self.onoffsource.append("手动开关")
                    self.sendOrRevicedata.append(logdata["_source"]["M"])

                elif "got timer event report" in logdata["_source"]["M"]:
                    self.onoffsource.append("执行记录")
                    self.sendOrRevicedata.append(logdata["_source"]["M"])

                elif "Alexa" in logdata["_source"]["message"] and logdata["_source"]["iName"] == "DeviceStatusPost":
                    self.onoffsource.append("alexa开关")
                    self.sendOrRevicedata.append(self.getgroup(pat1,logdata["_source"]["message"]))
                    self.wetherDeldata(logdata["_source"]["traceId"])

                elif "IFTTT " in logdata["_source"]["message"] and logdata["_source"]["iName"] == "DeviceStatusPost":
                    self.onoffsource.append("IFTTT开关")
                    self.sendOrRevicedata.append(self.getgroup(pat1,logdata["_source"]["message"]))
                    self.wetherDeldata(logdata["_source"]["traceId"])

                elif "linkageTriggerService " in logdata["_source"]["message"] and logdata["_source"]["iName"] == "DeviceStatusPost":
                    self.onoffsource.append("smart触发")
                    self.sendOrRevicedata.append(self.getgroup(pat1,logdata["_source"]["message"]))
                    self.wetherDeldata(logdata["_source"]["traceId"])

                elif    "msg" in logdata["_source"].keys():
                    if '"OTP":"on"' in logdata["_source"]["msg"]:
                        self.onoffsource.append("过流保护")
                        self.sendOrRevicedata.append(pat1.search(logdata["_source"]["msg"]))
                    else:
                        self.onoffsource.append("")
                        self.sendOrRevicedata.append("")

                elif    "url" in logdata["_source"].keys():
                    if "thirdparty" in logdata["_source"]["url"]:
                        self.onoffsource.append("第三方")
                        self.sendOrRevicedata.append(logdata["_source"]["url"])
                        self.wetherDeldata(logdata["_source"]["traceId"])
                    else:
                        self.onoffsource.append("")
                        self.sendOrRevicedata.append("")

                else:
                    self.onoffsource.append("")
                    self.sendOrRevicedata.append(logdata["_source"]["message"])
        self.alldata.clear()
        self.alldata.append(self.T)
        self.alldata.append(self.acocuntid)
        self.alldata.append(self.cid)
        self.alldata.append(self.onoffsource)
        self.alldata.append(self.sendOrRevicedata)
        self.alldata.append(self.Traceid)

    def showDataByTable(self):
        self.table.showdata(self.alldata)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 270)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 600)
        self.table.setColumnWidth(5, 280)

    def wetherDeldata(self,traceid):
        if self.traceid == traceid:
            del self.T[self.dellistvalue-1]
            del self.acocuntid[self.dellistvalue-1]
            del self.cid[self.dellistvalue-1]
            del self.Traceid[self.dellistvalue-1]
            del self.onoffsource[self.dellistvalue-1]
            del self.sendOrRevicedata[self.dellistvalue-1]
            self.traceid = ""
            self.dellistvalue = 0
        else:
            pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    a = UI()
    a.showUI()
    win.show()
    sys.exit(app.exec_())