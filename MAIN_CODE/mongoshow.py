# from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,\
#     QLabel,QLineEdit,QTableWidget,QTableWidgetItem,QAbstractItemView,QApplication
from PyQt5.QtWidgets import QWidget,QPushButton,QLineEdit,QLabel,QTableWidget,QTableWidgetItem,QAbstractItemView,QComboBox,QFrame,QGridLayout,QMainWindow,QCalendarWidget,\
    QLabel,QMessageBox,QTextEdit,QMenu,QAction
from PyQt5.QtGui import QIcon,QFont,QMouseEvent,QCursor,QKeySequence
from PyQt5.QtCore import Qt,QDate
from mongo import Mongodb_connect
from getiplocation import FromIpgetLocation
from getiplocation import FromRouterGetVender
from bson import ObjectId
import qdarkstyle
import dateutil.parser
from isodate import isodatetime
import sys,datetime,json,os,re
import logging
logging.basicConfig(level=logging.DEBUG)

class MongoShow(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        if parent:
            self.setParent(parent)
        else:
            pass
        self.clickednum =[0,0,0]#1.记录self.btn3点击次数
        self.startdate  =""
        self.enddate    =""
        self.aggregatelist=[]
        self.dict       ={} #访问mongodb查询条件，不包括排序，skip，limit
        self.skip       =0 #设置上下页略过的起始值
        self.stacomb2getlist=[]#从mongodb动态获取组类列表存放，用户判断stacomb2是否手动输入
        self.staticdata ={}#用作判断数据统计的数据是要进行匹配还是进行统计，统计值为A,匹配值为B
        self.staticlist =[]#用作数据统计添加元素顺序，便于添加删除
        self.quirelist  = [{"$match": {"createTime":{'$gt':"2020-05-01T00:00:00",\
                                                   '$lt':datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M%S")}}},\
                           {"$group": {"_id": {}, "count": {"$sum": 1}}},
                           {"$limit":1000}]  # aggregate聚合列表
        #数据统计stacombo1创建对照表
        self.staticmainbox = {"产品型号": "ConfigModule", "ErrCode": "DetailInfo.Step4_DeviceReturnData.CurrentConfig.Result.err" \
            , "APP版本": "AppVersion", "OSVersion": "OSVersion", "配网结果": "Result",
                         "SSID": "DetailInfo.Step3_ConfigInfo.wifiSSID", "手机型号": "MobileType", "AccountID": "UserID"}
        self.dataflag   = 0 #用于判断选择的日期是组合查询选择还是数据统计选择

        self.setWindowOpacity(1)
        # self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowTitle("配网日志")
        self.setWindowIcon(QIcon("./pic/kibana.png"))
        self.setGeometry(20, 80, 1330, 900)
        self.table=QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setGeometry(0, 80, self.width(), self.height() - 100)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)#设置启用右键模式
        self.table.customContextMenuRequested.connect(self.rightmenushow)
        self.combobox1=QComboBox(self)
        self.combobox1.addItem("accountid&CID查询")
        self.combobox1.addItem("组合查询")
        self.combobox1.addItem("数据统计")
        self.combobox1.textActivated.connect(self.comboboxchoiced)
        # 组合查询添加3个选择查询
        self.combobox2=QComboBox(self)
        self.combobox2.setVisible(False)
        self.combobox3=QComboBox(self)
        self.combobox3.setVisible(False)
        self.combobox4=QComboBox(self)
        self.combobox4.setVisible(False)

        #数据统计显示及触发控制
        self.stacomb1=QComboBox(self)
        self.stacomb1.setToolTip("支持mongoshell查询，可输入键值")
        # self.stacomb1.setWindowIconText("选择主类")
        self.stacomb1.activated.connect(self.set_sta2combitem)
        self.stacomb2 = QComboBox(self)
        self.stacomb2.setToolTip("选择ALL默认进行分组统计，选择单项进行匹配查询，可支持模糊匹配,如regex:myspectrum(注意冒号需为英文冒号)")
        # self.stacomb2.setWindowIconText("选择分支")
        self.stabtngetlist=QPushButton("获取所有")
        self.stabtngetlist.setToolTip("从数据库动态获取所有类型")
        self.stabtngetlist.clicked.connect(self.get_sta2combitembyconnectmongo)
        self.stabtnaddson=QPushButton("添加",self)
        self.stabtnaddson.clicked.connect(self.addordeletquiredata)
        self.stabtndelson=QPushButton("删除",self)
        self.stabtndelson.clicked.connect(self.addordeletquiredata)
        self.selectdatatime=QPushButton("选择时间")
        self.selectdatatime.clicked.connect(self.showOrhidCalender)
        self.stabtnsearch=QPushButton("查询",self)
        self.stabtnsearch.clicked.connect(self.getdataformmongobyaggregate)
        self.statext=QLineEdit(self)

        #设置控件默认不可见
        self.stacomb1.setVisible(False)
        self.stacomb2.setVisible(False)
        self.stabtngetlist.setVisible(False)
        self.stabtnaddson.setVisible(False)
        self.stabtndelson.setVisible(False)
        self.selectdatatime.setVisible(False)
        self.stabtnsearch.setVisible(False)
        self.statext.setVisible(False)
        #设置文本框不可编辑
        self.statext.setReadOnly(False)
        #设置stacomb1条目
        list1=["产品型号","ErrCode","APP版本","OSVersion","配网结果","SSID","手机型号","AccountID"]
        #设置stacomb1选中触发stacomb2条目
        self.stacomb1.addItems(list1)
        #设置stacomb可编辑
        self.stacomb1.setEditable(True)
        self.stacomb2.setEditable(True)
        #设置stacomb2初始条目
        list2=["ALL",'WiFi_AirFryer_CS158-AF_EU', 'WiFiBT_Oven_CS130-AO', 'InwallSwitch3way', 'InwallswitchUS', 'OutdoorSocket15A', 'InwallSwitch3way', 'WiFi_Bulb_WhiteLightBulb_US', 'AirPurifier131', 'WifiSmartBulb', '10AOutletUS', '10AOutletEU', 'WifiWallDimmer', '15AOutletNightlight', 'WiFiBT_Scale_FatScalePlus_US', '7AOutlet', 'WiFi_SKA_AirFryer137_US', 'WiFi_Bulb_MulticolorBulb_US']
        self.stacomb2.addItems(list2)


        self.box1 = QLineEdit()
        self.box2 = QLineEdit()#组合查询添加3个输入框
        self.box2.setVisible(False)
        self.box3 = QLineEdit()
        self.box3.setVisible(False)
        self.box4 = QLineEdit()
        self.box4.setVisible(False)

        self.btn1 = QPushButton("查询", self)
        self.btn1.setEnabled(True)
        self.btn1.clicked.connect(self.accurateAccountorCid)
        self.btn11= QPushButton("查询所有", self)
        self.btn11.setEnabled(True)
        self.btn11.clicked.connect(self.accurateAccountorCid)
        self.btn2 = QPushButton("显示IPlocation&路由器厂商",self)
        self.btn2.setEnabled(False)
        self.btn2.clicked.connect(self.queryroutermacAndIPlocation)
        # self.btn3 = QPushButton("AddFilter",self)
        # self.btn3.setVisible(False)
        # self.btn3.clicked.connect()
        self.btn3 = QPushButton("search",self)
        self.btn3.setEnabled(False)
        self.btn3.clicked.connect(self.combinesearch)

        self.btn4 = QPushButton("上一页", self)
        self.btn4.setVisible(False)
        self.btn4.clicked.connect(self.frontandnext)

        self.btn5 = QPushButton("下一页", self)
        self.btn5.setVisible(False)
        self.btn5.clicked.connect(self.frontandnext)
        self.btn6=QPushButton("选择日期",self)
        self.btn6.setVisible(False)
        self.btn6.clicked.connect(self.showOrhidCalender)

        self.textwindow=QTextEdit(self)
        self.textwindow.setGeometry(0,60,1100,840)
        self.textwindow.setVisible(False)

        # self.btn5.clicked.connect(self.combinesearch)


        self.Glevel = QGridLayout(self)#占总宽度22，高度82
        self.Glevel.addWidget(self.combobox1, 0,0,1,3, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.box1, 0,3,1,11,Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.btn1,0,14,1,1,Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.btn11, 0, 15, 1, 1, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.btn2, 0, 16, 1, 5, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.btn3, 0, 21, 1, 1, Qt.AlignVCenter | Qt.AlignTop)

        self.Glevel.addWidget(self.combobox2, 1, 0, 1, 3, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.box2, 1, 3, 1, 4, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.combobox3, 1, 7, 1, 3, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.box3, 1, 10, 1, 4, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.combobox4, 1, 14, 1, 3, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.box4, 1, 17, 1, 3, Qt.AlignVCenter | Qt.AlignTop)
        self.Glevel.addWidget(self.btn6, 1, 20, 1, 2, Qt.AlignVCenter | Qt.AlignTop)

        self.Glevel.addWidget(self.stacomb1, 2, 0, 1, 6)
        self.Glevel.addWidget(self.stacomb2, 2, 6, 1, 6)
        self.Glevel.addWidget(self.stabtngetlist, 2, 12, 1, 2)
        self.Glevel.addWidget(self.stabtnaddson, 2, 14, 1, 2)
        self.Glevel.addWidget(self.stabtndelson, 2, 16, 1, 2)
        self.Glevel.addWidget(self.selectdatatime,2,18,1,2)
        self.Glevel.addWidget(self.stabtnsearch, 2, 20, 1, 2)
        self.Glevel.addWidget(self.statext, 3, 0, 1, 22)

        self.Glevel.addWidget(self.table,4,0,80,22)
        self.Glevel.addWidget(self.btn4, 84, 9, 1, 2)
        self.Glevel.addWidget(self.btn5, 84, 11, 1, 2)


        self.show()
    def getdataformmongobyaggregate(self):
        list1 = []  # 用于储存聚合的键值
        connect=Mongodb_connect(flags=2)
        connect.connect_mongodb(self.quirelist)
        data=connect.get_aggregatedata()
        for x in range(len(data)):
            data[x]["_id"]["count"] = data[x]["count"]
            data[x]=data[x]["_id"]
            data[x]=str(data[x])
        data.sort()
        # for y in range(len(data)):
        #     data[y]=data[y]
        for s in self.quirelist[1]["$group"]["_id"].keys():
            list1.append(s)
            self.aggregatelist.append([s])
        list1.append("count")
        self.aggregatelist.append(["count"])

        for x in data:
            for y in range(len(list1)):
                pat=self.refindemore(list1[y])
                try:
                    aa=pat.search(x)
                    if "\'" in aa.group(1):
                        self.aggregatelist[y].append(aa.group(1).replace("\'",""))
                    else:
                        self.aggregatelist[y].append(str(aa.group(1)))
                except AttributeError:
                    self.aggregatelist[y].append("None")
        self.showdata(self.aggregatelist)
        self.clearallaggregatelist()

    def clearallaggregatelist(self):
        self.staticdata.clear()
        self.staticlist.clear()
        self.quirelist[0]["$match"].clear()
        self.quirelist[1]["$group"]["_id"].clear()
        self.aggregatelist.clear()

    def refindemore(self,x):
        pat = re.compile(r"\'%s\':('(.*?)'|(.*?))(,|})" %x)
        return pat

    def rightmenushow(self):
        # if self.combobox1.currentText() =="accountid&CID查询":
        self.table_menu=QMenu(self.table)
        action1= QAction(u"show detail  F2",self)
        action2 =QAction(u"download json data",self)
        self.table_menu.addAction(action1)
        self.table_menu.addAction(action2)
        # action1.setShortcut('F2')
        # action1.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        action1.triggered.connect(self.show_detailinfo)
        action2.triggered.connect(self.sava_as_json)
        pos=QCursor.pos()#获取鼠标在父窗体当前相对位置
        self.table_menu.move(pos)
        self.table_menu.show()
        # else:
        #     pass

    def showOrhidCalender(self):
        text=self.sender().text()
        if text   == "选择日期":
            self.dataflag=0
        elif text == "选择时间":
            self.dataflag=1
        self.calenderdata=Calender(self.x(),self.y())
        self.calenderdata.btn3.clicked.connect(self.closeorwarning)


    def closeorwarning(self):
        if QDate.fromString(self.calenderdata.box1.text(),"yyyy-MM-dd")>QDate.fromString(self.calenderdata.box2.text(),"yyyy-MM-dd") and self.calenderdata.box1.text() != "" and self.calenderdata.box2.text() != "":
            warning=QMessageBox.warning(self.calenderdata,"Warning","开始日期不能大于结束日期",QMessageBox.Yes)
        elif self.calenderdata.box1.text() == "" and self.calenderdata.box2.text() != "":
            warning = QMessageBox.warning(self.calenderdata, "Warning", "请选择开始时间", QMessageBox.Yes)
        elif self.calenderdata.box1.text() != "" and self.calenderdata.box2.text() == "":
            warning = QMessageBox.warning(self.calenderdata, "Warning", "请选择结束时间", QMessageBox.Yes)
        elif self.calenderdata.box1.text() == "" and self.calenderdata.box2.text() == "":
            warning = QMessageBox.warning(self.calenderdata, "Warning", "请选择开始和结束时间", QMessageBox.Yes)
        else:
            self.startdate=self.calenderdata.box1.text()+"T"+"00:00:00"
            self.enddate=self.calenderdata.box2.text()+"T"+"23:59:59"
            logging.debug("self.startdate：{}".format(self.startdate))
            logging.debug("self.enddate：{}".format(self.enddate))

        if self.dataflag == 1:
            # try:
            #     del self.quirelist[0]["$match"]["$StartConfigDate"]["$gt"]
            #     del self.quirelist[0]["$match"]["$StartConfigDate"]["$lt"]
            # except KeyError:
            #     pass
            try:
                self.quirelist[0]["$match"]["createTime"]["$gt"] = self.startdate
                self.quirelist[0]["$match"]["createTime"]["$lt"] = self.enddate
            except KeyError:
                self.quirelist[0]["$match"]["createTime"]        = {}
                self.quirelist[0]["$match"]["createTime"]["$gt"] = self.startdate
                self.quirelist[0]["$match"]["createTime"]["$lt"] = self.enddate

            self.statext.setText(str(self.quirelist))

        self.calenderdata.close()

    def frontandnext(self):
        sender=self.sender()
        if sender.text() == "上一页":
            if self.skip ==0:
                pass
            else:
                self.skip-=100
        elif sender.text() == "下一页":
            self.skip+=100
        ss=Mongodb_connect(querydata=self.dict,flags=1,skipnum=self.skip)
        ss.connect_mongodb()
        # ss.connect_mongodb(collection="app_upload_log")
        data = self.getdata(ss)
        self.showdata(data)


    def comboboxchoiced(self): #设置初始下拉条选择界面
        if self.combobox1.currentText() == "accountid&CID查询":
            self.box1.setEnabled(True)
            self.btn1.setEnabled(True)
            self.btn11.setEnabled(True)
            self.btn3.setEnabled(False)
            self.btn4.setVisible(False)
            self.btn5.setVisible(False)
            self.combobox2.setVisible(False)
            self.combobox3.setVisible(False)
            self.combobox4.setVisible(False)
            self.box2.setVisible(False)
            self.box3.setVisible(False)
            self.box4.setVisible(False)
            self.btn6.setVisible(False)
            self.stacomb1.setVisible(False)
            self.stacomb2.setVisible(False)
            self.stabtngetlist.setVisible(False)
            self.stabtnaddson.setVisible(False)
            self.stabtndelson.setVisible(False)
            self.selectdatatime.setVisible(False)
            self.stabtnsearch.setVisible(False)
            self.statext.setVisible(False)
            self.table.setColumnHidden(self.table.columnCount()-1,False)
        elif self.combobox1.currentText() == "组合查询":
            self.box1.setEnabled(False)
            self.btn1.setEnabled(False)
            self.btn11.setEnabled(False)
            self.btn3.setEnabled(True)
            self.btn4.setVisible(False)
            self.btn5.setVisible(False)
            self.btn6.setVisible(True)
            self.combobox2.setVisible(True)
            self.comboboxaddlist(self.combobox2)
            self.combobox3.setVisible(True)
            self.comboboxaddlist(self.combobox3)
            self.combobox4.setVisible(True)
            self.comboboxaddlist(self.combobox4)
            self.box2.setVisible(True)
            self.box2.setPlaceholderText("带-reg为模糊匹配")
            self.box3.setVisible(True)
            self.box3.setPlaceholderText("带-reg为模糊匹配")
            self.box4.setVisible(True)
            self.box4.setPlaceholderText("带-reg为模糊匹配")
            self.stacomb1.setVisible(False)
            self.stacomb2.setVisible(False)
            self.stabtngetlist.setVisible(False)
            self.stabtnaddson.setVisible(False)
            self.stabtndelson.setVisible(False)
            self.selectdatatime.setVisible(False)
            self.stabtnsearch.setVisible(False)
            self.statext.setVisible(False)
            if self.table.columnCount() != 0:
                if self.table.horizontalHeaderItem(self.table.columnCount()-1).text() == "detail":
                    self.table.setColumnHidden(self.table.columnCount()-1,True)
            # self.combinsearch()
        elif self.combobox1.currentText() == "数据统计":
            self.box1.setEnabled(False)
            self.btn1.setEnabled(False)
            self.btn11.setEnabled(False)
            self.btn3.setEnabled(False)
            self.btn4.setVisible(False)
            self.btn5.setVisible(False)
            self.combobox2.setVisible(False)
            self.combobox3.setVisible(False)
            self.combobox4.setVisible(False)
            self.box2.setVisible(False)
            self.box3.setVisible(False)
            self.box4.setVisible(False)
            self.btn6.setVisible(False)
            self.stacomb1.setVisible(True)
            self.stacomb2.setVisible(True)
            self.stabtngetlist.setVisible(True)
            self.stabtnaddson.setVisible(True)
            self.stabtndelson.setVisible(True)
            self.selectdatatime.setVisible(True)
            self.stabtnsearch.setVisible(True)
            self.statext.setVisible(True)

    def addordeletquiredata(self):
        text=self.sender().text()

        # self.stacomb2getlist = []  # 从mongodb动态获取组类列表存放，用户判断stacomb2是否手动输入
        # self.staticdata={}#用作判断数据统计的数据是要进行匹配还是进行统计，统计值为A,匹配值为B
        # self.staticlist=[]#用作数据统计添加元素，便于添加删除
        # self.quirelist = [{"$match": {}}, {"$group": {"_id": {}, "count": {"$sum": 1}}}]  # aggregate聚合列表

        if text =="添加":
            if  self.stacomb1.currentText() not in self.staticlist:
                self.staticlist.append(self.stacomb1.currentText()) #stacombo1添加到列表
            if  self.stacomb2.currentText() == "ALL":
                self.staticdata[self.stacomb1.currentText()]="A"#标记为group添加
                if  self.stacomb1.currentText() in self.staticmainbox.keys():#判断是否为已知数据
                    self.quirelist[1]["$group"]["_id"][self.stacomb1.currentText()]="$"+self.staticmainbox[self.stacomb1.currentText()]
                    # self.quirelist[3]["$sort"]["_id."+self.staticmainbox[self.stacomb1.currentText()]] = -1
                else:
                    self.quirelist[1]["$group"]["_id"][self.stacomb1.currentText()]="$"+self.stacomb1.currentText()
                    # self.quirelist[3]["$sort"]["_id."+self.stacomb1.currentText()] = -1
            else:
                self.staticdata[self.stacomb1.currentText()]="B"
                if self.stacomb1.currentText() in self.staticmainbox.keys():
                    if "regex" not in self.stacomb2.currentText():
                        self.quirelist[0]["$match"][self.staticmainbox[self.stacomb1.currentText()]]=self.stacomb2.currentText()
                    else:
                        self.quirelist[0]["$match"][self.staticmainbox[self.stacomb1.currentText()]]={"$regex":"%s"%self.stacomb2.currentText()[6:].split()[0],"$options":"i"}
                else:
                    if "regex" not in self.stacomb2.currentText():

                        self.quirelist[0]["$match"][self.stacomb1.currentText()] = self.stacomb2.currentText()
                    else:
                        self.quirelist[0]["$match"][self.stacomb1.currentText()] = {"$regex": "%s" % self.stacomb2.currentText()[6:].split()[0], "$options": "i"}

        elif text == "删除":
            try:
                if      self.staticdata[self.staticlist[-1]]=="A":
                    del self.quirelist[1]["$group"]["_id"][self.staticlist[-1]]
                    if  self.staticlist[-1] in self.quirelist[0]["$match"].keys():
                        del quirelist[0]["$match"][self.staticmainbox[self.staticlist[-1]]]
                    else:
                        pass
                elif    self.staticdata[self.staticlist[-1]] =="B":
                    del self.quirelist[0]["$match"][self.staticmainbox[self.staticlist[-1]]]
                    if  self.staticlist[-1] in self.quirelist[1]["$group"]["_id"].keys():
                        del self.quirelist[1]["$group"]["_id"][self.staticlist[-1]]
                    else:
                        pass
                else:
                    pass
                del self.staticdata[self.staticlist[-1]]
                del self.staticlist[-1]
            except IndexError:
                pass

        # print(self.quirelist)
        # print(self.staticdata)
        # print(self.staticlist)

        self.statext.setText(str(self.quirelist))



    def set_sta2combitem(self,i):
        # print(i)
        if i==0:#self.stacomb1.currentText() == "产品型号":#ConfigModule
            list = ["ALL",'WiFi_AirFryer_CS158-AF_EU', 'WiFiBT_Oven_CS130-AO', 'InwallSwitch3way', 'InwallswitchUS',
                            'OutdoorSocket15A', 'cherylInwallSwitch3way', 'WiFi_Bulb_WhiteLightBulb_US',
                            'AirPurifier131', 'WifiSmartBulb', '10AOutletUS', '10AOutletEU', 'WifiWallDimmer',
                            '15AOutletNightlight', 'WiFiBT_Scale_FatScalePlus_US', '7AOutlet',
                            'WiFi_SKA_AirFryer137_US', 'WiFi_Bulb_MulticolorBulb_US']

        elif i==1:#self.stacomb1.currentText() == "ErrCode": #"DetailInfo.Step4_DeviceReturnData.CurrentConfig.Result.err"
            list=["ALL",'0','51','52','53','54','55','56', '58','60','62','63','65']
        elif i==2:#self.stacomb1.currentText() == "APP版本":#AppVersion
            list=["ALL",'VeSync 2.9.35', 'VeSync 2.6.5', 'VeSync 2.7.4', 'VeSync V2.3.5 build5', 'VeSync V2.2.8 build18', 'VeSync 2.9.6', 'VeSync V2.4.8 build2', 'VeSync V2.2.5 build20', 'VeSync 2.7.6', 'VeSync 2.8.5', 'VeSync V2.4.4 build4', '2.4.0', 'VeSync 2.9.2', 'VeSync 2.6.1', 'VeSync 2.9.17', 'VeSync V2.4.1 build1', 'VeSync V2.5.0 build1', 'VeSync 2.6.3', 'VeSync 2.7.2', 'VeSync 2.8.4', '2.4.7', 'VeSync 2.9.4', 'VeSync 2.9.20', 'VeSync 2.9.30', 'VeSync 2.9.16', None, '2.4.5', 'VeSync V2.3.3 build50', '2.6.0', 'VeSync 2.9.28', 'VeSync V2.3.4 build1', 'VeSync 2.9.32（build 2）', 'VeSync 2.9.14', 'VeSync 2.9.15', 'VeSync V2.3.9 build1', 'VeSync 2.9.12', 'VeSync 2.8.0', 'VeSync 2.8.6', 'VeSync 2.8.7', 'VeSync 2.7.0', 'VeSync 2.9.13', '2.3.3', 'VeSync 2.9.8', 'VeSync 2.8.2', '2.5.0', 'VeSync 2.9.25', 'VeSync 2.9.5', 'VeSync 2.9.3', 'VeSync 2.9.9', 'VeSync 2.9.19', 'VeSync 2.9.22', 'VeSync V2.5.1 build1', '2.3.8', 'VeSync 2.6.7', 'VeSync 2.9.11', 'VeSync 2.7.8', 'VeSync 2.7.5', 'VeSync V2.5.3 build1', 'VeSync 2.9.26', 'VeSync 2.9.27', 'VeSync V2.4.2 build2', 'VeSync 2.9.23', 'VeSync 2.9.1', 'VeSync 2.9.29(build3)', 'VeSync V2.3.8 build1', '2.3.2', 'VeSync 2.9.0', 'VeSync 2.8.1', 'VeSync 2.9.21', '2.3.7', 'VeSync V2.4.7 build2', '2.3.6', 'VeSync V2.2.1 build1', '2.2.3', 'VeSync V2.6.0 build4', 'VeSync 2.8.9', 'VeSync 2.9.34 build1', 'VeSync 2.9.10', '2.4.1', 'VeSync 2.8.8', 'VeSync 2.7.9', '2.4.8', 'VeSync 2.9.29', 'VeSync 2.6.4', 'VeSync 2.6.6', 'VeSync 2.9.31 build7', '2.5.1', 'VeSync 2.7.3', 'VeSync 2.9.7', '2.5.3', 'VeSync 2.9.31', 'VeSync V2.4.0 build2', 'VeSync 2.6.2', 'VeSync 2.9.32', 'VeSync V2.4.5 build1', 'VeSync 2.7.7', 'VeSync 2.9.33', 'VeSync V2.3.0 build25']
        elif i==3:#self.stacomb1.currentText() == "OSVersion":#OSVersion
            list=["ALL",'10.3.1', '13.4.1', '11.0', 'Android 4.4.4', '11.0.1', '9.3.6', '11.0.3', '10.3.4', 'Android R', '11.3', '11.2.1', '11.2.5', 'Android 4.3', '10.3.2', '14.0', '12.1.3', '11.1.2', '10.3.3', '12.3.1', '12.2', 'Android 5.1', 'Android 6.0', '12.1.2', '13.4', '13.2.3', '13.4.5', '12.4.1', '11.4', 'Android 7.1.1', 'Android 8.0.0', 'Android 6.0.1', '12.4.2', 'Android 7.0', '13.2.2', 'Android 10', '12.4.5', 'Android 9', '13.3.1', None, 'Android 8.1.0', '12.3.2', '13.1.2', '12.1.1', '13.1.3', '12.4', '11.2.2', '9.3.5', '12.4.4', '12.1.4', '13.1', 'Android 4.4.2', '11.4.1', '12.4.6', 'Android 7.1.2', '9.2', '13.2', 'Android 5.0.1', '9.3.2', '12.3', '13.3', '12.0.1', 'Android 5.0.2', 'Android 5.1.1', '11.3.1', '12.4.3', '12.0', 'Android 5.0', '13.1.1', '13.0', '11.2.6', '12.1']
        elif i==4:#self.stacomb1.currentText() == "配网结果":#Result
            list=["ALL",'Success', 'Failure']
        elif i==5:#self.stacomb1.currentText() == "SSID":#DetailInfo.Step3_ConfigInfo.wifiSSID
            list=["ALL"]
        elif i==6:#self.stacomb1.currentText() == "手机型号":#MobileType
            list=["ALL"]
        elif i == 7:
            list=["ALL"]
        self.stacomb2.clear()
        self.stacomb2.addItems(list)
    def get_sta2combitembyconnectmongo(self):
        list=["ConfigModule","DetailInfo.Step4_DeviceReturnData.CurrentConfig.Result.err","AppVersion","OSVersion","Result","DetailInfo.Step3_ConfigInfo.wifiSSID","MobileType","UserID"]
        index=self.stacomb1.currentIndex()
        if index != 5 and index!=7:
            s=Mongodb_connect(flags=2)
            s.connect_mongodb(list[index])
            self.stacomb2getlist=s.get_list()[:]
            self.stacomb2.clear()
            self.stacomb2.addItems(self.stacomb2getlist)
        else:
            pass
    def queryroutermacAndIPlocation(self):
        if self.btn2.text() == "显示IPlocation&路由器厂商":
            location = ["Iplocation"]
            routermacVender= ["routermacVender"]
            ip=self.uplog.get_ip()
            # print(ip)
            routermac= self.uplog.get_routerMac()
            s=[]
            k=[]
            for x in range(1,len(ip)):
                if ip[x] != "":
                    if ip[x] not in s:
                        s.append(ip[x])
                        req=FromIpgetLocation(ip[x])
                        location.append(req.getlocation())
                    else:
                        location.append("")
                else:
                    location.append("")
            for x in range(1,len(routermac)):
                if routermac[x] != "" and routermac[x] != "ff:ff:ff:ff:ff:ff":
                    if routermac[x] not in s:
                        s.append(routermac[x])
                        req=FromRouterGetVender(routermac[x])
                        routermacVender.append(req.getroutermacVender())
                    else:
                        routermacVender.append("")
                else:
                    routermacVender.append("")
            self.addColumn(routermacVender,8)
            self.addColumn(location,12)
            self.btn2.setText("隐藏IPlocation&路由器厂商")

        elif self.btn2.text() == "隐藏IPlocation&路由器厂商":
            self.table.removeColumn(8)
            self.table.removeColumn(11)
            self.btn2.setText("显示IPlocation&路由器厂商")
    def combinesearch(self):
        self.skip=0
        self.dict={}
        comtext2=self.combobox2.currentText()
        comtext3=self.combobox3.currentText()
        comtext4=self.combobox4.currentText()
        boxtext2=self.box2.text()
        boxtext3=self.box3.text()
        boxtext4=self.box4.text()
        if boxtext2 !="":
            self.dict=self.comboxtransfomtosearch(comtext2,boxtext2,self.dict)

        if boxtext3 != "":
            self.dict=self.comboxtransfomtosearch(comtext3,boxtext3,self.dict)
        if boxtext4 != "":
            self.dict=self.comboxtransfomtosearch(comtext4,boxtext4,self.dict)
        if self.startdate != "" and self.enddate !="":
            # try:
            self.dict["createTime"]={"$gt":self.startdate,"$lt":self.enddate}
        # except NameError:
            #     pass

        # print(self.dict)
        print(self.dict)
        self.uplog = Mongodb_connect(querydata=self.dict,flags=1)
        self.uplog.connect_mongodb()
        # self.uplog.connect_mongodb(collection="app_upload_log")
        data = self.getdata(self.uplog)
        self.showdata(data)
        self.btn4.setVisible(True)
        self.btn5.setVisible(True)

    def comboxtransfomtosearch(self,combox,boxtext,dict):
        boxtext = r"{}".format(boxtext)
        if combox == "errCode":
            dict["DetailInfo.Step4_DeviceReturnData.CurrentConfig.Result.err"] = boxtext
            return dict

        elif combox == "SSID-reg":
            dict["$or"]=[{"DetailInfo.Step3_ConfigInfo.wifiSSID":{"$regex":'{}'.format(boxtext),"$options":'i'}},{"DetailInfo.Step3_ConfigInfo.wifiID":{"$regex":'{}'.format(boxtext),"$options":'i'}}]
            return dict

        elif combox == "ConfigModule":
            dict["ConfigModule"]=boxtext
            return dict

        elif combox == "AppVersion":
            dict["AppVersion"] = boxtext

            return dict

        elif combox == "Result":
            dict["Result"] = boxtext
            return dict

        elif combox == "OSVersion-reg":
            dict["OSVersion"] = {"$regex":'{}'.format(boxtext),"$options":'i'}
            return dict

        elif combox == "AccountEmail-reg":
            dict["AccountEmail"]={"$regex":'{}'.format(boxtext),"$options":'i'}
            return dict

        elif combox == "IsVpn":
            if boxtext == "true" or boxtext == "True":
                dict["IsVpn"] = {"$eq":True}
            elif boxtext == "false" or boxtext == "False":
                dict["IsVpn"] = {"$eq": False}
            return dict

        elif combox == "FirmVersion-reg":
            dict["FirmVersion"] = {"$regex": '{}'.format(boxtext), "$options": 'i'}
            return dict
        elif combox == "ishandle":
            if boxtext =="true" or boxtext =="True":
                dict["DetailInfo.Step3_ConfigInfo.isManualInput"] = {"$eq":True}
            elif boxtext =="false" or boxtext =="False":
                dict["DetailInfo.Step3_ConfigInfo.isManualInput"] = {"$eq": False}
            return dict

        elif combox == "desc":
            pass



    def comboboxaddlist(self,combox):
        list=["errCode","SSID-reg","ConfigModule","AppVersion","Result","OSVersion-reg","AccountEmail-reg","IsVpn","FirmVersion","desc","ishandle"]
        combox.addItems(list)

    def addColumn(self,data,colum):
        self.table.insertColumn(colum)
        self.table.setHorizontalHeaderItem(colum,QTableWidgetItem(data[0]))
        for s in range(1,len(data)):
            self.table.setItem(s-1,colum,QTableWidgetItem(str(data[s])))

    def resizeEvent(self, QResizeEvent):
        self.table.resize(self.width(), self.height() - 100)

    def accurateAccountorCid(self):
        text=self.box1.text()
        self.btn2.setEnabled(True)
        if len(text)>=15 and not re.search(r"[0-9]{7}",text):
            self._fromCidreqdata(text.split()[0])
        elif len(text) == 0:
            pass
        else:
            self._fromaccountreqdata(text.split()[0])


    def _fromaccountreqdata(self,text):
        sender_text = self.sender().text()
        self.uplog=Mongodb_connect(UserID=text)
        self.uplog.connect_mongodb()
        if sender_text == "查询所有":
            self.uplog.connect_mongodb(collection="app_upload_log")
        data=self.getdata(self.uplog)
        logging.info("had get all mongo data......")
        self.showdata(data)

    def _fromCidreqdata(self,text):
        sender_text=self.sender().text()
        self.uplog=Mongodb_connect(CID=text)
        self.uplog.connect_mongodb()
        if sender_text == "查询所有":
            self.uplog.connect_mongodb(collection="app_upload_log")
        data=self.getdata(self.uplog)
        self.showdata(data)

    def show_detailinfo(self):
        detail = self.uplog.get_detail()[self.table.currentRow()+1]
        detail=JSONEncoder().encode(detail)
        detail=json.loads(detail)
        self.textwindow.setText(json.dumps(detail,indent=5,ensure_ascii=False))
        self.textwindow.setVisible(True)
    def sava_as_json(self):
        folder=os.path.exists("D:/kibanalog_downloads/")
        if folder:
            pass
        else:
            try:
                os.makedirs("D:/kibanalog_downloads/")
            except:
                folder = os.path.exists("D:\\kibanalog_downloads\\")
                if folder:
                    pass
                else:
                    os.makedirs("D:\\kibanalog_downloads\\")
        filename="{}".format(datetime.datetime.now().strftime("%H-%M-%S")) + ".txt"
        save_message=QMessageBox(self)
        save_message.information(self,"save infomation","文件会保存在D:/kibanalog_downloads/"+filename,QMessageBox.Yes)
        file=open("D:/kibanalog_downloads/" + filename,"a")
        detail=self.uplog.get_detail()
        for k in detail:
            data = JSONEncoder().encode(k)
            data = json.loads(data)
            data=json.dumps(data, indent=5, ensure_ascii=False)
            file.write(data+"\n")
        file.close()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            if self.table.isVisible():
                self.textwindow.setVisible(False)
            else:
                pass
        elif QKeyEvent.key() == Qt.Key_F2:#为查看detail信息设置快捷键
            try:
                if self.table.currentRow() >= 0: #判断是否选中self.table单位
                    self.show_detailinfo()
                else:
                    pass
            except:
                pass
        else:
            pass
    def showdata(self,alldata):
        self.table.setRowCount(len(alldata[0]) - 1)
        self.table.setColumnCount(len(alldata))
        for i in range(0, len(alldata)):  # 总列数,显示所有数据
            for j in range(1, len(alldata[0])):  # 总数据行数
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(alldata[i][0]))
                ss = QTableWidgetItem(alldata[i][j])
                self.table.setItem(j - 1, i, ss)
                ss.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置所有单元格对齐方式
        # if self.table.horizontalHeaderItem(self.table.columnCount() - 1).text() == "detail":
        #     for k in range(1,len(alldata[0])):
        #         kk=locals()["Btn"+"%d"%k]=QPushButton("显示详情"+"%d"%k,self)
        #         self.table.setCellWidget(k-1,len(alldata)-1,kk)
        #         kk.clicked.connect(self.show_detailinfo)
            self.setcloumnwidth()
        # self.hiderows(flags=flags)
        # self.table.cellClicked.connect(self.highlightDifferentAddData)

    def setcloumnwidth(self):
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 30)
        # self.table.setColumnWidth(7, 80)
        # self.table.setColumnWidth(8, 80)
        self.table.setColumnWidth(7, 80)
        self.table.setColumnWidth(8, 250)
        self.table.setColumnWidth(9, 120)

    def getdata(self,uplog):
        data=[]
        detail=["detail"]
        data.append(uplog.get_userid())
        data.append(uplog.get_StartConfigDate())
        data.append(uplog.get_ConfigModule())
        data.append(uplog.get_Result())
        data.append(uplog.get_AppVersion())
        data.append(uplog.get_OSVersion())
        data.append(uplog.get_errCode())
        # data.append(uplog.get_phonerssi())
        # data.append(uplog.get_phoneDeviceRssi())
        data.append(uplog.get_deviecrssi())
        data.append(uplog.get_cid())
        data.append(uplog.get_FirmVersion())
        data.append(uplog.get_routerMac())
        data.append(uplog.get_WifiCount())
        data.append(uplog.get_SSID())
        data.append(uplog.get_ip())
        data.append(uplog.get_AccountEmail())
        data.append(uplog.get_PassWord())
        data.append(uplog.get_transform_Text())
        data.append(uplog.get_ishandle())
        data.append(uplog.get_IsVpn())
        data.append(uplog.get_desc())
        # if self.combobox1.currentText() == "accountid&CID查询":
        #     for s in range(len(uplog.get_userid())-1):
        #         detail.append("")
        #     data.append(detail)
        return data

class JSONEncoder(json.JSONEncoder):
    """处理ObjectId,该类型无法转为json"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)

class Calender(QWidget):
    def __init__(self,x,y):
        super().__init__()
        self.x=x
        self.y=y
        self.StartDate = ""
        self.EndDate = ""
        self.initUi()

    def initUi(self):
        self.setWindowTitle("日期选择")
        self.setWindowIcon(QIcon("kibana.png"))
        self.setGeometry(self.x+600,self.y+150,300,400)
        self.setWindowOpacity(1)
        self.calender=QCalendarWidget(self)
        self.calender.resize(300,200)
        self.calender.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.btn1=QPushButton("开始时间",self)
        self.btn1.clicked.connect(self.getstartorenddata)
        self.btn2 = QPushButton("结束时间",self)
        self.btn2.clicked.connect(self.getstartorenddata)
        self.btn3 = QPushButton("确定",self)
        # self.btn3.clicked.connect(self.closeorwarning)
        # self.btn3.clicked.connect()
        self.box1=QLabel(self)
        self.box2=QLabel(self)
        self.Gride=QGridLayout(self)
        self.Gride.addWidget(self.calender,0,0,6,4)
        self.Gride.addWidget(self.btn1,6,0,1,1)
        self.Gride.addWidget(self.box1, 6, 1, 1, 1)
        self.Gride.addWidget(self.btn2, 6, 2, 1, 1)
        self.Gride.addWidget(self.box2, 6, 3, 1, 1)
        self.Gride.addWidget(self.btn3,7, 3, 1, 1)

        self.show()

    def getstartorenddata(self):
        self.text=self. sender()
        self.calender.clicked.connect(self.showdata)

    def showdata(self):
        if self.text.text() == "开始时间":
            self.box1.setText(self.calender.selectedDate().toString("yyyy-MM-dd"))
        elif self.text.text() == "结束时间":
            self.box2.setText(self.calender.selectedDate().toString("yyyy-MM-dd"))
    # def closeorwarning(self):
    #     if QDate.fromString(self.box1.text(),"yyyy-MM-dd")>=QDate.fromString(self.box2.text(),"yyyy-MM-dd") and self.box1.text() != "" and self.box2.text() != "":
    #         warning=QMessageBox.warning(self,"Warning","开始日期不能大于结束日期",QMessageBox.Yes)
    #     elif self.box1.text() == "" and self.box2.text() != "":
    #         warning = QMessageBox.warning(self, "Warning", "请选择开始时间", QMessageBox.Yes)
    #     elif self.box1.text() != "" and self.box2.text() == "":
    #         warning = QMessageBox.warning(self, "Warning", "请选择结束时间", QMessageBox.Yes)
    #     elif self.box1.text() == "" and self.box2.text() == "":
    #         warning = QMessageBox.warning(self, "Warning", "请选择开始和结束时间", QMessageBox.Yes)
    #     else:
    #         self.StartDate=self.box1.text()
    #         self.EndDate=self.box2.text()
    #         print(self.StartDate)
    #         print(self.EndDate)
    #
    #         self.close()


