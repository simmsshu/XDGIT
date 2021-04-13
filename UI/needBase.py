from PyQt5.QtWidgets import QTableWidget,QFrame,QLineEdit,QPushButton,QTextEdit,QAbstractItemView,QTableWidgetItem,\
    QApplication,QWidget,QLabel
from PyQt5.Qt import QColor,QIcon,QFont,QPoint
from PyQt5.QtCore import Qt,pyqtSignal
from configparser import RawConfigParser
from bson import objectid,ObjectId
from datetime import datetime,timedelta
import importlib
import pymongo
import pymysql
import requests
import re
import json
import logging
logging.basicConfig(level=logging.INFO)
PIC_BASE_DIR = "./SOURCES/pic/"
CONFIG = RawConfigParser()
CONFIG.read("config.ini")
def get_current_screen_desktop():
    return QApplication.desktop().screen(QApplication.desktop().screenNumber())

class  Mongodb_connect(object):
    def __init__(self,config):
        self.data = []
        self.__username = config.get("mongo","username")
        self.__pwd=config.get("mongo","pwd")
        self.__host=config.get("mongo","host")
        self.__port=config.get("mongo","port")
        self.__dbname=config.get("mongo","dbname")
        self.__database=config.get("mongo","database")
        self.__uri="mongodb://{}:{}@{}:{}/{}?authMechanism=SCRAM-SHA-1".format(self.__username,self.__pwd,self.__host,self.__port,self.__dbname)
        self.__connect_mongodb()

    def __connect_mongodb(self,collection="setup_log"):
        self.__client=pymongo.MongoClient(self.__uri)
        self.cursor = self.__client[self.__database][collection]

    def get_data(self,arg):
        return self.cursor.find(arg,no_cursor_timeout = True)

    def get_count(self,arg):
        return self.cursor.find(arg).count()

    def close(self):
        self.__client.close()

class MongoConfigDetailInfo():

    @classmethod
    def set_cofnig(cls,config):
        cls.host = config.get("mysql","host")
        cls.user = config.get("mysql","user")
        cls.password = config.get("mysql","password")
        cls.db = config.get("mysql","db")

    @classmethod
    def connectDB(cls):
        try:
            cls.db = pymysql.connect(host = cls.host,user = cls.user,password= cls.password,db= cls.db)
        except Exception as e:
            logging.info("MongoConfigDetailInfo connection ERR:{}".format(e))
        return cls.db

    @classmethod
    def close(cls):
        cls.db.close()

    @classmethod
    def insert_table_info(cls,table,keys,values):
        '''
        :param table: sring table名称
        :param keys: tuple 元组内元素需为字符串
        :param values: 双重元组数据，且内层元组数据需长度一致
        :return:
        '''
        sql = '''REPLACE INTO {table} {keys} VALUES ()'''.format(table=table, keys=keys)
        sql = cls._set_sql(sql,len(keys))
        logging.debug("执行sql语句:{}".format(sql))
        s = cls.connectDB()
        try:
            s.cursor().executemany(sql,values)
            s.commit()
        except Exception as d:
            logging.info("there is exception in insertdata to mysql,exception:{}".format(str(d)))

    @classmethod
    def get_data_by_sql(cls,sql):

        logging.debug("get_data_by_sql-sql:{}".format(sql))
        s = cls.connectDB()
        s = s.cursor(pymysql.cursors.DictCursor)
        try:
            s.execute(sql)
            k = s.fetchall()
            return k
        except Exception as f:
            logging.info("get_data_by_sql Exception:{},sql:{}".format(str(f),sql))
            pass

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
        self.search.setIcon(QIcon("./SOURCES/pic/search.ico"))
        self.search.setGeometry(210, 0, 30, 30)
        self.search.setStyleSheet("border:none")
        self.search.clicked.connect(self.searchdata)

        self.front  =   QPushButton("",self.searchbox)
        self.front.setIcon(QIcon("./SOURCES/pic/front.ico"))
        self.front.setGeometry(240,0,30,30)
        self.front.setStyleSheet("border:none")
        self.front.clicked.connect(lambda: self.frontandnextpress(-1))

        self.next   =   QPushButton("", self.searchbox)
        self.next.setIcon(QIcon("./SOURCES/pic/next.ico"))
        self.next.setGeometry(270,0,30,30)
        self.next.setStyleSheet("border:none")
        self.next.clicked.connect(lambda: self.frontandnextpress(1))

        self.clo = QPushButton("", self.searchbox)
        self.clo.setIcon(QIcon("./SOURCES/pic/close.ico"))
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
        try:
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
                self.textwindow.setGeometry(0, 0, self.width() - 100, self.height() - 100)
                try:
                    id_ = self.item(self.currentRow(), 0).text()
                    self.textwindow_text = self.get_data(id_)
                    detail = JSONEncoder().encode(self.textwindow_text)
                    detail = json.loads(detail)
                    self.textwindow.setText(json.dumps(detail, indent=5, ensure_ascii=False))
                    self.textwindow.setHidden(False)
                except:
                    detail = JSONEncoder().encode(self.textwindow_text)
                    detail = json.loads(detail)
                    self.textwindow.setText(json.dumps(detail, indent=5, ensure_ascii=False))
                    self.textwindow.setHidden(False)
        except AttributeError:
            pass

    def get_data(self,id_):
        s = Mongodb_connect(CONFIG)
        for d in s.get_data({"_id":ObjectId(f"{id_}")}):
            return d


    def searchdata(self):
        self.frontandnextFlag = []
        global  pressFlag
        pressFlag = -1
        findtext = ""
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

class JSONEncoder(json.JSONEncoder):
    """处理ObjectId,该类型无法转为json"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
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
    def get_data_byindex(cls, data, indexlist):
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
        except IndexError:
            pass
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


class Dict(dict):
    def __missing__(self, key):
        return ""