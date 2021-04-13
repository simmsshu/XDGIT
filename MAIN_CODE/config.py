from PyQt5.QtWidgets import QMainWindow,QWidget,QApplication,QMenuBar,QMenu,QLabel,QLineEdit,QPushButton,QComboBox,QGridLayout,\
    QHBoxLayout,QVBoxLayout,QTextEdit,QToolBar,QMessageBox,QTableWidget,QTableWidgetItem,QAction,QHeaderView,QAbstractItemView,\
    QFrame,QScrollBar,QSizePolicy,QStyleOption, QStyle
from PyQt5.QtGui import QIcon,QCursor,QMovie,QResizeEvent,QPainter
from PyQt5.QtCore import Qt,QThread,pyqtSignal,QSize
from PyQt5.Qt import QFont
import sys,os,json,re,time,threading,logging
from elasticsearch import Elasticsearch
from datetime import datetime,timedelta
from BASE_ABOUT.needClass import *
from copy import deepcopy
import threading
import time
logging.basicConfig(level=logging.INFO)
class Rwfile():
    def __init__(self):
        self.filename = "./cfg.json"

    def writeToFile(self,text):
        t=0
        f=open(self.filename,"w",encoding="utf-8")
        data = json.dumps(text, indent=5,ensure_ascii=False)
        f.write(data)
        f.close()

    def readFile_with_eval(self):
        try:
            f=open(self.filename,"r",encoding="utf-8")
            # s=eval(f.read())
            s=json.load(fp=f)
            f.close()
        except Exception as e:
            print(e)
            return {}
        return s


