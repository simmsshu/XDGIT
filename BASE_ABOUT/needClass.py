import requests,re,json,time
from PyQt5.QtWidgets import QLabel,QApplication,QLineEdit,QTableWidgetItem,QFrame,QAbstractItemView,QPushButton,QTextEdit,QHBoxLayout,\
                            QGridLayout,QVBoxLayout
from PyQt5.QtGui import QMovie,QIcon,QColor,QMouseEvent,QPaintEvent,QPainter,QBrush,QFont
# from PyQt5.Qt import QPixmap,QFont
from PyQt5.QtCore import pyqtSignal,Qt,QModelIndex,QRect,QPoint,QThread
from PyQt5.QtWidgets import QTableWidget,QAbstractItemView,QWidget
# from multiprocessing import Process
from datetime import datetime,timedelta
from elasticsearch import Elasticsearch
from bson import ObjectId
from csv import  DictWriter
import logging
import sys
import importlib
import threading
import json
import copy
logging.basicConfig(level= logging.DEBUG)
sys.path.append("")
PIC_BASE_DIR = "../SOURCES/pic/"
pressFlag = -1
#获取当前屏幕
def get_current_screen_desktop():
    return QApplication.desktop().screen(QApplication.desktop().screenNumber())

# def add_uncertain_data(data,number,sourlist = [],sourcedict = {}):
#     '''
#     :param data: 字典数据
#     :param number: 第几条request.data
#     :return: sourlist:sourcedita所有键值keys列表;sourcedict：sourcedata对应的键，值--值为list
#     '''
#     if number == 1:
#         for d in data.keys():
#             sourlist.append(d)
#             sourcedict[d] = []
#             sourcedict[d].append(str(data[d]))
#     else:
#         for d in data.keys():
#             if d not in sourlist:
#                 sourlist.append(d)
#                 sourcedict[d] = []
#                 for s in range(number-1):
#                     sourcedict[d].append("")
#                 sourcedict[d].append(data[d])
#         for k in sourlist:
#             try:
#                 sourcedict[k].append(str(data[k]))
#             except KeyError:
#                 sourcedict[k].append("")
#     return sourlist,sourcedict

