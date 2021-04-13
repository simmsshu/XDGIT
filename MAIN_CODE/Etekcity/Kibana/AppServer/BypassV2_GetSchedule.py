import datetime
import sys
import json
from MAIN_CODE.body import _BypassV2_Getschedule
from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QPushButton,QLabel,QHBoxLayout,QVBoxLayout
from BASE_ABOUT.needClass import get_current_screen_desktop,getsearchindex,\
    Tablewidget,ShowMovieAndOther,GetElasticsearchData,sovedict
class BypassV2Getschedule(QWidget):
    def __init__(self,parent = None):
        super(BypassV2Getschedule, self).__init__()
        if parent:
            self.setParent(parent)
        else:
            self.setGeometry(100,100,get_current_screen_desktop().width()-200,get_current_screen_desktop().height()-200)
        self.alldata = []
        self.mainlayout = QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.topwidget = QWidget(self)
        self.table = Tablewidget(self)
        self.table.doubleClicked.connect(self.doubleclicked)
        self.mainlayout.addWidget(self.topwidget,1)
        self.mainlayout.addWidget(self.table,30)
        self.toplayout = QHBoxLayout()
        self.topwidget.setLayout(self.toplayout)

        self.lab1 =QLabel("AccountID&CID",self.topwidget)
        self.lintext1 = QLineEdit(self.topwidget)
        self.btn1     = QPushButton("确认",self.topwidget)
        self.btn1.clicked.connect(self.getdataAndshow)
        self.toplayout.addWidget(self.lab1,1)
        self.toplayout.addWidget(self.lintext1,10)
        self.toplayout.addWidget(self.btn1,1)
        self.show()

    def getdataAndshow(self):
        self.alldata.clear()
        ShowMovieAndOther(self,self.getresponse,self.showdata)

    def getresponse(self):
        if self.lintext1.text().split() != "":
            body = _BypassV2_Getschedule
            body["query"]["bool"]["must"].append(
                {"query_string":{"query":"{}".format(self.lintext1.text().split()[0])}})
            index = getsearchindex("cloud-appserver-new",days=15,connect="-")
        print("body:{}".format(body))
        print("index:{}".format(index))
        rs = GetElasticsearchData(body,index).getalldata()
        self.get_all_data(rs)

    def get_all_data(self,rs):
        time    = ["时间"]
        userid  = ["UserID"]
        phbrand = ["机型"]
        os      = ["系统"]
        timezone= ["时区"]
        cid     = ["CID"]
        dcmodel = ["设备型号"]
        schnum  = ["num"]
        schid   = ["schid"]
        sttime  = ["开始时间"]
        startAC = ["执行动作"]
        sunrise = ["sunrise"]
        enable  = ["enable"]
        repeat  = ["rapeat"]
        for k in rs["hits"]["hits"]:
            data = k["_source"]
            try:
                time.append(sovedict(data,"time"))
                userid.append(sovedict(data,"request.context.accountID"))
                phbrand.append(sovedict(data,"request.context.phoneBrand"))
                os.append(sovedict(data,"request.context.phoneOS"))
                timezone.append(sovedict(data,"request.context.timeZone"))
                try:
                    requestdata = eval(sovedict(data,"request.data"))
                    cid.append(sovedict(requestdata,"cid"))
                    dcmodel.append(sovedict(requestdata,"configModule"))
                    try:
                        responseresult = json.loads(sovedict(data, "response.result"))
                        schnum.append(sovedict(responseresult, "result.total"))
                        if sovedict(responseresult, "result.total") == 0:
                            schid.append("")
                            sttime.append("")
                            startAC.append("")
                            sunrise.append("")
                            enable.append("")
                            repeat.append("")
                        else:
                            for s in responseresult["result"]["schedules"]:
                                schid.append(str(s["id"]))
                                sttime.append(str(datetime.datetime.utcfromtimestamp(s["startTs"])))
                                startAC.append(str(s["startAct"]))
                                sunrise.append(str(s["sunrise"]))
                                enable.append(str(s["enabled"]))
                                repeat.append(str(s["repeat"]))
                    except Exception as e:
                        schnum.append("")
                        schid.append("")
                        sttime.append("")
                        startAC.append("")
                        sunrise.append("")
                        enable.append("")
                        repeat.append("")
                except:
                    cid.append("")
                    dcmodel.append("")
                    try:
                        responseresult = json.loads(sovedict(data, "response.result"))
                        schnum.append(sovedict(responseresult, "result.total"))
                        if sovedict(responseresult, "result.total") == 0:
                            schid.append("")
                            sttime.append("")
                            startAC.append("")
                            sunrise.append("")
                            enable.append("")
                            repeat.append("")
                        else:
                            for s in responseresult["result"]["schedules"]:
                                schid.append(str(s["id"]))
                                sttime.append(str(datetime.datetime.utcfromtimestamp(s["startTs"])))
                                startAC.append(str(s["startAct"]))
                                sunrise.append(str(s["sunrise"]))
                                enable.append(str(s["enabled"]))
                                repeat.append(str(s["repeat"]))
                    except Exception as e:
                        schnum.append("")
                        schid.append("")
                        sttime.append("")
                        startAC.append("")
                        sunrise.append("")
                        enable.append("")
                        repeat.append("")
                    # raise e

            except:
                raise
            g +=1
        self.alldata.append(time)
        self.alldata.append(userid)
        self.alldata.append(phbrand)
        self.alldata.append(os)
        self.alldata.append(timezone)
        self.alldata.append(cid)
        self.alldata.append(dcmodel)
        self.alldata.append(schnum)
        self.alldata.append(schid)
        self.alldata.append(sttime)
        self.alldata.append(startAC)
        self.alldata.append(sunrise)
        self.alldata.append(enable)
        self.alldata.append(repeat)

    def doubleclicked(self):
        sender = self.sender()
        sender.currentColumn()
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()

    def showdata(self):
        # print(self.alldata)
        for x in self.alldata:
            print(len(x))
        self.table.showdata(self.alldata)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = BypassV2Getschedule()
    d.show()
    app.exec_()