class defineWindow(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        if parent:
            self.setParent(parent)
        self.list = []
        readconfig = Rwfile()
        self.configdict = readconfig.readFile_with_eval()
        self.configMainWindow()

    def configMainWindow(self):
        self.setWindowTitle("自建查询")
        self.setWindowIcon(QIcon("./pic/Kibana.png"))
        self.setGeometry(100,100,900,800)
        # self.bt11=s1.addAction("新建")
        self.bt11 = QPushButton("新建查询",self)
        self.bt11.clicked.connect(self.creatprojectWindow)

        self.mainLable1=QLabel("输入关键字查询索引",self)
        self.searchbox1=QLineEdit(self)
        self.searchbox1.textChanged.connect(self.searchWidget)
        self.indexbtn=QPushButton("index工具",self)
        self.indexbtn.clicked.connect(self.loadindextool)
        self.combox1=QComboBox(self)
        self.combox1.addItems(["cloud-wifioutlet7a","cloud-mqtt","cloud-appserver-new","cloud-alexacontrolproxy","综合"])
        self.combox1.setCurrentIndex(4)
        self.combox1.currentTextChanged.connect(self.getCurrentComboxSearchIndex)
        # self.confirmbtn=QPushButton("确认",self)
        # 主布局
        main_layout=QVBoxLayout(spacing=0)
        top_widget=QWidget(self)
        top_layout=QHBoxLayout()
        # self.top_widget.setSpacing(0)
        top_widget.setLayout(top_layout)
        middle_widget=QWidget(self)
        self.middle_layout=QGridLayout()
        # self.middle_layout.setSpacing(5)
        middle_widget.setLayout(self.middle_layout)
        top_layout.addWidget(self.bt11)
        top_layout.addWidget(self.combox1)
        top_layout.addWidget(self.mainLable1)
        top_layout.addWidget(self.searchbox1)
        top_layout.addWidget(self.indexbtn)

        main_layout.addWidget(top_widget,30)
        main_layout.addWidget(middle_widget,770)
        # self.widget = QWidget(self)
        # self.widget.setStyleSheet('''QPushButton{border-radius:3px;border:solid;}''')
        self.setLayout(main_layout)
        keylist = self.getkeylist(self.configdict)
        self.addButtomWithKey(keylist)


        self.show()

    def addButtomWithKey(self,keylist):
        self.btnlist=[]
        font = QFont()
        font.setFamily("宋体")
        font.setPointSize(8)
        button_Adaptive = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        for j in range(len(keylist)):
            self.btnlist.append(j)
            self.btnlist[j]=QPushButton(self)
            self.btnlist[j].setStyleSheet("QPushButton{border-radius:5px;background-color:white;border:1px solid;}"
                                     "QPushButton:hover{background-color:gray;}")
            #设置最大最小尺寸，避免设置圆角后大小改变
            self.btnlist[j].setMinimumSize(QSize(0, 0))
            self.btnlist[j].setMaximumSize(QSize(200, 20))

            self.btnlist[j].setFont(font)
            self.btnlist[j].setText(keylist[j])
            self.btnlist[j].setSizePolicy(button_Adaptive)
            self.btnlist[j].setToolTip(keylist[j])
            self.btnlist[j].clicked.connect(self.btnclick)
        self.setlbtnlayout()


    def setlbtnlayout(self):
        width = 0
        height = 0
        for btn in self.btnlist:
            logging.debug(f"width,btnwidth,self.width:{width},{btn.width()},{self.width()}")
            if (width + btn.width()) < self.width():
                pass
            else:
                width = 0
                height += 1
            self.middle_layout.addWidget(btn, height, width, 1, btn.width())
            width += btn.width()
        if height <= 19:
            self.middle_layout.addWidget(QFrame(self), height + 1, 0, 20 - height - 1, self.width())

    def searchWidget(self):
        self.clearMiddle_layout_widget()
        text=self.searchbox1.text()
        items=self.getkeylist(self.configdict)
        searchresultlist=[]
        for a in items:
            if text in a:
                searchresultlist.append(a)
        self.addButtomWithKey(searchresultlist)

    def btnclick(self):
        sender=self.sender()
        self.list.append(InquiryPage(sender.text(),self.configdict))

    def getCurrentComboxSearchIndex(self):
        self.clearMiddle_layout_widget()
        text=self.combox1.currentText()
        keylist=self.getkeylist(self.configdict)
        needindex=[]
        if text != "综合":
            for a in keylist:
                if text == self.configdict[a]["index"]:
                    needindex.append(a)
            self.addButtomWithKey(needindex)
        else:
            self.addButtomWithKey(keylist)

    def clearMiddle_layout_widget(self):
        for i in range(self.middle_layout.count()):
            self.middle_layout.itemAt(i).widget().deleteLater()

    def getkeylist(self,dictdata):
        list1=[]
        for s in  dictdata.keys():
            list1.append(s)
        return list1



        self.show()
    def creatprojectWindow(self):
        self.secondwindow=ConfigWindow()

    def loadindextool(self):
        self.list.append(Transform())


class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = Rwfile()
        self.configdict = self.config.readFile_with_eval()
        self.configWindow()



    def configWindow(self):
        self.setGeometry(200,200,800,600)
        self.setWindowTitle("新建查询条目")
        self.setWindowIcon(QIcon("./pic/Kibana.png"))
        self.lab1=QLabel("请输入查询名称",self)
        self.lab2=QLabel("请选择ELK索引",self)
        self.lab3=QLabel("请输入查询body",self)
        self.lab4=QLabel("选择每页显示数量",self)
        self.lab5=QLabel("排序字段",self)
        self.linedit1=QLineEdit(self)
        self.linedit1.setPlaceholderText("为查询索引取名")

        self.combox1=QComboBox()
        self.combox1.addItems(["cloud-wifioutlet7a","cloud-mqtt","cloud-appserver-new","cloud-alexacontrolproxy"])
        self.combox1.setToolTip("可手动输入，在ELK日志 index内寻找，取-日期前部分")
        self.combox1.setEditable(True)

        self.context1=QTextEdit(self)
        self.context1.setPlaceholderText("请在此输入查询体内容，如\n{\n\t\"query\":{\"match_all\":[]}}")
        self.linedit2=QLineEdit("500",self)
        self.linedit5=QLineEdit("@timestamp",self)
        # self.linedit2.setPlaceholderText("500")
        self.showconifg=QPushButton("前往显示配置页面",self)
        self.showconifg.clicked.connect(self.showingConfigEvent)
        self.boxlayout=QGridLayout(self)
        self.boxlayout.addWidget(self.lab1, 0, 0, 1, 30)
        self.boxlayout.addWidget(self.linedit1, 0, 30, 1, 30)
        self.boxlayout.addWidget(self.lab2, 1, 0, 1, 30)
        self.boxlayout.addWidget(self.combox1, 1, 30, 1, 30)
        self.boxlayout.addWidget(self.lab3, 0, 60, 1, 200,Qt.AlignHCenter)
        self.boxlayout.addWidget(self.context1, 1, 60, 6, 200)
        self.boxlayout.addWidget(self.lab4, 2, 0, 1, 30)
        self.boxlayout.addWidget(self.linedit2, 2, 30, 1, 30)
        self.boxlayout.addWidget(self.lab5,3,0,1,30)
        self.boxlayout.addWidget(self.linedit5,3,30,1,30)
        self.boxlayout.addWidget(self.showconifg, 7, 200, 1, 30)
        self.boxlayout.setSpacing(5)
        self.setLayout(self.boxlayout)



        self.show()
    def showingConfigEvent(self):
        if self.linedit1.text() not in self.configdict.keys():
            pass
        else:
            self.showtips("该查询名称已存在,请更换")
            return
        try:
            if int(self.linedit2.text())>1000:
                self.showtips("查询返回不可超过1000")
                return
            else:
                pass
        except Exception as s:
            print(s)
            self.showtips("请输入整数")
            return

        try:
            self.quirebody=eval(self.context1.toPlainText())
        except Exception as bodyerr:
            self.showtips(str(bodyerr))
            return
        # self.configdict[self.linedit1] = {}
        self.configdict[self.linedit1.text()] = {}
        self.configdict[self.linedit1.text()]["index"] = self.combox1.currentText()
        self.configdict[self.linedit1.text()]["body"]   =   {"query":{
                                                                "bool":{
                                                                    "must":[]
                                                                }
                                                            }}
        self.configdict[self.linedit1.text()]["body"]["query"]["bool"]["must"].append(self.quirebody["query"])
        self.configdict[self.linedit1.text()]["body"]["size"] = int(self.linedit2.text())
        self.configdict[self.linedit1.text()]["body"]["from"] = 0
        # if self.combox1.currentText() == "cloud-appserver":
        self.configdict[self.linedit1.text()]["body"]["sort"] = {self.linedit5.text(): {"order": "desc"}}
        # else:
        #     self.configdict[self.linedit1.text()]["body"]["sort"] = {"T": {"order": "desc"}}
        # print(self.configdict)
        self.goSearchAndShowconfig=SearchAndShowconfig(self.configdict,self.linedit1.text())
        # print(self.configdict)
        self.goSearchAndShowconfig.showWindow()

    def showtips(self,tips):
        QMessageBox.warning(self,"Tips",tips,QMessageBox.Yes)



class SearchAndShowconfig(QWidget):
    def __init__(self,configdict,queryName):
        super().__init__()
        self.configdict = configdict
        # 需要的字典数据
        self.queryName = queryName
        # 需要数据所在字典的键值
        self.sort = UsefulMethod.getsignaldictkey(self.configdict[self.queryName]["body"],"sort")
        #储存单列对应多个索引的列表
        self.line_many_index_list = []




    def showWindow(self):
        self.configdict[self.queryName]["globalvars"] = []
        self.response = dict()
        self.sonDictIndex = []
        # 存储combox22数据
        self.sonDictData = []
        # 存储转换过的所有数据
        self.indexlist = []
        # 储存返回一天日志的所有键值

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("配置查询和显示规则")
        self.setWindowIcon(QIcon("./pic/Kibana.png"))
        self.lab1=QLabel("输入测试查询条件",self)
        self.linetext1=QLineEdit(self)
        self.linetext1.setPlaceholderText("该处输入全局查找条件")
        self.linetext2=QLineEdit()
        self.btn1=QPushButton("获取数据",self)
        self.btn1.setToolTip("直接获取最近一天所有记录的key值，不用输入查询条件")
        self.btn1.clicked.connect(self.getAllIndex)
        self.btn2=QPushButton("添加查询条件")
        self.btn2.setToolTip("添加该项会保存到配置文件中,尽量不使用该条件")
        self.btn2.clicked.connect(self.showOrHiddeSearchCondition)
        self.btn3=QPushButton("保存",self)
        self.btn3.clicked.connect(self.savaConfigFile)
        self.btn4=QPushButton("test")
        self.combox1=QComboBox(self)
        self.combox1.setEditable(True)
        self.combox2=QComboBox(self)
        # self.combox2.setEditable(True)
        self.combox2.addItems(["is","not","is one of"])
        self.linetext3=QLineEdit(self)
        self.linetext3.setPlaceholderText("输入查询条件")

        self.combox1.setHidden(True)
        self.combox2.setHidden(True)
        self.linetext3.setHidden(True)
        self.btn4.setHidden(True)


        self.combox11=QComboBox(self)
        self.combox11.setEditable(True)
        self.combox11.setMaxVisibleItems(50)
        # self.combox11.addItem("")
        self.combox11.currentTextChanged.connect(self.showIndexDataType)
        self.btn10=QPushButton("Add to list",self)
        self.btn10.setToolTip("将该索引添加到列表后一个列按照列表索引依次取值，若不为空则则返回值")
        self.btn10.clicked.connect(self.add_del_key_clicked)
        self.btn101 = QPushButton("DEL")
        self.btn101.setToolTip("删除列表最后一个索引")
        self.btn101.clicked.connect(self.add_del_key_clicked)
        self.linetext12=QLineEdit(self)
        self.linetext12.setPlaceholderText("请输入列名")
        self.btn11=QPushButton("test",self)
        # self.btn11.setEnabled(False)
        self.btn11.clicked.connect(self.showMainDictData)

        self.linetextnext1 = QLineEdit(self)
        #设置文本框不可编辑
        self.linetextnext1.setFocusPolicy(Qt.NoFocus)
        self.linetextnext1.setHidden(True)

        self.lab21 = QLabel("选择转换类型",self)
        self.combox21 = QComboBox(self)
        self.combox21.addItems(["不转换","使用正则"])
        self.combox21.currentTextChanged.connect(self.transformToDictOrRegex)
        self.lab22 = QLabel("输入正则表达式",self)
        self.combox22=QComboBox(self)
        self.combox22.setEditable(True)
        self.linetext21=QLineEdit(self)
        self.linetext21.setPlaceholderText("如SENDclient\[(.*?)\],可参考python re模块")
        self.table21=QTableWidget(self)
        self.table21.setRowCount(self.configdict[self.queryName]["body"]["size"])
        self.table21.setColumnCount(30)
        self.table21.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table21.setWordWrap(False)
        self.table21.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置启用右键模式
        ##设置鼠标跟踪以及鼠标进入单元格触发事件
        # self.table21.setMouseTracking(True)
        # self.table21.cellEntered.connect(self.tableHeaderTip)
        self.table21.cellDoubleClicked.connect(self.tableContentText)
        self.table21.customContextMenuRequested.connect(self.tablerightmenushow)
        self.table21.setStyleSheet("QTableWidget.item{border:1px solid ;}")
        self.btn21=QPushButton("test",self)
        self.btn21.setEnabled(False)
        self.btn21.clicked.connect(self.transformToDictOrRegexBtn)

        self.mainlayout=QGridLayout(self)
        self.mainlayout.setSpacing(0)
        self.toplayout=QHBoxLayout()
        self.middlelayout=QGridLayout()
        self.topwidget=QWidget(self)
        self.topwidget.setLayout(self.toplayout)
        self.middlewidget=QWidget(self)
        self.middlewidget.setLayout(self.middlelayout)

        self.toplayout.addWidget(self.lab1,Qt.AlignTop)
        self.toplayout.addWidget(self.linetext1, Qt.AlignTop)
        self.toplayout.addWidget(self.btn1, Qt.AlignTop)
        self.toplayout.addWidget(self.btn2, Qt.AlignTop)
        self.toplayout.addWidget(self.btn3, Qt.AlignTop)

        self.middlelayout.addWidget(self.combox1,0,0,1,5)
        self.middlelayout.addWidget(self.combox2,0,5,1,2)
        self.middlelayout.addWidget(self.linetext3, 0, 7, 1, 2)
        self.middlelayout.addWidget(self.btn4,0,9,1,1)
        self.middlelayout.addWidget(self.combox11,1,0,1,5)
        self.middlelayout.addWidget(self.btn10,1,5,1,1)
        self.middlelayout.addWidget(self.btn101,1,6,1,1)
        self.middlelayout.addWidget(self.linetext12,1,7,1,2)
        self.middlelayout.addWidget(self.btn11,1,9,1,1)
        self.middlelayout.addWidget(self.linetextnext1,2,0,1,10)
        self.middlelayout.addWidget(self.lab21,3,0,1,1)
        self.middlelayout.addWidget(self.combox21,3,1,1,1)
        self.middlelayout.addWidget(self.combox22,3,2,1,4)
        self.middlelayout.addWidget(self.lab22,3,6,1,1)
        self.middlelayout.addWidget(self.linetext21,3,7,1,2)
        self.middlelayout.addWidget(self.btn21, 3, 9, 1, 1)
        self.middlelayout.addWidget(self.table21,4,0,15,10)

        self.mainlayout.addWidget(self.topwidget,0,0,1,7,Qt.AlignTop)
        self.mainlayout.addWidget(self.middlewidget,1,0,40,7)


        self.show()
    def transformToDictOrRegexBtn(self):
        key=[]
        for a in self.configdict[self.queryName]["querylist"]:
            for s in a.keys():
                key.append(s)
        if self.linetext12.text() != "" and self.linetext12.text() not in key:

            if len(self.line_many_index_list) != 0:
                sourcedata = self.line_many_index_list
            else:
                sourcedata = self.combox11.currentText()
            if self.combox21.currentText() == "使用正则":
                self.configdict[self.queryName]["querylist"].append(
                    {self.linetext12.text(): {"mainkey": sourcedata, "transformtidict":False,"useregex": True,"regex":self.linetext21.text()}})
                self.table21.setHorizontalHeaderItem(len(self.configdict[self.queryName]["querylist"]) - 1,
                                                     QTableWidgetItem(self.linetext12.text()))
                c = 0
                for s in self.response["hits"]["hits"]:
                    data = self.get_data_by_index_from_list(s["_source"], sourcedata)
                    data0 = self.getRegexdata(str(data),self.linetext21.text())
                    k = QTableWidgetItem(str(data0))
                    self.table21.setItem(c, len(self.configdict[self.queryName]["querylist"]) - 1, k)
                    c += 1

            else:
                pass

        elif self.linetext12.text() == "":
            self.quirefilterWarning("请输入列名")
        elif self.linetext12.text() in key:
            self.quirefilterWarning("列名"+"{}".format(self.linetext12.text())+"已存在，请更换")
        else:
            pass
        self.line_many_index_list.clear()
        self.linetextnext1.clear()
        self.linetextnext1.setHidden(True)

    def getRegexdata(self,sourcedata,regexdata,flag=0):

        # if flag == 0:
        #     if '"' in regexdata:
        #         regexdata=regexdata.replace('"',"'")
        #     else:
        #         pass
        # elif flag == 1:
        #     pass
        logging.debug("getRegexdata-sourcedata,regexdata:{},{}".format(sourcedata, regexdata))
        if  regexdata.startswith("(") and regexdata.endswith(")"):
            #这里传入的regexdata需要是"(re.compile(r正则))"
            try:
                rex = eval(regexdata)
                for s in rex:
                    result = s.search(sourcedata)
                    if result:
                        try:
                            return result.group(1)
                        except:
                            return result.group(0)
                return ""
            except:
                return ""
        else:
            if "\\" in regexdata:
                regexdata = regexdata.replace("\\", "\\\\")
            pat1=re.compile(r"{}".format(regexdata))
            result=pat1.search(sourcedata)
            if result:
                try:
                    return result.group(1)
                except:
                    return result.group(0)
            else:
                return ""
        # else:
        #     return ""


    def transformToDictOrRegex(self):

        if    self.combox21.currentText() == "使用正则":
            self.btn21.setEnabled(True)
            pass
        else:
            self.sonDictIndex=[]
            self.btn21.setEnabled(False)

        self.combox22.addItems(self.sonDictIndex)

    def showSonInformation(self,rspdata,dictdata):
        data = dictdata.split(".")
        if rspdata == "":
            yield ""

        elif re.match("{",rspdata):
            try:
                t=eval(rspdata)
                if isinstance(t,dict):
                    try:
                        ss=UsefulMethod.parseindex(t,data)
                        for rr in ss:
                            yield rr
                    except Exception as showSonInformationerr1:
                        self.quirefilterWarning(showSonInformationerr1)

            except Exception as getsondataerr:
                if "NameError" in getsondataerr.__repr__():
                    d = re.search(r"\'(.*?)\'", getsondataerr.__str__()).group(1)
                    globals()[d] = d
                    self.configdict
                    self.showSonInformation(rspdata,dictdata)
                else:
                    self.quirefilterWarning(getsondataerr.__repr__())
                    return
        else:
            yield ""

    def tableContentText(self):
        sender=self.sender()
        sender.currentColumn()
        self.table21.setWordWrap(True)
        self.table21.resizeRowsToContents()

    def tablerightmenushow(self):
        self.table_menu = QMenu(self.table21)
        action1 = QAction(u"show detail  F2",self)
        action2 = QAction(u"delete current column",self)
        action3 = QAction(u"show single row",self)
        action4 = QAction(u"add column", self)
        self.table_menu.addAction(action1)
        self.table_menu.addAction(action2)
        self.table_menu.addAction(action3)
        self.table_menu.addAction(action4)
        # action1.triggered.connect(self.show_detailinfo)
        action2.triggered.connect(self.deletecolumn)
        action3.triggered.connect(self.showSingalRow)
        action4.triggered.connect(self.addColumn)
        pos = QCursor.pos()  # 获取鼠标在父窗体当前相对位置
        self.table_menu.move(pos)
        self.table_menu.show()

    def showSingalRow(self):
        self.table21.setWordWrap(False)
        for s in range(self.table21.rowCount()):
            self.table21.setRowHeight(s,1)

    def addColumn(self):
        self.table21.setColumnCount(self.table21.columnCount()+1)

    def deletecolumn(self):
        k=self.table21.currentColumn()
        self.table21.removeColumn(k)
        try:
            del self.configdict[self.queryName]["querylist"][k]
        except IndexError:
            pass
    def add_del_key_clicked(self):
        text = self.sender().text()
        if self.combox11.currentText() != "":
            self.linetextnext1.setHidden(False)
            if text == "Add to list":
                self.line_many_index_list.append(self.combox11.currentText())
                self.linetextnext1.setHidden(False)
            elif text == "DEL":
                if len(self.line_many_index_list) >= 1:
                    del self.line_many_index_list[-1]

                else:
                    pass
            self.linetextnext1.setText(str(self.line_many_index_list))
        else:
            pass



    def showMainDictData(self):
        #隐藏多条件添加的查询框
        self.linetextnext1.setHidden(True)
        self.linetextnext1.clear()
        s= None
        if self.linetext12.text() == "":
            self.quirefilterWarning("请输入列名")
        else:
            if len(self.line_many_index_list) == 0:
                s = self.combox11.currentText()
            else:
                s = self.line_many_index_list
            logging.debug("showMainDictData-s:{}".format(s))
            logging.debug("showMainDictData-text-dict:{},{}".format(self.linetext12.text(),self.configdict))
            if "querylist" in self.configdict[self.queryName].keys():
                if self.linetext12.text() not in self.configdict[self.queryName]["querylist"]:
                    self.configdict[self.queryName]["querylist"].append({self.linetext12.text():deepcopy(s)})
                else:
                    self.quirefilterWarning("列名已存在，请重新输入")
                    return
            else:
                self.configdict[self.queryName]["querylist"]=[]
                self.configdict[self.queryName]["querylist"].append({self.linetext12.text(): deepcopy(s)})

                data=self.getNeedData(self.response,self.sort)
                d=0
                for x in data:
                    self.table21.setVerticalHeaderItem(d,QTableWidgetItem(x))
                    d+=1
                    if d > self.configdict[self.queryName]["body"]["size"]:
                        self.quirefilterWarning("Indexerr，请核对日期数据是否与其他数据对应")

            self.showNeedData(self.response, {self.linetext12.text(): s},
                              len(self.configdict[self.queryName]["querylist"]) - 1)
        self.line_many_index_list.clear()
        self.combox21.setCurrentIndex(0)
        self.combox22.clear()


    #遍历显示数据
    def showNeedData(self,response,a,column):  #a格式{"":""},column为显示的列
        c=0
        #显示行
        for key in a.keys():
            self.table21.setHorizontalHeaderItem(column,QTableWidgetItem(key))
            for s in response["hits"]["hits"]:
                data = self.get_data_by_index_from_list(s["_source"],a[key])
                k = QTableWidgetItem(str(data))
                self.table21.setItem(c,column,k)
                c += 1

    def showOrHiddeSearchCondition(self):
        sender=self.sender()
        if sender.text() == "添加查询条件":
            self.combox1.setHidden(False)
            self.combox2.setHidden(False)
            self.linetext3.setHidden(False)
            self.btn4.setHidden(False)
            self.btn2.setText("取消条件查询")
        elif sender.text() == "取消条件查询":
            self.combox1.setHidden(True)
            self.combox2.setHidden(True)
            self.linetext3.setHidden(True)
            self.btn4.setHidden(True)
            self.btn2.setText("添加查询条件")

    def get_data_by_index_from_list(self,data,keys):
        if isinstance(keys,str):
            return DictAndStrTransfer.get_data_byindex(data, keys.split("."))
        elif isinstance(keys,list):
            for a in keys:
                if DictAndStrTransfer.get_data_byindex(data,a.split(".")) == "":
                    pass
                else:
                    return DictAndStrTransfer.get_data_byindex(data,a.split("."))
            return ""
        else:
            return ""


    def getAllIndex(self):
        self.combox11.clear()
        index=self.getsearchindex(self.configdict[self.queryName]["index"],days=1)
        if self.linetext1.text() != "":
            self.configdict[self.queryName]["body"]["query"]["bool"]["must"].append(self.addQuireRule(self.linetext1.text()))
        else:
            pass

        body=self.configdict[self.queryName]["body"]
        logging.debug("getAllIndex-body:{}".format(body))
        self.response=self.getResponse(body,index)
        # for hit in self.response["hits"]["hits"]:
        #     DictAndStrTransfer.transfer_to_index(hit["_source"])
        lock = threading.Lock()
        for i in range(10):
            t = threading.Thread(target=self.addtask,args=(self.response["hits"]["hits"],i,lock))
            t.start()
            t.join()

        k=DictAndStrTransfer.get_indexlist()
        for s in k:
            # if s not in self.indexlist:
            self.indexlist.append(s)
        self.indexlist.sort()
        self.combox1.addItems(self.indexlist)
        self.combox11.addItems(self.indexlist)
        #遍历数据所有主子键并显示
        # self.showIndexDataType()
    def addtask(self,data,number,lock):
        for s in range(number*50,(number+1)*50):
            DictAndStrTransfer.transfer_to_index(data[s]["_source"])
    def showIndexDataType(self):
        self.linetext12.setText(self.combox11.currentText())
        self.linetext21.clear()

    def getIndexDatatype(self,response,index):
        list1=[]
        a=index.split(".")
        for hit in response["hits"]["hits"]:
            for data in  UsefulMethod.parseindex(hit["_source"],a):
                if str(type(data).__name__) not in list1:
                    list1.append(type(data).__name__)
                    list1.append(1)
                else:
                    b=list1.index(str(type(data).__name__))
                    list1[b+1]+=1
        return str(list1)




    def addQuireRule(self,quirycondition,quirekey=None,quirefilter=None):
        if quirekey == None and quirycondition != "":
            return {
                "query_string": {
                 "query": "{}".format(quirycondition)
                  }}

        else:
            if quirefilter == None:
                self.Warning("请选择filter")


    def quirefilterWarning(self,tips):
        QMessageBox.warning(self,"Warning",tips,QMessageBox.Yes)


    def getResponse(self,body,index,days=7):
        Elasticsearch_5601.body =   body
        if isinstance(index,list):
            Elasticsearch_5601.index=   index[0][:-11]
        logging.debug(f"splitindex:{Elasticsearch_5601.index}")
        Elasticsearch_5601.days =   days
        return Elasticsearch_5601.getdata()

    def getNeedData(self,responseResult,needvalue=None,flag=0):#needvalue为需要数据的路径，格式为'a.b.c'
        if flag == 0:#获取对应键的值
            a=needvalue.split(".")
            for hit in responseResult["hits"]["hits"]:
                data=hit["_source"]
                for dd in  UsefulMethod.parseindex(data,a):
                    if dd == None:
                        yield ""
                    else:
                        if isinstance(dd,str):
                            yield  dd
                        else:
                            yield str(dd)
        elif flag == 1:#获取索引
            for hit in responseResult["hits"]["hits"]:
                for q in UsefulMethod.getMainkeyAndSonkey(hit["_source"]):
                    yield q
        elif flag == 2:#获取日志总数
            for hit in responseResult["hits"]["hits"]:
                pass
        elif flag == 3:#获取对应键的数据类型
            pass


    def getTablecolumns(self):
        return self.table21.columnCount()
    def getTablecolumWidth(self,column):
        return self.table21.columnWidth(column)


    def getsearchindex(self,index,days=7):
        totalDays = []
        totalIndex = []
        today = datetime.utcnow()
        if index != "setup_log":
            for i in range(0, days):
                totalDays.append((today - timedelta(i)).__format__('%Y-%m-%d'))
        else:
            for i in range(0, 100):
                totalDays.append((today - timedelta(i)).__format__('%Y.%m.%d'))
        for i in totalDays:
            totalIndex.append(index + "-"+ i)
        return totalIndex
    def savaConfigFile(self):
        if "query_string" in self.configdict[self.queryName]["body"]["query"]["bool"]["must"][-1].keys():
            del self.configdict[self.queryName]["body"]["query"]["bool"]["must"][-1]
        a=Rwfile()
        file=os.path.exists("./cfg.json")
        if file:
            f=open("./cfg.json","r",encoding="utf-8")
            listdata=json.load(fp=f)
            # print(listdata)
            listdata[self.queryName]=self.configdict[self.queryName]
            listdata[self.queryName]["columnwidths"]=[]
            for b in range(self.getTablecolumns()):
                listdata[self.queryName]["columnwidths"].append(self.getTablecolumWidth(b))

            f.close()
            a.writeToFile(listdata)
        else:
            # print(self.configdict)
            a.writeToFile(self.configdict)
        self.quirefilterWarning("保存成功")


fnclicked=0
class InquiryPage(QWidget):
    def __init__(self,text,configdict):
        super().__init__()
        self.text=text
        self.configdict=configdict
        self.configpageparent=SearchAndShowconfig(configdict,text)
        self.searchResult=dict()
        self.sort = UsefulMethod.getsignaldictkey(self.configdict[self.text]["body"],"sort")
        self.showInquiryPage()
    def showInquiryPage(self):
        self.setWindowTitle(self.text)
        self.setWindowIcon(QIcon("./pic/Kibana.png"))
        self.setGeometry(200,100,900,800)

        self.topwidget=QWidget(self)
        self.toplayout=QHBoxLayout()
        self.topwidget.setLayout(self.toplayout)

        self.secondwidget=QWidget(self)
        self.secondlayout=QHBoxLayout()
        self.secondwidget.setLayout(self.secondlayout)
        self.secondwidget.setHidden(True)

        self.middlewidget=QWidget(self)
        self.mainlayout=QVBoxLayout()
        self.setLayout(self.mainlayout)
        self.mainlayout.setStretch(0,0)
        #设置主布局和子布局
        self.combox1=QComboBox(self)
        self.combox1.addItem("全局查询")
        self.btn0 = QPushButton("GetIndex",self)
        self.btn0.clicked.connect(self.setcombox1items)
        self.combox11=QComboBox(self)
        self.combox11.addItem("is")
        self.combox1.currentIndexChanged.connect(self.combox11Setting)
        self.linetext1=QLineEdit(self)
        self.linetext1.setPlaceholderText("输入查询条件")
        self.linetext1.returnPressed.connect(self.searchbtnclicked)
        self.combox12=QComboBox(self)
        self.combox12.addItems(["today","7 days","30 days"])
        self.combox12.setCurrentIndex(1)
        self.btn1=QPushButton("查询",self)
        self.btn1.clicked.connect(self.searchbtnclicked)
        self.btn11=QPushButton("添加查询条件",self)
        self.btn11.clicked.connect(self.addCondition)

        self.combox2 = QComboBox(self)
        self.combox21 = QComboBox(self)
        self.combox21.addItems(["is", "not", "or"])
        self.linetext2 = QLineEdit(self)
        self.linetext2.setPlaceholderText("输入查询条件")
        self.Frame2=QFrame(self)

        self.table=Tablewidget(self)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setGeometry(20,0,880,800)
        self.table.textwindow.setGeometry(20,0,800,700)
        self.table.clicked.connect(self.get_row_click_all_data)
        self.table.cellDoubleClicked.connect(self.showContentByAdaptive)
        # self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showRightMenu)
        # self.table.setHorizontalScrollBarPolicy()
        # self.table.horizontalScrollbarValueChanged.connect(self.verticalScrollbarshow)
        # self.table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # self.table.setRowCount(self.configdict[self.text]["body"]["size"])
        self.textwindow = QTextEdit(self)
        self.textwindow.setVisible(False)

        self.Frame=QFrame(self)
        self.Frame.resize(self.width(),100)
        self.buttomlayout=QHBoxLayout()
        self.Frame.setLayout(self.buttomlayout)
        self.lable3=QLabel(self.Frame)
        self.lable3.setGeometry(0,0,10,40)

        self.btn31=QPushButton("上一页", self.Frame)
        self.btn31.clicked.connect(self.frontOrNextPage)
        self.btn32=QPushButton("下一页", self.Frame)
        self.btn32.clicked.connect(self.frontOrNextPage)
        # self.btn32.setGeometry(0,self.Frame.width()/2+10,10,70)
        self.frame3=QFrame(self.Frame)
        self.buttomlayout.addWidget(self.lable3, Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.btn31,  Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.btn32,  Qt.AlignVCenter)
        self.buttomlayout.addWidget(self.frame3, Qt.AlignVCenter)
        self.buttomlayout.setStretchFactor(self.lable3, 4)
        self.buttomlayout.setStretchFactor(self.btn31,  1)
        self.buttomlayout.setStretchFactor(self.btn32,  1)
        self.buttomlayout.setStretchFactor(self.frame3, 4)

        self.toplayout.addWidget(self.combox1,Qt.AlignTop)
        self.toplayout.addWidget(self.combox11,Qt.AlignTop)
        self.toplayout.addWidget(self.linetext1,Qt.AlignTop)
        self.toplayout.addWidget(self.combox12, Qt.AlignTop)
        self.toplayout.addWidget(self.btn1,Qt.AlignTop)
        self.toplayout.addWidget(self.btn11,Qt.AlignTop)
        self.toplayout.addWidget(self.btn0, Qt.AlignTop)
        self.toplayout.setStretchFactor(self.combox1, 4)
        self.toplayout.setStretchFactor(self.btn0, 1)
        self.toplayout.setStretchFactor(self.combox11, 1)
        self.toplayout.setStretchFactor(self.linetext1, 4)
        self.toplayout.setStretchFactor(self.combox12, 1)
        self.toplayout.setStretchFactor(self.btn1, 2)
        self.toplayout.setStretchFactor(self.btn11, 2)


        self.secondlayout.addWidget(self.combox2, 2, Qt.AlignTop)
        self.secondlayout.addWidget(self.combox21, 2, Qt.AlignTop)
        self.secondlayout.addWidget(self.linetext2, 10, Qt.AlignTop)
        self.secondlayout.addWidget(self.Frame2, 5, Qt.AlignTop)

        self.mainlayout.addWidget(self.topwidget,1,Qt.AlignTop)
        self.mainlayout.addWidget(self.secondwidget,1,Qt.AlignTop)
        self.mainlayout.addWidget(self.table,30)
        self.mainlayout.addWidget(self.Frame,1,Qt.AlignBottom)
        self.show()
        # self.setcombox1items()
    def get_row_click_all_data(self):
        row = self.table.currentRow()
        self.table.textwindow_text = self.searchResult["hits"]["hits"][row]
        print("Tablewidget.textwindow_text:{}".format(self.table.textwindow_text))

    def showRightMenu(self):
        self.table_menu = QMenu(self.table)
        action1 = QAction(u"show detail  F2", self)
        action2 = QAction(u"hide current column", self)
        action3 = QAction(u"show single row", self)
        action4 = QAction(u"transfer to datetime", self)

        self.table_menu.addAction(action1)
        self.table_menu.addAction(action2)
        self.table_menu.addAction(action3)
        self.table_menu.addAction(action4)

        action1.triggered.connect(self.showDetail)
        action2.triggered.connect(self.hidecolumn)
        action3.triggered.connect(self.showSingalRow)
        action4.triggered.connect(self.transfer_to_datetime_by_column)

        pos = QCursor.pos()  # 获取鼠标在父窗体当前相对位置
        self.table_menu.move(pos)
        self.table_menu.show()
    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.table.textwindow.setGeometry(20, 0, self.width()-100, self.height() - 100)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent == Qt.Key_Escape:
            if self.textwindow.isVisible():
                self.textwindow.setVisible(False)
                self.textwindow.close()

    def combox11Setting(self):
        sender = self.sender()
        self.combox11.clear()
        if self.combox1.currentText() != "全局查询":
            self.combox11.addItems(["is","or","not"])
        else:
            self.combox11.addItem("is")

    def addCondition(self):
        sender=self.sender()
        if sender.text() == "添加查询条件":
            if self.combox2.count() == 0:
                for x in range(1,self.combox1.count()):
                    self.combox2.addItem(self.combox1.itemText(x))
            else:
                pass
            self.secondwidget.setHidden(False)
            self.btn11.setText("取消添加")
        elif sender.text() == "取消添加":
            self.secondwidget.setHidden(True)
            self.btn11.setText("添加查询条件")
    def hidecolumn(self):
        self.table.setColumnHidden(self.table.currentColumn(),True)

    def showSingalRow(self):
        self.table.setWordWrap(False)
        for s in range(self.table.rowCount()):
            self.table.setRowHeight(s, 1)

    def transfer_to_datetime_by_column(self):
        column = self.table.currentColumn()

        for row in range(self.table.rowCount()):
            data = self.transform_to_datetime(self.table.item(row,column).text())
            logging.debug("row,column,data:{},{},{}".format(row,column,data))
            if data == "":
                pass
            else:
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

    def transform_to_datetime(self,string):
        logging.debug("transform_to_datetime_string:{}".format(string))
        time = ""
        try:
            for s in string.split("\n"):
                # logging.debug("transform_to_datetime_s:{}".format(s))
                time += str(datetime.utcfromtimestamp(int(s)))+"\n"
            time = time[:-1]
        except:
            time = ""
        # logging.debug("transform_to_datetime_time:{}".format(time))
        return time

    def frontOrNextPage(self):
        sender=self.sender()
        global fnclicked
        if   sender.text() == "上一页":
            if fnclicked >= 1:
                fnclicked -= 1
                self.configdict[self.text]["body"]["from"] = self.configdict[self.text]["body"]["size"] * fnclicked
                # print(fnclicked)
                # print(self.configdict[self.text]["body"]["from"])
                self.searchbtnclicked()
            else:
                pass
        elif sender.text() == "下一页":

            if self.configdict[self.text]["body"]["size"] * (fnclicked + 1) < self.searchResult["hits"]["total"]:
                fnclicked += 1
                self.configdict[self.text]["body"]["from"] = self.configdict[self.text]["body"]["size"] * fnclicked
                # print(fnclicked)
                # print(self.configdict[self.text]["body"]["from"])
                self.searchbtnclicked()
            else:
                pass

    def showDetail(self):
        self.textwindow.setGeometry(100, 100, self.width() - 200, self.height() - 200)
        row=self.table.currentRow()
        detail = self.searchResult["hits"]["hits"][row]
        self.textwindow.setText(json.dumps(detail, indent=5, ensure_ascii=False))
        self.textwindow.setVisible(True)
        self.textwindow.show()

    def showContentByAdaptive(self):
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()

    def searchbtnclicked(self):
        self.table.clear()
        self.searchResult.clear()
        self.configdict[self.text]["body"]["query"]["bool"]["must"] = \
            self.configdict[self.text]["body"]["query"]["bool"]["must"][:1]
        self.showGIF=ShowMovieAndOther(self,self.searchResultByConditions,self.sonThreadAchieved)

    def getSearchResult(self,result):
        self.searchResult=result

    def sonThreadAchieved(self):
        self.showdata()

    def showdata(self):
        self.table.setRowCount(len(self.searchResult["hits"]["hits"]))
        self.table.setColumnCount(len(self.configdict[self.text]["columnwidths"]))
        for l in range(len(self.configdict[self.text]["columnwidths"])):
            self.table.setColumnHidden(l,False)
        timerow = 0
        self.lable3.setText("total:"+str(self.searchResult["hits"]["total"]))
        for time in self.configpageparent.getNeedData(self.searchResult, self.sort):
            self.table.setVerticalHeaderItem(timerow, QTableWidgetItem(time))
            timerow += 1
        for a in range(len(self.configdict[self.text]["querylist"])):
            self.table.setColumnWidth(a,self.configdict[self.text]["columnwidths"][a])
            for b in self.configdict[self.text]["querylist"][a].keys():
                self.table.setHorizontalHeaderItem(a, QTableWidgetItem(b))
                querydata = self.configdict[self.text]["querylist"][a][b]
                if isinstance(querydata, str):
                    row = 0
                    for c in self.searchResult["hits"]["hits"]:
                        data = DictAndStrTransfer.get_data_byindex(c["_source"],querydata.split("."))
                        self.table.setItem(row, a, QTableWidgetItem(str(data)))
                        row += 1
                if isinstance(querydata,list):
                    row = 0
                    for c in self.searchResult["hits"]["hits"]:
                        data = self.configpageparent.get_data_by_index_from_list(c["_source"],querydata)
                        self.table.setItem(row, a, QTableWidgetItem(str(data)))
                        row += 1
                elif isinstance(querydata, dict):
                    row = 0

                    if querydata["regex"]:
                        for x in self.searchResult["hits"]["hits"]:
                            maindata = self.configpageparent.get_data_by_index_from_list(x["_source"], querydata["mainkey"])
                            # maindata = DictAndStrTransfer.get_data_byindex(c["_source"], querydata["mainkey"].split("."))
                            pat = querydata["regex"]
                            regexfinddata = self.configpageparent.getRegexdata(str(maindata), pat,flag=1)
                            self.table.setItem(row, a, QTableWidgetItem(regexfinddata))
                            row += 1

                else:
                    pass
        for col in range(self.table.columnCount()):
            count=0
            for row in range(self.table.rowCount()):
                if isinstance(self.table.item(row,col),type(None)):
                    count += 1
                elif self.table.item(row,col).text() == "":
                    count+=1
                else:
                    break
            if count == self.table.rowCount():
                self.table.setColumnHidden(col,True)

    def searchResultByConditions(self):
        index=self.getSearchIndex()
        condition=self.configdict[self.text]["body"]["query"]["bool"]
        condition["must_not"]=[]

        if self.linetext1 != ""  and self.combox11.currentText() != "not":
            condition["must"].append(self.getQueryConditionFormText(self.combox1.currentText(),self.combox11.currentText(),self.linetext1.text()))
        elif self.combox11.currentText() == "not":
            condition["must_not"].append(self.getQueryConditionFormText(self.combox1.currentText(),self.combox11.currentText(),self.linetext1.text()))
        else:
            pass

        if self.btn11.text() == "取消添加":
            if self.linetext2.text() != "" and self.combox21.currentText() != "not":
                condition["must"].append(self.getQueryConditionFormText(self.combox2.currentText(),self.combox21.currentText(),self.linetext2.text()))
            elif self.combox21.currentText() == "not":
                condition["must_not"].append(self.getQueryConditionFormText(self.combox2.currentText(),
                                                                       self.combox21.currentText(), self.linetext2.text()))
            else:
                pass

        self.searchResult=self.configpageparent.getResponse(self.configdict[self.text]["body"],index)
        logging.debug(f"searchresult:{self.searchResult}")
        if self.searchResult["hits"]["total"] == 0 and "setup" in index[0]:
            s = []
            for a in index:
                s.append(a.replace(".",""))
            self.searchResult = self.configpageparent.getResponse(self.configdict[self.text]["body"], s)


    def getQueryConditionFormText(self,index,filter,condition):
        if condition != "":
            if  index   ==   "全局查询":
                if  filter  == "is":
                    return {
                    "query_string": {
                     "query": "{}".format(condition)
                      }}
                else:
                    return {}
            else:
                if filter == "is":
                    return {"match_phrase":
                                {index:
                                     {"query":condition}}}
                elif filter == "or":
                    ss = {"bool":
                                {"should":[],
                                 "minimum_should_match":1}}
                    condition=condition.split(" ")
                    for a in range(len(condition)):
                        ss["bool"]["should"].append({"match_phrase":
                          {index: condition[a]}})
                    return ss
                elif filter == "not":
                    return {
                        "match_phrase":{
                            index:{
                                "query":condition
                            }
                        }
                    }
        else:
            return {}

    def getSearchIndex(self):
        days=0
        if self.combox12.currentText() == "7 days":
            days = 7
        elif self.combox12.currentText() == "today":
            days = 1
        elif self.combox12.currentText() == "30 days":
            days = 30
        return self.configpageparent.getsearchindex(self.configdict[self.text]["index"],days=days)

    def setcombox1items(self):
        # a=self.get_index()
        ShowMovieAndOther(self, self.get_index,self.get_index_acheived)
        # self.combox1.addItems(a)
    def get_index(self):
        list1=[]
        body=self.configdict[self.text]["body"]
        index=self.configpageparent.getsearchindex(self.configdict[self.text]["index"],days=1)
        response=self.configpageparent.getResponse(self.configdict[self.text]["body"],index)
        for x in self.configpageparent.getNeedData(response,flag=1):
            if x not in list1:
                list1.append(x)
        self.combox1.addItems(list1)

    def get_index_acheived(self):
        self.btn0.setEnabled(False)


class ShowMovieAndOther():
    def __init__(self,fa,usemethod,achieved,args=()):
        fa.showmovie = ShowMovie(fa.width(), fa.height(), fa)
        fa.showmovie.showMovie()
        fa.start = ThreadMethod(usemethod, args)
        fa.start.start()
        fa.start.acheived.connect(fa.showmovie.cloMovie)
        fa.start.acheived.connect(achieved)

class ShowMovie(QLabel):
    def __init__(self,width,height,parent):
        super(ShowMovie,self).__init__()
        self.setParent(parent)
        self.setGeometry(width/2 - 100, height / 2 - 100, 200, 200)
        self.movie = QMovie("../SOURCES/pic/loading.gif")
        self.movie.setScaledSize(self.size())
        self.setMovie(self.movie)
    def showMovie(self):
        self.show()
        self.movie.start()
    def cloMovie(self):
        self.movie.stop()
        self.close()


class ThreadMethod(QThread):
    acheived=pyqtSignal()
    def __init__(self,method,args):
        super(ThreadMethod,self).__init__()
        self.method=method
        self.args=args
        self.stopFlag=False

    def run(self,flag=0):
        if self.args==():
            self.method()
        else:
            self.method(arg for arg in self.args)
        self.acheived.emit()


class UsefulMethod():
    def __init__(self):
        pass
    @classmethod
    def getMainkeyAndSonkey(cls, d, sk="", s=[]):
        for k, v in d.items():
            if type(v) is dict:
                if sk == "":
                    sk = k
                else:
                    sk = sk + "." + k
                ddd = UsefulMethod.getMainkeyAndSonkey(v, sk)
                for a in ddd:
                    yield a
                sk = sk.split(".")
                if len(sk) == 1:
                    sk = ""
                else:
                    sk = ".".join(sk[:-1])
                # 因yield使用中，该层字典遍历完成后保存的sk为当前的值，而不是调用函数进行赋值操作，所以需要对sk的值重新定义，切掉末尾的键值
            else:
                if sk == "":
                    yield k
                else:
                    yield (sk + "." + k)

    #访问dictdata的["a","b","c"]元素
    @classmethod
    def parseindex(cls,dictdata,a):
        try:
            for s in a:
                if len(a) ==0:
                    pass
                elif len(a) == 1:
                    if isinstance(dictdata,dict):
                        pass
                    elif isinstance(dictdata,str) and re.match(r"\"{",dictdata):
                        dictdata = eval(dictdata)
                    yield dictdata[a[0]]
                else:
                    # if isinstance(dictdata,dict):
                    #     pass
                    # elif isinstance(dictdata,str) and re.match(r"\"{",dictdata):
                    #     dictdata = eval(dictdata)
                    dd=UsefulMethod.parseindex(dictdata[a[0]],a[1:])
                    for t in dd:
                        yield t
                        return
        except KeyError:
            # yield  None
            yield ""
        except TypeError:
            # yield None
            yield ""
    @classmethod
    def getsignaldictkey(cls,dictdata,keyvalue):
        value=""
        for x in dictdata[keyvalue]:
            value=x
        return value
class Transform(QWidget):
    def __init__(self):
        super(Transform, self).__init__()
        self.setGeometry(100,100,600,800)
        self.setWindowTitle("json强制转换解析")
        self.btn1 = QPushButton("提取Key",self)
        self.btn1.clicked.connect(self.getkey)
        self.btn2 = QPushButton("解析key",self)
        self.btn2.clicked.connect(self.sovekey)
        self.cobox = QComboBox(self)
        self.cobox.addItems(["不使用正则","使用正则"])
        self.cobox.currentTextChanged.connect(self.cobox_change)
        self.lab1 = QLabel("解析Key值",self)
        self.lineedit = QLineEdit(self)
        self.lineedit.setEnabled(False)
        self.text1 = QTextEdit(self)
        self.text1.setPlaceholderText("输入原始字符串")
        self.text0 = QLineEdit(self)
        self.text0.setPlaceholderText("填入解析的Key值")
        self.text2 = QTextEdit(self)
        self.text3 = QTextEdit(self)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.text1,0,0,10,20)
        layout.addWidget(self.btn1,11,0,1,2)
        layout.addWidget(self.lab1,11,2,1,2)
        layout.addWidget(self.text0,11,4,1,6)
        layout.addWidget(self.cobox,11,10,1,2)
        layout.addWidget(self.lineedit,11,12,1,4)
        layout.addWidget(self.btn2,11,16,1,2)
        layout.addWidget(self.text2,12,0,10,10)
        layout.addWidget(self.text3,12,10,10,10)
        self.show()
    def cobox_change(self):
        text = self.cobox.currentText()
        if text == "不使用正则":
            self.lineedit.setEnabled(False)
        elif text == "使用正则":
            self.lineedit.setEnabled(True)

    def getkey(self):
        self.text2.clear()
        text = self.text1.toPlainText()
        DictAndStrTransfer.transfer_to_index(text)
        keys = DictAndStrTransfer.get_indexlist()
        # logging.debug("keys:{}".format(keys))
        txt = ""
        for s in keys:
            txt += (s+"\n")
        self.text2.setPlainText(txt)

    def sovekey(self):
        self.text3.clear()
        sourcetext = self.text1.toPlainText()
        index = self.text0.text()
        if index.startswith("[") and index.endswith("]"):
            try:
                index = eval(index)
                for x in index:
                    data = DictAndStrTransfer.get_data_byindex(sourcetext,x.split("."))
                    if data:
                        if self.lineedit.text():
                            data1 = self.getRegexdata(data,self.lineedit.text())
                            self.text3.setPlainText(data1)
                        else:
                            self.text3.setPlainText(data)
                if not self.text3.toPlainText():
                    self.text3.setPlainText("无数据")
            except Exception as e:
                self.text3.setPlainText(str(e))
        else:
            try:
                data = DictAndStrTransfer.get_data_byindex(sourcetext,index.split("."))
                if data:
                    if self.lineedit.text():
                        data1 = self.getRegexdata(data, self.lineedit.text())
                        self.text3.setPlainText(data1)
                    else:
                        self.text3.setPlainText(data)
            except Exception as f:
                self.text3.setPlainText(str(f))

    def getRegexdata(self,sourcedata,regexdata):
        if  regexdata.startswith("(") and regexdata.endswith(")"):
            #这里传入的regexdata需要是"(re.compile(r正则))"
            try:
                rex = eval(regexdata)
                for s in rex:
                    result = s.search(sourcedata)
                    # logging.debug("result:{}".format(result))
                    if result:
                        try:
                            return result.group(1)
                        except:
                            return result.group(0)
                return ""
            except Exception as e:
                print(e)
                return ""
        else:
            if "\\" in regexdata:
                regexdata = regexdata.replace("\\", "\\\\")
            pat1=re.compile(r"{}".format(regexdata))
            result=pat1.search(sourcedata)
            if result:
                try:
                    return result.group(1)
                except:
                    return result.group(0)
            else:
                return ""

if __name__ == "__main__":
    try:
        app=QApplication(sys.argv)
        s=defineWindow()
        # s = Transform()
        app.exec_()
    except Exception as e:
        print(e)
        d = input()

