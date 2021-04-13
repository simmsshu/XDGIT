# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,\
    QLabel,QLineEdit,QTableWidget,QTableWidgetItem,QAbstractItemView,QApplication
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import Qt
from initstate_data import MyClass
from Onoffline1 import MyClass1
from kibana_7A import Kibana_7Alog
from datetime import datetime

app = QApplication(sys.argv)
class OnOffLine(QWidget): #离线日志显示类

    def __init__(self):
        super().__init__()
        self.table=QTableWidget(self)
        self.total_data = QLabel(self)
        self.size=500
        self.fromsize=0
        self.frontAndnNextClickCount=0
        self.btnstatus=0  #点击的按钮获取
        self.totallogs=0
        self.dealdatatime=datetime.now()
        self.table1=QLabel(self)
        self.OnOffline()
 #h获取查询到的日志总数
    def OnOffline(self):

        self.setWindowIcon(QIcon("./pic/kibana.png"))
        self.setWindowTitle("掉线日志")
        intch=app.desktop()#设置窗体位置
        self.setGeometry(intch.width()/ 2-80 , intch.height()/2-self.height(),1000,900)
        lab=QLabel("CID",self)
        fon1=QFont("宋体",15)
        lab.setFont(fon1)
        self.box=QLineEdit()
        self.btn1 = QPushButton("重连日志", self)
        self.btn2 = QPushButton("掉线详情", self)
        self.btn3 = QPushButton("7A重连日志", self)
        self.btn31=QPushButton("7A掉线重连",self)
        self.btn4=QPushButton("上一页", self)
        self.btn5=QPushButton("下一页",self)

        self.btn4.setGeometry(self.width()/2-60,self.height()-30,40,20)
        self.btn5.setGeometry(self.width()/2+10,self.height()-30,40,20)
        self.table1.setGeometry(self.width()/2+60,self.height()-30,40,20)
        self.table1.setText("第 1 页")
        level=QHBoxLayout(self)
        level.addWidget(lab,0,Qt.AlignVCenter | Qt.AlignTop)
        level.addWidget(self.box,0,Qt.AlignVCenter | Qt.AlignTop)
        level.addWidget(self.btn1,0,Qt.AlignVCenter | Qt.AlignTop)
        level.addWidget(self.btn2,0,Qt.AlignVCenter | Qt.AlignTop)
        level.addWidget(self.btn3,0,Qt.AlignVCenter | Qt.AlignTop)
        level.addWidget(self.btn31, 0, Qt.AlignVCenter | Qt.AlignTop)
        self.btn1.clicked.connect(self.from_CID_search_data)
        self.btn2.clicked.connect(self.from_CID_search_detaildata)
        self.btn3.clicked.connect(self.from_CID_search_7AReconnection)
        self.btn31.clicked.connect(self.from_CID_search_7AReconnectionAndOffline)
        self.btn4.clicked.connect(self.setSizeandFrom)
        self.btn5.clicked.connect(self.setSizeandFrom)

        self.show()
    def setSizeandFrom(self):

        sinalFrom=self.sender()
        if sinalFrom.text()=="下一页" and self.frontAndnNextClickCount <=0:
            self.frontAndnNextClickCount=1
            self.fromsize=self.fromsize+self.size+1
        elif sinalFrom.text()=="上一页" and self.frontAndnNextClickCount ==0:
            self.frontAndnNextClickCount=-1
        elif sinalFrom.text()=="上一页" and self.frontAndnNextClickCount ==1:
            self.frontAndnNextClickCount = self.frontAndnNextClickCount -1
            self.fromsize = self.fromsize - self.size-1
        elif sinalFrom.text()=="下一页" and self.frontAndnNextClickCount >=1:
            self.frontAndnNextClickCount = self.frontAndnNextClickCount + 1
            self.fromsize = self.fromsize + self.size
        elif sinalFrom.text()=="上一页" and self.frontAndnNextClickCount >1:
            self.frontAndnNextClickCount = self.frontAndnNextClickCount -1
            self.fromsize = self.fromsize - self.size
        else:
            pass
        print(self.frontAndnNextClickCount)
        if self.frontAndnNextClickCount>=0:
            print(self.btnstatus,self.totallogs,self.fromsize,self.frontAndnNextClickCount)
            if self.btnstatus == 1 and self.totallogs >= 500 and self.fromsize <= self.totallogs:
                self._frontandnext_initstate()
                self.table1.setText("第 {} 页".format(int(self.fromsize / 500) + 1))
            elif self.btnstatus == 2 and self.totallogs >= 500 and self.fromsize <= self.totallogs:
                self._frontandnext_onofflinedetail()
                self.table1.setText("第 {} 页".format(int(self.fromsize / 500) + 1))
            elif self.btnstatus == 3 and self.totallogs >= 500 and self.fromsize <= self.totallogs:
                self._frontandnext_7Ainitstate()
                self.table1.setText("第 {} 页".format(int(self.fromsize / 500) + 1))
            elif self.btnstatus == 4 and self.totallogs >= 500 and self.fromsize <= self.totallogs:
                self._frontandnext_7AReconnectionAndOffline()
                self.table1.setText("第 {} 页".format(int(self.fromsize / 500) + 1))
            else:
                pass
        else:
            pass

    def _frontandnext_7AReconnectionAndOffline(self):
        cid = self.box.text()
        self.starttime = datetime.now()
        log_7AOnOffline = Kibana_7Alog(cid, days=30,searchflag="body2" ,fromsize=self.fromsize, size=self.size)
        self.getdatatime = datetime.now()
        self.totallogs = log_7AOnOffline.gettotallogs()
        flags = 4  # 判断按钮确定后续函数调用的函数以及显示数据
        self.show_detail_data(log_7AOnOffline, flags)
        self.show_total_detai7Ainitstate(log_7AOnOffline)

    def _frontandnext_7Ainitstate(self):
        cid = self.box.text()
        self.starttime = datetime.now()
        log_7Ainitstate = Kibana_7Alog(cid, days=30, fromsize=self.fromsize, size=self.size)
        self.getdatatime = datetime.now()
        flags = 3
        self.totallogs = log_7Ainitstate.gettotallogs()
        # self.show_total_detaiOffline(self.onofflinedetaldata)
        self.show_detail_data(log_7Ainitstate, flags)

    def _frontandnext_initstate(self):
        cid = self.box.text()
        self.starttime = datetime.now()
        onofflinedata = MyClass(cid, 15, self.fromsize, self.size)
        self.getdatatime = datetime.now()
        flags=1
        # self.btnstatus=1
        self.show_total_Data(onofflinedata)
        self.show_detail_data(onofflinedata,flags)

    def _frontandnext_onofflinedetail(self):
        cid=self.box.text()
        self.starttime = datetime.now()
        onofflinedetaldata = MyClass1(cid, 15,self.fromsize,self.size)
        self.getdatatime = datetime.now()
        self.totallogs=onofflinedetaldata.get_total_logs()
        flags=2 #判断按钮确定后续函数调用的函数以及显示数据
        # self.btnstatus=2  #获取当前点击查询按钮状态
        self.show_total_detaiOffline(onofflinedetaldata)
        self.show_detail_data(onofflinedetaldata,flags)

    def from_CID_search_7AReconnectionAndOffline(self):
        cid = self.box.text()
        self.starttime = datetime.now()
        print("开始时间:" + self.starttime.__str__())
        self.fromsize = 0
        self.table1.setText("第 {} 页".format(int(1)))
        self.frontAndnNextClickCount = 0
        log_7AOnOffline = Kibana_7Alog(cid, days=30,searchflag="body2" ,fromsize=self.fromsize, size=self.size)
        self.getdatatime = datetime.now()
        print("获取数据时间:" + self.getdatatime.__str__())
        self.totallogs = log_7AOnOffline.gettotallogs()
        flags = 4  # 判断按钮确定后续函数调用的函数以及显示数据
        self.btnstatus = 4  # 定义当前点击查询按钮状态
        self.show_detail_data(log_7AOnOffline, flags)
        self.show_total_detai7Ainitstate(log_7AOnOffline)

    def from_CID_search_7AReconnection(self):
        cid = self.box.text()
        self.starttime = datetime.now()
        print("开始时间:" + self.starttime.__str__())
        self.fromsize = 0
        self.table1.setText("第 {} 页".format(int(1)))
        self.frontAndnNextClickCount=0
        log_7Ainitstate = Kibana_7Alog(cid,days=30,fromsize=self.fromsize,size=self.size)
        self.getdatatime = datetime.now()
        print("获取数据时间:" + self.getdatatime.__str__())
        self.totallogs = log_7Ainitstate.gettotallogs()
        flags = 3  # 判断按钮确定后续函数调用的函数以及显示数据
        self.btnstatus = 3  # 获取当前点击查询按钮状态
        self.show_detail_data(log_7Ainitstate, flags)
        self.show_total_detai7Ainitstate(log_7Ainitstate)

    def from_CID_search_detaildata(self):
        cid=self.box.text()
        self.starttime=datetime.now()
        print("开始时间:" + self.starttime.__str__())
        self.fromsize=0
        self.table1.setText("第 {} 页".format(int(1)))
        self.frontAndnNextClickCount = 0
        self.onofflinedetaldata = MyClass1(cid, 30,self.fromsize,self.size)
        self.getdatatime=datetime.now()
        print("获取数据时间:" + self.getdatatime.__str__())
        self.totallogs=self.onofflinedetaldata.get_total_logs()
        flags=2 #判断按钮确定后续函数调用的函数以及显示数据
        self.btnstatus=2  #获取当前点击查询按钮状态
        self.show_detail_data(self.onofflinedetaldata,flags)
        self.show_total_detaiOffline(self.onofflinedetaldata)
    def from_CID_search_data(self):
        cid=self.box.text()
        self.starttime = datetime.now()
        print("开始时间:" +self.starttime.__str__())
        self.fromsize = 0
        self.table1.setText("第 {} 页".format(int(1)))
        self.frontAndnNextClickCount = 0
        self.onofflinedata = MyClass(cid, 15,self.fromsize, self.size)
        self.getdatatime = datetime.now()
        print("获取数据时间:"+self.getdatatime.__str__())
        self.totallogs = self.onofflinedata.get_total_logs()
        flags=1
        self.btnstatus=1
        self.show_detail_data(self.onofflinedata,flags)
        self.show_total_Data(self.onofflinedata)

    def resizeEvent(self,s):#设置表格随窗体大小改变事件
        self.table.resize(self.width(),self.height()-120)
        self.btn4.move(self.width() / 2 - 60, self.height() - 30)#设置上下页案件随窗体变化居中
        self.btn5.move(self.width() / 2 + 10, self.height() - 30)
        self.table1.move(self.width()/2+60,self.height()-30)
        # event=QResizeEvent()
        # wid=event.size().width()
        # hei=event.size().heigth()
        # print(wid,hei)
    def ananysWhethercolumempty(self,colum):
        count_empty=0
        for i in colum:
            if i =="":
                count_empty = count_empty + 1
            else:
                pass
        if count_empty ==len(colum)-1:
            return True
        else:
            return  False

    def show_detail_data(self,onofflinedata,flags):  #表格的数据显示
        if flags==1:
            alldata = self.all_detail_data(onofflinedata,flags)
        elif flags==2:
            alldata = self.onoffline_all_data(onofflinedata,flags)
        elif flags == 3 or flags == 4:
            alldata = self.kibana_initstateData(onofflinedata,flags)
        self.table.setRowCount(len(alldata[0]) - 1)
        self.table.setColumnCount(len(alldata))
        self.setTablecloumwid(flags)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑属性
        self.table.setGeometry(0,80,self.width(),self.height()-120)
        # self.headerSetting(self.table)
        for i in range(0,len(alldata)):#总列数,显示所有数据
            for j in range(1,len(alldata[0])):#总数据行数
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(alldata[i][0]))
                ss=QTableWidgetItem(alldata[i][j])
                self.table.setItem(j-1,i,ss)
                ss.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter) #设置所有单元格对齐方式
        for i in range(len(alldata)):
            if self.ananysWhethercolumempty(alldata[i]) :
                self.table.setColumnHidden(i,True)
            else:
                self.table.setColumnHidden(i, False)
        else :
            pass
        self.dealdatatime = datetime.now()
        # print("处理完成时间:" +self.dealdatatime.__str__())
        # print(str((self.getdatatime-self.starttime).seconds))
        # print(str((self.achivedealdatatime - self.getdatatime).seconds))
        # print(str((self.dealdatatime-self.getdatatime).seconds))

    def setTablecloumwid(self,flags):
        if flags == 1 :
            self.table.setColumnWidth(0, 200)
            self.table.setColumnWidth(1, 100)
            self.table.setColumnWidth(2, 120)
            self.table.setColumnWidth(3, 100)
            self.table.setColumnWidth(4, 70)
            self.table.setColumnWidth(5, 50)
            self.table.setColumnWidth(6, 120)
            self.table.setColumnWidth(7, 200)
        if flags == 2 :
            self.table.setColumnWidth(0, 200)
            self.table.setColumnWidth(1, 100)
            self.table.setColumnWidth(2, 120)
            self.table.setColumnWidth(3, 70)
            self.table.setColumnWidth(4, 150)
            self.table.setColumnWidth(5, 200)
        if flags == 3 or flags == 4:
            self.table.setColumnWidth(0, 200)
            self.table.setColumnWidth(1, 70)
            self.table.setColumnWidth(2, 100)
            self.table.setColumnWidth(3, 80)
            self.table.setColumnWidth(4, 100)
            self.table.setColumnWidth(5, 50)
            self.table.setColumnWidth(6, 130)
            self.table.setColumnWidth(7, 130)
            self.table.setColumnWidth(8,200)

    # def headerSetting(self,table):
    #     columnCount = table.columnCount()
    #     table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#设置表格内容自动缩进
    #     table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)#设置某列随内容自动调整行宽
    #     table.horizontalHeader().setSectionResizeMode(columnCount-1, QHeaderView.ResizeToContents)
    #     table.horizontalHeader().setSectionResizeMode(columnCount-2, QHeaderView.ResizeToContents)
    #     table.horizontalHeader().setSectionResizeMode(columnCount-3, QHeaderView.ResizeToContents)
    #
    #     table.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置表格不可编辑属性
    #     table.setColumnWidth(0,200)
    #     table.setColumnWidth(1,100)
    #     table.setColumnWidth(2,130)
    #     table.setColumnWidth(3,60)
    #     table.setColumnWidth(4,150)
    #     table.setColumnWidth(5,200)

    def show_total_detai7Ainitstate(self,onofflinedata):
        self.total_data.setText("总计日志:"+str(self.totallogs)+",网络重连："+str(onofflinedata.getcount_network())\
               +",wifi重连："+str(onofflinedata.getcount_wifi())+",PowerOn重连："+str(onofflinedata.getcount_poweron())\
               +",ConfigNet重连:"+str(onofflinedata.getcount_confignet())+",获取数据耗时:"+str((self.getdatatime-self.starttime).seconds)+"\n"\
                +"处理数据时间:"+str((self.dealdatatime-self.getdatatime).seconds)+"\t"+"CID:"+onofflinedata.getcid())
        self.total_data.setGeometry(20,40,800,45)

    def show_total_Data(self,onofflinedata): #设置标签显示内容
        self.total_data.setText("总计日志:"+str(onofflinedata.get_total_logs())+",网络重连："+str(onofflinedata.get_count_Network())\
               +",wifi重连："+str(onofflinedata.get_count_Wifi())+",PowerOn重连："+str(onofflinedata.get_count_PowerOn())\
               +",ConfigNet重连:"+str(onofflinedata.get_count_ConfigNet())+"获取数据耗时:"+str((self.getdatatime-self.starttime).seconds)+"\n"\
                +"处理数据时间:"+str((self.dealdatatime-self.getdatatime).seconds))
        self.total_data.setGeometry(20,40,800,45)
    def show_total_detaiOffline(self,onofflinedata):
        self.total_data.setText("总计日志:"+str(onofflinedata.get_total_logs())+",网络重连："+str(onofflinedata.get_count_Network())\
               +",wifi重连："+str(onofflinedata.get_count_Wifi())+",PowerOn重连："+str(onofflinedata.get_count_PowerOn())\
               +",ConfigNet重连:"+str(onofflinedata.get_count_ConfigNet())+"获取数据耗时:"+str((self.getdatatime-self.starttime).seconds)+"\n"\
                +"处理数据时间:"+str((self.dealdatatime-self.getdatatime).seconds))
        self.total_data.setGeometry(20,40,800,45)

    # def reconnect_arvtime(self):
    #     for i in self.onofflinedetaldata.get_onofflinealldata():
    #         if i != "":
    #             offlinetime=datetime.timestamp()

    def all_detail_data(self,onofflinedata,flags):
        all_data=[]
        all_data.append(onofflinedata.get_T())
        # all_data.append(onofflinedata.get_second())
        # all_data.append(onofflinedata.get_accurate())
        all_data.append(onofflinedata.get_onoffline())
        all_data.append(onofflinedata.get_routermac())
        all_data.append(onofflinedata.get_wifiName())
        all_data.append(onofflinedata.get_firmVersion())
        all_data.append(onofflinedata.get_mcuVersion())
        all_data.append(onofflinedata.get_RSSI())
        all_data.append(onofflinedata.get_retry())
        all_data.append(onofflinedata.get_host_name())
        all_data.append(onofflinedata.get_fimuploadofftime())
        return all_data
    def onoffline_all_data(self,total_onoffline,flags):
        all_data=[]
        all_data.append(total_onoffline.get_T())
        # all_data.append(onofflinedata.get_second())
        # all_data.append(onofflinedata.get_accurate())
        all_data.append(total_onoffline.get_onoffline())
        all_data.append(total_onoffline.get_routermac())
        all_data.append(total_onoffline.get_RSSI())
        all_data.append(total_onoffline.get_retry())
        all_data.append(total_onoffline.get_host_name())
        all_data.append(total_onoffline.get_onofflinealldata())
        return all_data
    def kibana_initstateData(self,initstateData,flags):
        all_data=[]
        all_data.append(initstateData.getT())
        all_data.append(initstateData.getaccountid())
        all_data.append(initstateData.getdeviceName())
        all_data.append(initstateData.getfirmVersion())
        all_data.append(initstateData.getinitState())
        all_data.append(initstateData.getRSSI())
        all_data.append(initstateData.getmac())
        all_data.append(initstateData.getwifiName())
        all_data.append(initstateData.getH())
        if flags == 4:
            all_data.append(initstateData.getseonfflinetotaltime())
        return all_data