def write_listDict_to_csv(_path,data:"list[dicts]"):
    with open(_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        f.close()

def drop_empty(string):
    string = string.strip()
    return string.replace("\n","")

def sovedict(data,keys):
    '''
    :param data: 字典数据
    :param keys: 需要匹配的键以"a.b.c"格式传入
    :return: str
    '''
    d = keys.split(".")
    logging.debug("sovedict-keys:{}".format(d))
    return _getvaluebykey(data,d)

def _getvaluebykey(data,keys):
    '''
    :param data: 字典数据
    :param keys: 需要匹配的键以"a.b.c"格式传入
    :return: str
    '''
    try:
        if len(keys) > 1:
            return _getvaluebykey(data[keys[0]],keys[1:])
        else:
            return str(data[keys[0]])
    except KeyError:
        logging.warning("this item can't sove to dict:{},{}".format(data,keys))
        return ""

def getsearchindex(index, days=7,connect="-"):
    totalDays = []
    totalIndex = []
    today = datetime.utcnow()
    for i in range(0, days):
        totalDays.append((today - timedelta(i)).__format__('%Y-%m-%d'))

    for i in totalDays:
        totalIndex.append(index + connect + i)
    return totalIndex

def getbody(query,start = 0,size = 500,isFilter = True,filter = None,sort = None):
    body = {
        "size": size,  # 返回查询条数
        "from": start,  # 返回起始页
        "sort": {"T": {"order": "desc"}},  # 排序
        "_source": ["M", "T", "host.name"] # 返回指定字段
    }
    if sort is not None:
        body["sort"] = sort
    if isFilter is not True:
        del body["_source"]
    else:
        if filter is not None:
            if isinstance(filter,list):
                body["_source"] = filter
            else:
                print("body filter is {} but need list".format(type(filter)))
    if isinstance(query,dict):
        for a in query.keys():
            body[a] = query[a]
        return body
    else:
        print("getbody method args need dict type")

def addKeyAndValeToDict(target,exitstarget,value):
    if isinstance(target,dict):
        if exitstarget in target.keys():
            if isinstance(target[exitstarget],dict):
                target[exitstarget]=[target[exitstarget]]
                target[exitstarget].append(value)
            elif isinstance(target[exitstarget],list):
                target[exitstarget].append(value)
            else:
                return target
        else:
            target[exitstarget] = []
            target[exitstarget].append(value)
        return target
    else:
        print("无法将目标数据加入非字典")
        return target

def from_list_get_need_key_and_value(data,keys,notequal = ""):
    if isinstance(data,list):
        for s in range(len(data)):
            if keys[0] in data[s].keys():
                if len(keys) > 1:
                    i = from_list_get_need_key_and_value(data[s][keys[0]],keys[1:])
                    if i != notequal and i != None:
                        return i
                else:
                    if data[keys[0]] != notequal:
                        return data[keys[0]]
                        break

    if isinstance(data,dict):
        if keys[0] in data.keys():
            if len(keys) > 1:
                from_list_get_need_key_and_value(data[keys[0]],keys[1:])
            else:
                if data[keys[0]] != notequal:
                    return data[keys[0]]



class TempleteWindow(QFrame):
    def __init__(self):
        super(TempleteWindow, self).__init__()
        self.setGeometry(200,200,get_current_screen_desktop().width()-400,get_current_screen_desktop().height()-400)
        #设置背景透明
        self.setAttribute(Qt.WA_TranslucentBackground)
        #设置窗口无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        #设置主窗体
        self.widget = QWidget(self)
        self.widget.setGeometry(0,0,self.width(),self.height())
        self.widget.setObjectName("mainwidget")
        self.set_mw_style()
        #设置title格式
        self.title = QLabel(self.widget)
        self.title.setGeometry(0, 0, self.widget.width(), 30)
        self.title.setObjectName("title")
        self.settitle_style()
        #设置主窗口样式
        self.contentWindow = QWidget(self.widget)
        self.contentWindow.setObjectName("content")
        self.setcontent_window_style()
        self.contentWindow.setGeometry(0, self.title.height(), self.widget.width(),
                                       self.widget.height() - self.title.height())
        #设置父类需要的子类属性和方法
        self.son_attr = None
        #设置标题栏
        self.titlepic = QPushButton(self.title)
        # self.titlepic.setDisabled(True)
        self.titlepic.setStyleSheet("QPushbuttom:pressed{border:1px solid white;}")
        # self.titlepic.height = self.title.height()
        self.title_tit = QLabel(self.title)
        self.close_btn = QPushButton(self.title)
        self.close_btn.clicked.connect(self.btn_close)
        self.normal_btn = QPushButton(self.title)
        self.normal_btn.clicked.connect(self.btn_normal)
        self.min_btn = QPushButton(self.title)
        self.min_btn.clicked.connect(self.btn_min)

        self.title_tit.setGeometry(25, 0, self.title.width()-125, 30)
        self.close_btn.setGeometry(self.title.width() - 35,0,30,30)
        self.normal_btn.setGeometry(self.title.width() - 65, 0, 30, 30)
        self.min_btn.setGeometry(self.title.width() - 95, 0, 30, 30)

        self.min_btn.setIcon(QIcon(PIC_BASE_DIR + "min.ico"))
        self.normal_btn.setIcon(QIcon(PIC_BASE_DIR + "max.ico"))
        self.close_btn.setIcon(QIcon(PIC_BASE_DIR + "close.ico"))
        self.setTitleWindow()
        self._initDrag()

    def set_son_attr(self,maps):
        '''
        :param maps: 该参数以键值对形式传递{"Module": "mainWindow", "class": "MainWindow", "method": "windowResize", "args": self})
        :return:
        '''
        self.son_attr = maps

    def btn_icon(self):
        pass

    def btn_min(self):
        self.showMinimized()

    def btn_normal(self):
        if self.isMaximized():
            self.showNormal()
            self.normal_btn.setIcon(QIcon(PIC_BASE_DIR + "max.ico"))
        else:
            self.showMaximized()
            self.normal_btn.setIcon(QIcon(PIC_BASE_DIR + "normal.ico"))
    def btn_close(self):
        self.close()

    def set_title(self,title):
        font = QFont("华文行楷",10)
        self.title_tit.setFont(font)
        # self.title_tit.setStyleSheet("QPushButton{border:None;background-color:None;text-align:left}")
        self.title_tit.setText(title)

    def mouseDoubleClickEvent(self,QMouseEvent):
        if QMouseEvent.pos() in self._top_rect:
            self.btn_normal()

    def setTitleWindow(self,pic = PIC_BASE_DIR + "kibana.png"):
        self.titlepic.setGeometry(2, 2, 25, 25)
        self.titlepic.setIcon(QIcon(pic))

    def settitle_style(self,color = 'rgb(199,250,204)'):
        style = '''QLabel#title{{border-top-left-radius:10px;border-top-right-radius:10px;background-color:{};}}
                                            QPushButton{{border-radius:5px;}}
                                            QPushButton:hover{{border:1px solid white;}}
                                            QPushButton:pressed{{border:1px solid;background-color:gray}}'''.format(color)
        self.title.setStyleSheet(style)
    def setcontent_window_style(self,color = 'rgb(199,237,204)'):
        pass
        self.contentWindow.setStyleSheet('''QWidget#content{{background-color:{};border-top-style:dotted;
                                            border-bottom-left-radius:10px;border-bottom-right-radius:10px;}}'''.format(color))

    def set_mw_style(self,border_radius = "10px",bc ="rgba(200,230,200,0.8)",style = "" ):
        if not style:
            self.QWidget_style = r'''
            QWidget#mainwidget{{border-radius:{};
                    background-color:{};
                    }}'''.format(border_radius,bc)
        else:
            self.QWidget_style = style
        self.widget.setStyleSheet(self.QWidget_style)
    def resizeEvent(self, QResizeEvent):
        # 自定义窗口调整大小事件
        # 改变窗口大小的三个坐标范围
        # self._right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5)
        #                     for y in range(self.widget.height() + 20, self.height() - 5)]
        # self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - 5)
        #                      for y in range(self.height() - 5, self.height() + 1)]
        # self._corner_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
        #                      for y in range(self.height() - 5, self.height() + 1)]
        self._top_rect = [QPoint(x, y) for x in range(30,self.width()-60)
                             for y in range(30)]
        #标题窗口和内容窗口和主显示窗口大小调整
        self.widget.setGeometry(0, 0, self.width(), self.height())
        self.title.setGeometry(0, 0, self.widget.width(), 30)
        self.contentWindow.setGeometry(0, self.title.height(), self.widget.width(),self.widget.height() - self.title.height())
        self.title_tit.setGeometry(25, 0, self.title.width() - 125, 30)
        self.close_btn.setGeometry(self.title.width() - 35, 0, 30, 30)
        self.normal_btn.setGeometry(self.title.width() - 65, 0, 30, 30)
        self.min_btn.setGeometry(self.title.width() - 95, 0, 30, 30)
        #如果子类有需要resize方法，resizeEvent同时调用子类方法
        if self.son_attr:
            try:
                module = importlib.import_module(self.son_attr["Module"])
                cla = getattr(module,self.son_attr["class"])
                meth = getattr(cla,self.son_attr["method"])
                meth(self.son_attr["args"])
            except Exception as e:
               print(e)


    def _initDrag(self):
        # 设置鼠标跟踪判断扳机默认值
        self._move_drag = False

    def mousePressEvent(self, event):
        # 重写鼠标点击的事件
        if (event.button() == Qt.LeftButton) and (event.pos() in self._top_rect):
            # 鼠标左键点击标题栏区域
            self._move_drag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

        else:
            self._move_drag = False
            # self._bottom_drag = False

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self._move_drag:
            # 标题栏拖放窗口位置
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()



    def mouseReleaseEvent(self, QMouseEvent):
        # 鼠标释放后，各扳机复位
        self._move_drag = False

    # def showwindinw(self):
    #     self.show()

class JSONEncoder(json.JSONEncoder):
    """处理ObjectId,该类型无法转为json"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)

class Tablewidget(QTableWidget):
    def __init__(self,parent):
        super().__init__()
        self.setParent(parent)
        self.frontandnextFlag = []
        self.pat = re.compile(r"<font style='background-color:red;'>(.*?)</font>")
        self.searchbox = QFrame(self)
        self.searchbox.setGeometry(10,50,330,30)
        # self.searchbox.setFrameRect(QRect(10,10,10,10))
        self.searchbox.setStyleSheet("border-radius:2px;background-color:rgb(200,200,200)")
        self.searchbox.setHidden(True)

        self.searchtextbox = QLineEdit(self.searchbox)
        self.searchtextbox.setGeometry(0,0,210,30)
        self.searchtextbox.setStyleSheet("border:none")

        #文本显示框
        self.textwindow = QTextEdit(self)
        self.textwindow.setGeometry(0,0, self.width() - 100, self.height() - 100)
        self.textwindow.setVisible(False)
        self.textwindow_text = None
        #搜索窗口
        self.search = QPushButton("", self.searchbox)
        self.search.setIcon(QIcon("./pic/search.ico"))
        self.search.setGeometry(210, 0, 30, 30)
        self.search.setStyleSheet("border:none")
        self.search.clicked.connect(self.searchdata)

        self.front  =   QPushButton("",self.searchbox)
        self.front.setIcon(QIcon("./pic/front.ico"))
        self.front.setGeometry(240,0,30,30)
        self.front.setStyleSheet("border:none")
        self.front.clicked.connect(lambda: self.frontandnextpress(-1))

        self.next   =   QPushButton("", self.searchbox)
        self.next.setIcon(QIcon("./pic/next.ico"))
        self.next.setGeometry(270,0,30,30)
        self.next.setStyleSheet("border:none")
        self.next.clicked.connect(lambda: self.frontandnextpress(1))

        self.clo = QPushButton("", self.searchbox)
        self.clo.setIcon(QIcon("./pic/close.ico"))
        self.clo.setGeometry(300, 0, 30, 30)
        self.clo.setStyleSheet("border:none")
        self.clo.clicked.connect(self.searchboxclo)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # 设置垂直方向滑块像素移动
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        # 设置水平方向滑块像素移动
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers | QAbstractItemView.DoubleClicked)
        # # 设置表格不可编辑
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # 设置启用右键策略

    def showdata(self, data):
        self.setRowCount(len(data[0]) - 1)
        self.setColumnCount(len(data))
        for i in range(0, len(data)):  # 总列数,显示所有数据
            self.setHorizontalHeaderItem(i, QTableWidgetItem(data[i][0]))
            for j in range(1, len(data[0])):  # 总数据行数
                ss = QTableWidgetItem(data[i][j])
                self.setItem(j - 1, i, ss)
                ss.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置所有单元格对齐方式

    def keyPressEvent(self, QkeyEvent):
        if QkeyEvent.key() == Qt.Key_F:
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.searchbox.show()
                self.searchbox.setHidden(False)
                self.searchtextbox.setFocus()
        elif QkeyEvent.key() == Qt.Key_Escape:
            if self.searchbox.isHidden():
                self.textwindow.setHidden(True)
            else:
                self.searchbox.setHidden(True)
                self.textwindow.setHidden(True)
        elif QkeyEvent.key() == Qt.Key_F2:
            self.textwindow.setGeometry(0,0, self.width() - 100, self.height() - 100)
            detail = JSONEncoder().encode(self.textwindow_text)
            detail = json.loads(detail)
            self.textwindow.setText(json.dumps(detail, indent=5, ensure_ascii=False))
            self.textwindow.setHidden(False)


    def searchdata(self):
        self.frontandnextFlag = []
        global  pressFlag
        pressFlag = -1
        findtext = ""
        # if self.searchtextbox.text() == "":
        #     return
        # else:
        try:
            findtext = self.searchtextbox.text().split()[0]
        except IndexError:
            findtext = "$@##$$@!!"  #如果为空，标记特殊寻找字符，找不到将Qlabel替换为字符串
        for a in range(self.rowCount()):
            for b in range(self.columnCount()):
                if isinstance(type(self.item(a,b)),type(None)) and isinstance(type(self.cellWidget(a,b)),type(None)):
                    pass
                else:

                    if isinstance(type(self.cellWidget(a,b)),type(QLabel)):
                        if "<font style" in self.cellWidget(a,b).text():
                            d = self.cancelCssFormat(self.cellWidget(a,b).text())
                            celltext = self.cellWidget(a,b).text().replace(
                                "<font style='background-color:red;'>{}</font>".format(d),
                                d)
                            if findtext in celltext:
                                self.cellWidget(a,b).setText(self.setStrkeyColor(celltext,findtext))
                                self.frontandnextFlag.append([a,b])
                            else:
                                self.removeCellWidget(a,b)
                                celltext = celltext.replace("<br>", "\n")
                                self.setItem(a,b,QTableWidgetItem(celltext))
                        else:
                            celltext = self.cellWidget(a,b).text()
                            celltext = celltext.replace("<br>", "\n")
                            self.removeCellWidget(a,b)
                            self.setItem(a,b,QTableWidgetItem(celltext))
                    elif isinstance(type(self.item(a, b)), type(QTableWidgetItem)):
                        if findtext in self.item(a,b).text():
                            celltext = self.item(a,b).text().replace("\n","<br>")
                            celltext = self.setStrkeyColor(celltext,findtext)
                            lab = QLabel(celltext,self)
                            self.setCellWidget(a,b,lab)
                            self.setItem(a,b,QTableWidgetItem(""))
                            self.frontandnextFlag.append([a, b])
                            # print(a,b,type(self.cellWidget(a,b)),type(self.item(a,b)),"\n",lab.text())
                        else:
                            pass
                    else:
                        pass

    def setStrkeyColor(self,strdata,key):
        needstr = strdata.replace(key,"<font style='background-color:red;'>{}</font>".format(key))
        return needstr

    def cancelCssFormat(self,strdata):
        return self.pat.search(strdata).group(1)

    def stecellbackcolor(self,a,b,color=QColor(200,200,200)):
        self.item(a,b).setBackground(QColor(color))

    def searchboxclo(self):
        self.searchtextbox.clear()
        self.searchbox.close()

    def frontandnextpress(self,k):
        global pressFlag
        pressFlag += k
        if pressFlag >= 0 and pressFlag < len(self.frontandnextFlag):
            self.setCurrentCell(self.frontandnextFlag[pressFlag][0],self.frontandnextFlag[pressFlag][1])
        else:
            pressFlag = -1

class NetworkLabel(QLabel):
    def  __init__(self):
        super().__init__()
        self.setGeometry(200,200,500,20)
        self.mainlayout     =   QHBoxLayout()
        self.titlelayout    =   QHBoxLayout()
        self.btngroup       =   QButtonGroup()
        self.setObjectName("mian")
        self.mainlayout.setContentsMargins(0,0,0,0)
        self.mainlayout.setSpacing(0)
        self.setLayout(self.mainlayout)
        #设置要末端要添加Frame的label数量
        self.labelnum       =   10
        #label数量
        self.num            =   0
        #label自增值，不自减
        self.labelnum_increase = 0
        #设置主label和close按钮触发事件
        self.labelclicked_method   =   None
        self.clobtnclicked_method  =   None
        #标签变量储存信息
        self.labeldict      =   {}
        self.labellist      =   []
        #样式颜色设置
        self.toplabcolor    =   "#E7EAED"
        self.labcolor       =   "transparent"
        self.labcheckcolor  =   "#F1F3F4"
        self.labhovercolor  =   "#FFFFFF"
        self.clobtnhovcolor =   "#E7EAED"
        self.setStyleSheet(self.style)

    def _add_layout(self):
        for s in self.children():
            if isinstance(s,QFrame):
                self.mainlayout.removeWidget(s)
        self.mainlayout.addWidget(self.labeldict[self.labellist[-1]]["widget"],1)
        if self.num < self.labelnum:
            self.mainlayout.addWidget(QFrame(self),self.labelnum-self.num)

    def addtitle(self,text,title_objname = None,clobtn_label_content = "x"):
        title   =   QPushButton(self)
        layout  =   QHBoxLayout()
        title.setMinimumSize(20,20)
        title.setMaximumSize(500,100)
        title.setCheckable(True)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        lab1    =   QLabel(u"{}".format(text),title)
        if isinstance(clobtn_label_content,str):
            clobtn  =   QPushButton(clobtn_label_content,title)
        else:
            clobtn = QPushButton(clobtn_label_content,"", title)
        clobtn.setObjectName("clobtn" + str(self.labelnum_increase))
        clobtn.setMinimumSize(5,5)
        clobtn.setMaximumSize(10,10)
        clobtn.setHidden(True)
        layout.addWidget(lab1,4)
        layout.addWidget(clobtn,1)
        title.setLayout(layout)
        if title_objname:
            title.setObjectName(title_objname)
        else:
            title_objname   =   "label" + str(self.num)
            title.setObjectName(title_objname)

        title.clicked.connect(self.show_clobtn)
        if self.labelclicked_method:
            title.clicked.connect(self.labelclicked_method)

        clobtn.clicked.connect(self.clobtn_click)
        if self.clobtnclicked_method:
            clobtn.clicked.connect(self.clobtnclicked_method)
        self.btngroup.addButton(title,self.labelnum_increase)
        self.labellist.append(title_objname)
        self.labeldict[title_objname] = {"widget":title,"text":text,"closebtn":clobtn}
        self.labelnum_increase += 1
        self.num        +=  1
        self._add_layout()

    def show_clobtn(self):
        for s in self.labeldict.keys():
            for d in self.labeldict[s]["widget"].children():
                if isinstance(d,QPushButton):
                    d.setHidden(True)
        for k in self.sender().children():
            if isinstance(k,QPushButton):
                k.setHidden(False)
        self.setStyleSheet(self.style)

    def clobtn_click(self):
        self.sender().parent().close()
        del self.labeldict[self.sender().parent().objectName()]
        del self.labellist[self.labellist.index(self.sender().parent().objectName())]
        self.num -= 1
        for s in self.children():
            if isinstance(s,QFrame):
                self.mainlayout.removeWidget(s)
        if self.num < self.labelnum:
            self.mainlayout.addWidget(QFrame(self),self.labelnum-self.num)



    @property
    def style(self):
        return f'''
                QLabel#main{{
                    background-color:{self.toplabcolor};
                }}
                QPushButton{{
                    background-color:{self.labcolor};
                    border-style:none;
                }}
                QPushButton:hover{{
                    background-color:{self.labhovercolor};
                    border-top-left-radius:5px;
                    border-top-right-radius:5px;
                }}
                QPushButton:checked{{
                    background-color:{self.labcheckcolor};
                    border-top-left-radius:5px;
                    border-top-right-radius:5px;
                    border:none;
                }}
                QPushButton > QPushButton{{
                    border-radius:5px;
                    border:none;
                }}
                QPushButton > QPushButton:hover{{
                    background-color:{self.clobtnhovcolor};
                    border:none;
                }}
        '''


class GetElasticsearchData():
    body  = None
    index = None
    __indexlist = None
    es    = "https://elk.vesync.com:9200"
    limit = 1000
    starttime = None
    endtime   = None
    __filter  = None
    days      = 7
    sort_     = {"@timestamp": {"order": "asc"}}
    __total   = 1
    url = "https://elk.vesync.com:5601/elasticsearch/_msearch"

    @classmethod
    def getalldata(cls):
        try:
            pass
            # payload = '{"index":"cloud-appserver-new-*","ignore_unavailable":"true","timeout":30000,"preference":1617326406859}\n' \
            #           '{"version":"true","size":{},"sort":[{"@timestamp":{"order":"desc","unmapped_type":"boolean"}}],' \
            #           '"_source":{"excludes":[]},"aggs":{"2":{"date_histogram":{"field":"@timestamp","interval":"30s","time_zone":"UTC","min_doc_count":1}}},' \
            #           '"stored_fields":["*"],' \
            #           '"script_fields":{},' \
            #           '"docvalue_fields":["@timestamp"],' \
            #           'query:{}'.format(cls.limit,cls.body["query"])
            # payloads = payload + "\n"
            # rsp = requests.post(url=url, headers=headers, data=payloads).json()
            # return rsp["responses"][0]
        except Exception as elasticsearchErr:
            raise
            logging.warning(f"getalldata_err:{elasticsearchErr}")

    @classmethod
    def get_data_by_yield(cls):
        cls.__check()
        while cls.__total:
            try:
                data = cls.getalldata()
                cls.__total =   data["hits"]["total"]
                cls.starttime = data["hits"]["hits"][-1]["_source"]["@timestamp"]
                cls.__setfilter()
                yield data
            except Exception as f:
                raise
                logging.info(f"get_data_by_yield_err:{f}")


    @classmethod
    def __check(cls):
        if isinstance(cls.body,dict):
            cls.body["size"] = cls.limit
            cls.body["sort"] = cls.sort_
        else:
            raise AttributeError("body类型必须为字典类型")
        if not cls.index:
            raise AttributeError("index属性未设置,比如索引为cloud-wifioutlet7a-2021-03-08的index为cloud-wifioutlet7a")
        else:
            cls.endtime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            if not cls.starttime:
                cls.__indexlist =   getsearchindex(cls.index,days=cls.days)
                cls.starttime   =   (datetime.strptime(cls.endtime,"%Y-%m-%dT%H:%M:%S") - timedelta(days=cls.days)).strftime("%Y-%m-%dT%H:%M:%S")
            else:
                cls.days        =   (datetime.utcnow() - datetime.strptime(cls.starttime,"%Y-%m-%dT%H:%M:%S")).days
                cls.__indexlist =   getsearchindex(cls.index,cls.days)
        cls.__setfilter()


    @classmethod
    def __setfilter(cls):
        cls.__filter = {"range": {"@timestamp": {"gt": f"{cls.starttime}", "lte": f"{cls.endtime}"}}}
        if "query" in cls.body.keys():
            if "bool" in cls.body["query"].keys():
                cls.body["query"]["bool"]["filter"] = cls.__filter
            else:
                cls.body["query"]["bool"] = {"filter": cls.__filter}

class GetOpsData():
    def __new__(cls, userid):
        cls.userid=userid
        return super().__new__(cls)
    @classmethod
    def getdata(cls):
        url="http://ops.vesync.com:8000/api/getUserInfo?uid={}&envValue=prd".format(cls.userid)
        cookie={"csrftoken":"6xRludy3Ptn4p2Kxk775JAN8xFqKRS7SSwgsDZ1NX8a95qiYawbbVoj6IgrqjLfx", "sessionid":"gtq9q1iux068y61k20kdx8szre9010an"}
        header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        rsp=requests.get(url,cookies=cookie,headers=header).json()
        return rsp
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
        self.movie = QMovie("./pic/loading.gif")
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

'''
将字典键解析成a.b.c格式，或者a.b.c解析成对应字典的值
'''
class UsefulMethod():
    def __init__(self):
        pass
    '''
    提取字典的所有键值为a.b.c格式,返回iterable
    '''
    @classmethod
    def getMainkeyAndSonkey(cls, d, sk="", s=[]):
        print(type(d),d)
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
    '''
    访问dictdata的["a","b","c"]元素
    '''
    @classmethod
    def parseindex(cls,dictdata,a):
        try:
            for s in a:
                if len(a) ==0:
                    pass
                elif len(a) == 1:
                    yield dictdata[a[0]]
                else:
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

class JSONEncoder(json.JSONEncoder):
    """处理ObjectId,该类型无法转为json"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)

class DictAndStrTransfer():
    indexlist = []
    globalvars = []

    @classmethod
    def transfer_to_index(cls, data, index="",lock = None):
        if isinstance(data, str):
            if data.startswith("{"):
                data = cls.transfertodict(data)
        if isinstance(data, dict):
            for d, k in data.items():
                if index == "":
                    index = d
                else:
                    index = index + "." + d
                cls.transfer_to_index(k, index)
                index = index.split(".")
                if len(index) == 1:
                    index = ""
                else:
                    index = ".".join(index[:-1])
        elif isinstance(data,list):
            for s in data:
                cls.transfer_to_index(s,index)
        else:
            if index not in cls.indexlist:
                if lock:
                    lock.acquire()
                    cls.addindex(index)
                    lock.release()
                else:
                    cls.addindex(index)
        # logging.debug("\ntransfer_to_index_indexlist:{}".format(cls.indexlist))

    @classmethod
    def addindex(cls,index):
        cls.indexlist.append(index)

    @classmethod
    def transfertodict(cls, data):
        try:
            return json.loads(json.loads(json.dumps(data)))
        except Exception as k:
            #mongo日志处理方法（使用JSONEncoder处理json中的对象）
            detail = JSONEncoder().encode(data)
            detail = json.loads(detail)
            if isinstance(detail,str):
                return eval(detail)
            else:
                return detail

    @classmethod
    def transfer_index_to_indexlist(cls, index):
        return index.split(".")

    @classmethod
    def get_data_byindex(cls, data:[dict,], indexlist:[list,str]):
        if isinstance(indexlist,str):
            indexlist   =   indexlist.split(".")
        if len(indexlist) != 0:
            if isinstance(data, str):
                if data.startswith("{") or data.startswith("\'{") or data.startswith("\"{"):
                    data = cls.transfertodict(data)
                    # logging.debug("get_data_byindex-data:{}".format(data))
                else:
                    pass
            if isinstance(data, dict):
                #判断该索引是否存在通配符，如果存在，匹配该索引
                rs = None
                if "*" in indexlist[0]:
                    for d in data.keys():
                        rs = re.search(indexlist[0], d)
                        if rs:
                            rs = d
                            break
                    if not rs:
                        rs = indexlist[0]
                else:
                    rs = indexlist[0]
                logging.debug("rs:{}".format(rs))
                try:
                    return cls.get_data_byindex(data[rs], indexlist[1:])
                except KeyError:
                    return ""
                except IndexError:
                    return str(data[rs])
            elif isinstance(data, list):
                s = ""
                for k in data:
                    s += cls.get_data_byindex(k, indexlist) +"\n"
                s = s[:-1]
                return s
            else:
                logging.debug("else_data:{}".format(data))
                return ""
        else:
            logging.debug("data:{}".format(data))
            return str(data)
        # else:
        #     return ""

    @classmethod
    def get_globalvars(cls):
        return cls.globalvars

    @classmethod
    def get_indexlist(cls):
        return cls.indexlist

    @classmethod
    def clear_indexlist(cls):
        cls.indexlist.clear()

    @classmethod
    def clear_globalvars(cls):
        cls.globalvars.clear()

class Body():
    def __set__(self, instance, value):
        instance.__dict__["body"] = value
        instance.starttime = None


class Elasticsearch_5601():

    headers =   {"authorization": "Basic dHM6dkkxY1NhMA==",
               "kbn-version": "6.4.0",
               "content-type": "application/x-ndjson",
               "accept": "application/json, text/plain, */*",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    limit = 1000
    def __init__(self,body,index="cloud-appserver-new",days = 7,range_="@timestamp",
                 url = "https://elk.vesync.com:5601/elasticsearch/_msearch",sort = {"@timestamp": {"order": "desc"}}):
        self.body   =   body
        self.index  =   index
        self.days   =   days
        self.range_ =   range_
        self.url    =   url
        self.sort_  =   sort
        self.starttime = None
        self.endtime   = None
        self.fronttime = [] #记录每页最终时间
        self.nexttime  = None
        self.__check()
        self.__setpayloads()

    def set_body(self,body):
        self.body = body
        self.__clear()

    def set_days(self,days):
        self.days   =   days
        self.__clear()

    def __clear(self):
        self.starttime = None
        self.endtime = None
        self.fronttime.clear()
        self.nexttime = None
        self.__check()
        self.__setpayloads()

    def getdata(self):
        self.__check()
        self.__setpayloads()
        # logging.debug(f"Elasticsearch_5601-getdata-payloads:{repr(self.payloads)}")
        self.rsp = requests.post(url=self.url, headers=self.headers, data=self.payloads).json()
        # logging.debug(f"Elasticsearch_5601-getdata-rsp:{rsp}")

        try:
            self.nexttime = self.__to_timestamp(datetime.strptime
                                             (self.rsp["responses"][0]["hits"]["hits"][-1]["_source"][self.range_],
                                              "%Y-%m-%dT%H:%M:%S.%fZ"))
        except:
            raise
        print(f"nexttime:{self.nexttime}")
        return self.rsp["responses"][0]

    def next_(self):
        self.fronttime.append(self.__to_timestamp(datetime.strptime
                     (self.rsp["responses"][0]["hits"]["hits"][0]["_source"][self.range_],"%Y-%m-%dT%H:%M:%S.%fZ")))
        self.endtime = self.nexttime
        print(f"self.fronttime:{self.fronttime}")
        return self.getdata()

    def front_(self):
        try:
            self.endtime = self.fronttime[-1]
            del self.fronttime[-1]
        except:
            pass
        print(f"self.fronttime:{self.fronttime}")
        return self.getdata()

    def get_data_yield(self):
        self.__check()
        self.__setpayloads()
        while self.total:
            rsp = requests.post(url=self.url, headers=self.headers, data=self.payloads).json()
            yield rsp["responses"][0]
            try:
                self.total   =   rsp["responses"][0]["hits"]["total"]
                self.endtime =  self.__to_timestamp(datetime.strptime
                              (rsp["responses"][0]["hits"]["hits"][-1]["_source"][self.range_],"%Y-%m-%dT%H:%M:%S.%fZ"))
                self.__setfilter()
                self.__setpayloads()
            except:
                self

    def __setpayloads(self):
        payload0    =   {"index":"%s-*"%self.index,"ignore_unavailable":"true","timeout":30000}
        payload1    =   {"version":"true",
                         "size":self.limit,
                         "sort":[self.sort_],
                         "_source":{
                            "excludes":[]},
                            "aggs":{
                                "2":{
                                    "date_histogram":{
                                        "field":"@timestamp",
                                        "interval":"30s",
                                        "time_zone":"UTC",
                                        "min_doc_count":1
                                    }
                                }
                            },
                            "stored_fields":["*"],
                            "docvalue_fields":["@timestamp"],
                            "query":self.body["query"]
                         }
        self.payloads    =   json.dumps(payload0)+"\n"+json.dumps(payload1)+"\n"

    def __check(self):
        if not isinstance(self.body,dict):
            raise AttributeError("body类型必须为字典类型")
        if not self.index:
            raise AttributeError("index属性未设置,比如索引为cloud-wifioutlet7a-2021-03-08的index为cloud-wifioutlet7a")
        else:
            if self.starttime and self.endtime:
                self.starttime   =   self.__to_timestamp(self.starttime)
                self.endtime     =   self.__to_timestamp(self.endtime)
            if not self.endtime:
                self.endtime     =   self.__to_timestamp(datetime.utcnow())
            if not self.starttime:
                self.starttime   =   self.__to_timestamp(datetime.utcnow() - timedelta(days=self.days))
        self.__setfilter()

    def __setfilter(self):
        self.__filter = {"range":{f"{self.range_}": {"gt": self.starttime, "lte": self.endtime}}}
        if "query" in self.body.keys():
            if "bool" in self.body["query"].keys():
                if "must" in self.body["query"]["bool"].keys():
                    if isinstance(self.body["query"]["bool"]["must"],dict):
                        a = self.body["query"]["bool"]["must"]
                        self.body["query"]["bool"]["must"] = [a,self.__filter]
                    else:
                        if "range" in self.body["query"]["bool"]["must"][-1].keys():
                            self.body["query"]["bool"]["must"][-1] = self.__filter
                        else:
                            self.body["query"]["bool"]["must"].append(self.__filter)
                else:
                    self.body["query"]["bool"]["must"] = self.__filter
            else:
                self.body["query"]["bool"] = {"must":self.__filter}
        else:
            raise AttributeError("body 格式错误")
        self.__deal_body()

    def __to_timestamp(self,time_):
        if isinstance(time_,str):
            try:
                return int(datetime.timestamp(datetime.strptime(time_, "%Y-%m-%dT%H:%M:%S")) * 1000)
            except:
                raise

        elif isinstance(time_,datetime):
            return int(datetime.timestamp(time_)*1000)

        elif isinstance(time_,int):
            return time_
        else:
            raise   ValueError(f"starttime or endtime should be string or datetime or int type-time_:{type(time_)}")

    def __deal_body(self):
        if "size" in self.body["query"].keys():
            self.limit   =   self.body["query"]["size"]
            del self.body["query"]["size"]
        if "from" in self.body["query"].keys():
            del self.body["query"]["from"]
        if "sort" in self.body["query"].keys():
            self.sort_   =   self.body["query"]["sort"]
            del self.body["query"]["sort"]
        logging.debug(f"Elasticsearch_5601-__deal_body-body:{self.body}")

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # s = TempleteWindow()
    # s.set_title("测试查询")
    # s.show()
    # # s.showwindinw()
    # app.exec_()
    # DictAndStrTransfer.get_data_byindex()
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "request.data": "upschedule"
                        }
                    },
                    {
                        "match": {
                            "request.context.method": "bypassV2"
                        }
                    }
                ]
            }
        }
    }
    s = Elasticsearch_5601(body)

    # Elasticsearch_5601.getdata()
    # print(Elasticsearch_5601.endtime)
    # Elasticsearch_5601.getdata()
    # print(Elasticsearch_5601.endtime)
    # Elasticsearch_5601.getdata()
    # print(Elasticsearch_5601.endtime)
    for x in s.getdata()["hits"]["hits"]:
        print(x)
    for y in s.next_()["hits"]["hits"]:
        print(y)
    for z in s.next_()["hits"]["hits"]:
        print(z)
    for a in s.front_()["hits"]["hits"]:
        print(a)
    for b in s.next_()["hits"]["hits"]:
        print(b)
    for c in s.front_()["hits"]["hits"]:
        print(c)
    # s.getdata()
    # s.next_()
    # s.next_()
    # s.next_()
    # s.front_()
    # s.front_()
    # s.front_()
    #
