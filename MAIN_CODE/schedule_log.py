# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QHBoxLayout,\
    QLabel,QLineEdit,QTableWidget,QTableWidgetItem,QAbstractItemView,QApplication
from PyQt5.QtGui import QIcon,QFont,QColor
from PyQt5.QtCore import Qt
# from Vdmp_log import VdmpLog
# from .Onoffline1 import MyClass1
# from .kibana_7A import Kibana_7Alog
from datetime import datetime
# from .kibana_7A import Kibana_7Alog

class ScheduleLog(QWidget):
    def __init__(self,parent= None):
        super().__init__()
        self.table = QTableWidget(self)
        self.list=[] #存储变色数据所在行号
        if parent:
            self.setParent(parent)
        self.scheduleLogShow()

    def scheduleLogShow(self):
        self.setWindowTitle("Schedule日志")
        self.setWindowIcon(QIcon("./pic/kibana.png"))
        self.setGeometry(20,80,1330,900)
        self.lab1=QLabel("CID",self)
        lab1Font=QFont("宋体",15)
        self.lab1.setFont(lab1Font)
        self.box1=QLineEdit()
        self.btn1=QPushButton("7Aschedule",self)
        self.btn2 = QPushButton("显示隐藏", self)
        self.btn3 = QPushButton("VdmpSchedule")
        self.btn2.move(0, 35)
        self.btn2.setVisible(False)
        Hlevel=QHBoxLayout(self)
        Hlevel.addWidget(self.lab1,0,Qt.AlignVCenter | Qt.AlignTop)
        Hlevel.addWidget(self.box1,0,Qt.AlignVCenter | Qt.AlignTop)
        Hlevel.addWidget(self.btn1,0,Qt.AlignVCenter | Qt.AlignTop)
        Hlevel.addWidget(self.btn3, 0, Qt.AlignVCenter | Qt.AlignTop)
        self.table.setGeometry(0, 80, self.width(), self.height() - 100)
        self.btn1.clicked.connect(self._7AScheduleCidLog)
        self.btn2.clicked.connect(self.wetherhiderow)
        self.btn3.clicked.connect(self._VdmpScheduleCidLog)


        self.show()
    def wetherhiderow(self):
            btn2Text=self.btn2.text()
            if btn2Text == "显示隐藏":
                if self.flags == 1:
                    for i in range(self.table.rowCount()):
                        self.table.setRowHidden(i,False)
                elif self.flags == 2:
                    self.table.setColumnHidden(5, False)
                self.btn2.setText("隐藏数据")
            if btn2Text == "隐藏数据":
                if self.flags == 1:
                    self.hiderows(self.flags)
                elif self.flags == 2:
                    self.table.setColumnHidden(5, True)
                self.btn2.setText("显示隐藏")


    def _7AScheduleCidLog(self):
        text1=self.box1.text()
        getCidLog=Kibana_7Alog(CID=text1,searchflag="body3")
        # getNeedData=self.getNeedData(getCidLog)
        self.flags=1
        self.btn2.setVisible(False)
        self.showAllData(getCidLog,self.flags)
    def _VdmpScheduleCidLog(self):
        text1 = self.box1.text().split()[0]
        getCidLog = VdmpLog(CID=text1)
        # getNeedData=self.getNeedData(getCidLog)
        self.flags = 2
        self.btn2.setVisible(True)
        self.showAllData(getCidLog.getAllData(), self.flags)

    def showAllData(self,alllogs,flags):
        if flags == 1:
            alldata = self.get7AScheduleNeedData(alllogs)
            self.table.setRowCount(len(alldata[0]) - 1)
            self.table.setColumnCount(len(alldata))
            # self.setTablecloumwid(flags)
            self.set7Aschedulecolumnwidth()
            # self.headerSetting(self.table)
            for i in range(0, len(alldata)):  # 总列数,显示所有数据
                for j in range(1, len(alldata[0])):  # 总数据行数
                    self.table.setHorizontalHeaderItem(i, QTableWidgetItem(alldata[i][0]))
                    ss = QTableWidgetItem(alldata[i][j])
                    self.table.setItem(j-1, i, ss)
                    ss.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置所有单元格对齐方式
            self.hiderows(flags=flags)
            self.table.cellClicked.connect(self.highlightDifferentAddData)
        elif flags == 2:
            alldata = alllogs
            self.table.setRowCount(len(alldata[0]) - 1)
            self.table.setColumnCount(len(alldata))
            for i in range(0, len(alldata)):  # 总列数,显示所有数据
                for j in range(1, len(alldata[0])):  # 总数据行数
                    self.table.setHorizontalHeaderItem(i, QTableWidgetItem(alldata[i][0]))
                    ss = QTableWidgetItem(alldata[i][j])
                    self.table.setItem(j - 1, i, ss)
                    ss.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 设置所有单元格对齐方式
            self.table.setColumnHidden(5, True)
            self.table.setColumnWidth(0,190)
            self.table.setColumnWidth(1, 77)
            self.table.setColumnWidth(2, 90)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑属性

        # self.table.cellClicked.connect(self.highlightDifferentAddData)


        for s in range(0,self.table.rowCount()):
            if self.table.item(s,1).text() == "设备" and (self.table.item(s,3).text()== "add" or self.table.item(s,3).text() == "del"):
                self.table.setRowHidden(s,True)
        self.hidecolumns(6)
        self.hidecolumns(7)
        self.hidecolumns(8)
        self.hidecolumns(9)
        # for ddd in range(self.table.rowCount()):
        #     print(self.table.item(ddd,8).text())

    def highlightDifferentAddData(self,a,b):
        # print(a,b)
        # print(self.table.item(a,b).text())
        list=[] #存储第6列不为空的行号
        list1=[] #存储第六列不为空，且第5列为add值的行号
        if b == 6 and self.table.item(a,b).text() != "":
            items=self.table.findItems(self.table.item(a,b).text(),Qt.MatchExactly)
            if len(self.list) !=0:
                for s in self.list:
                    self.setTableCellColor(s[0],s[1],255,255,255)
                del self.list[:]
            else:
                pass

            for s in items:
                list.append(s.row())
            for i in range(self.table.rowCount()):
                if i in list:
                    self.setTableCellColor(i,b,200,200,100)
                else:
                    self.setTableCellColor(i,b,255,255,255)
            for s in list:
                if self.table.item(s,5).text() == "add":
                    list1.append(s)
            list2=list1[::-1]

            for ss in range(0,len(list2)):
                if ss< len(list2)-1:
                        for j in range(7,11,1):
                            if self.table.item(list2[ss],j).text() == self.table.item(list2[ss+1],j).text():
                                pass
                            else:
                                self.setTableCellColor(list2[ss+1],j,200,200,100)
                                self.list.append([list2[ss+1],j])

                else:
                    pass
            for k in range(len(list)):
                if self.table.item(list[k], 5).text() == "report":
                    self.setTableCellColor(list[k], 1, 200, 200, 100)
                    self.list.append([list[k], 1])
        else:
            pass


    def setTableCellColor(self,a,b,c,d,e):
        if isinstance(self.table.item(a,b),type(None)):
            pass
        else:
            self.table.item(a,b).setBackground(QColor(c,d,e))


    def hiderows(self,flags):
        if flags == 1:
            for i in range(0,self.table.rowCount()):  #设置隐藏行
                if self.table.item(i,5).text() == "0" :
                # or (self.table.item(i,5).text() == "del" and \
                #             ((self.table.item(i,7).text() == "0:0" or self.table.item(i,7).text() == "")
                #              or (self.table.item(i,9).text() == "0:0" or self.table.item(i,9).text() == "")))
                    self.table.setRowHidden(i,True)
                else:
                    self.table.setRowHidden(i,False)
    def hidecolumns(self,column):
        i=0
        for s in range(self.table.rowCount()):
            if self.table.item(s,column).text() == "":
                pass
            else:
                i+=1
        if i == 0:
            self.table.setColumnHidden(column,True)
        else:
            self.table.setColumnHidden(column,False)

    def set7Aschedulecolumnwidth(self):
        self.table.setColumnWidth(0,190)
        self.table.setColumnWidth(1, 77)
        self.table.setColumnWidth(2, 76)
        self.table.setColumnWidth(3, 275)
        self.table.setColumnWidth(4, 85)
        self.table.setColumnWidth(5, 89)
        self.table.setColumnWidth(6, 88)
        self.table.setColumnWidth(7, 84)
        self.table.setColumnWidth(8, 92)
        self.table.setColumnWidth(9, 93)
        self.table.setColumnWidth(10, 112)
    def resizeEvent(self, QResizeEvent):
        self.table.resize(self.width(),self.height()-100)
        # print("窗体宽度:"+str(self.width()),"窗体高度:"+str(self.height()))
        # for i in range(self.table.columnCount()):
        #     print("第"+str(i)+"列宽:"+str(self.table.columnWidth(i)))
    def get7AScheduleNeedData(self,cidScheduleLog):
        data=[]
        data.append(cidScheduleLog.getT())
        data.append(cidScheduleLog.getminute())
        data.append(cidScheduleLog.getaccountid())
        data.append(cidScheduleLog.geOwnCid())
        data.append(cidScheduleLog.getlogsFrom())
        data.append(cidScheduleLog.getactions())
        data.append(cidScheduleLog.getscheduleid())
        data.append(cidScheduleLog.getschStartTime())
        data.append(cidScheduleLog.getstartAction())
        data.append(cidScheduleLog.getendTime())
        data.append(cidScheduleLog.getloop())
        return data

