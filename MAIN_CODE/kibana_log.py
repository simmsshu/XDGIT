# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QGridLayout,QLabel,QFrame
from PyQt5.QtGui import QIcon,QFont,QPalette,QBrush,QPixmap
from PyQt5.QtCore import Qt
from totalOnoffline import OnOffLine
from kibana_pic import img1,imag2,image_close,image_max,image_min,image_loading,image_front,image_next,image_search
import base64,webbrowser,UrL,os
from online_Excel_show import Oline_Excel_Window
from schedule_log import ScheduleLog
from mongoshow import MongoShow
from config import *
from UserOnOffline import UserOnOffline
# from _7AOonOff import UI
class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window()
    def main_window(self):

        self.wetherpath_exit()
        self.setWindowOpacity(1)
        self.setAutoFillBackground(True)
        #设置背景图片自适应窗口大小
        self.pix = QPixmap("./pic/background.png")
        # self.pix = self.pix.scaled(self.width(), self.height())
        # 设置背景图片
        pallete=QPalette()
        pallete.setBrush(QPalette.Background, QBrush(self.pix))
        self.setPalette(pallete)
        # 设置背景色透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置无边框属性
        self.setWindowFlag(Qt.FramelessWindowHint)
        #设置窗体图标
        # self.setWindowIcon(QIcon("kibana.png"))
        self.setWindowTitle("日志查询")
        self.resize(600,400)
        # Top_Text=QLabel(self)
        # Top_Text.setText("请选择需要查询的信息")
        # fon=QFont("宋体",20)
        # Top_Text.setFont(fon)
        # Top_Text.move(20,50)
        main_layout=QGridLayout(self)
        #设置边距
        main_layout.setContentsMargins(0,0,0,0)
        #设置布局控件间隔
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        self.top=QGridLayout()
        self.top_widget=QWidget()
        # self.top_widget.setStyleSheet("QWidget{background:red}")
        self.top_widget.setLayout(self.top)
        self.left=QGridLayout()
        self.left_widget=QWidget()
        self.left_widget.setLayout(self.left)
        # self.left_widget.setStyleSheet("QWidget{background:red}")
        self.middle=QGridLayout()
        self.middle_widget=QWidget()
        self.middle_widget.setLayout(self.middle)
        # self.middle_widget.setStyleSheet("QWidget{background:green}")
        self.right=QGridLayout()
        self.right_widget=QWidget()
        self.right_widget.setLayout(self.right)
        # self.right_widget.setStyleSheet("QWidget{ background:blue}")

        Lab1=QLabel(self)
        Lab1.setFixedSize(15,15)
        Lab1.setScaledContents(True)
        Lab1.setPixmap(QPixmap("./pic/kibana.png"))
        Frame1=QFrame(self)
        #设置最小化图片和触发事件
        Btn1 = QPushButton(self)
        Btn1.setStyleSheet("QPushButton{border-image: url(./pic/min.ico)}")
        Btn1.setFixedSize(10,10)
        Btn1.clicked.connect(self.showMinimized)
        #设置最大化和常规图标和触发事件
        self.Btn2=QPushButton("1",self)
        self.Btn2.setStyleSheet("QPushButton{border-image: url(./pic/max.ico)}")
        self.Btn2.setFixedSize(10,10)
        self.Btn2.clicked.connect(self.max_or_normal)
        #设置关闭窗口图标和触发事件
        Btn3=QPushButton(self)
        Btn3.setStyleSheet("QPushButton{border-image: url(./pic/close.ico)}")
        Btn3.setFixedSize(10,10)
        Btn3.clicked.connect(self.close)


        self.top.addWidget(Lab1,0,0,1,1,Qt.AlignTop)
        self.top.addWidget(Frame1,0,1,1,56,Qt.AlignTop)
        self.top.addWidget(Btn1,0,57,1,1,Qt.AlignTop)
        self.top.addWidget(self.Btn2,0,58,1,1,Qt.AlignTop)
        self.top.addWidget(Btn3,0,59,1,1,Qt.AlignTop)

        Btn4=QPushButton("MD5解密",self)
        Btn5=QPushButton("OPS",self)
        Btn6=QPushButton("Kibana_7A",self)
        Btn7=QPushButton("Kibana_VDMP",self)
        Btn8=QPushButton("Kibana_AppServer",self)
        Btn9=QPushButton("Kibana_Thirdparty",self)
        Btn10=QPushButton("Vesync云平台",self)

        Btn4.clicked.connect(self.toolbutton)
        Btn5.clicked.connect(self.toolbutton)
        Btn6.clicked.connect(self.toolbutton)
        Btn7.clicked.connect(self.toolbutton)
        Btn8.clicked.connect(self.toolbutton)
        Btn9.clicked.connect(self.toolbutton)
        Btn10.clicked.connect(self.toolbutton)
        Listbtn=[Btn4,Btn5,Btn6,Btn7,Btn8,Btn9,Btn10]
        self.add_widget_toLayout(self.left,Listbtn,2,1,60,1)

        #添加按键
        btn1 = QPushButton( "掉线日志",self)
        btn1.clicked.connect(self.goonoffline)
        # btn2 = QPushButton( "在线表格",self)
        # btn2.clicked.connect(self.goAppServer)
        btn3 = QPushButton("Schedule日志",self)
        btn3.clicked.connect(self.goScheduleLog)
        btn4 = QPushButton( "配网日志",self)
        btn4.clicked.connect(self.AppUploadLog)
        btn5 = QPushButton( "综合",self)
        btn5.clicked.connect(self.goComprehensive)
        btn6 = QPushButton( "UserOnOFFline",self)
        btn6.clicked.connect(self.userOnOffLine)
        btn7 = QPushButton( "7A开关查询",self)
        btn7.clicked.connect(self._7AOnOffSearch)
        list1=[btn1,btn3,btn4,btn6,btn7,btn5]
        self.add_widget_toLayout(self.middle,list1,2,1,60,1)

        main_layout.addWidget(self.top_widget,0,0,1,40)
        main_layout.addWidget(self.left_widget,1,0,59,4)
        main_layout.addWidget(self.middle_widget,1,4,59,30)
        main_layout.addWidget(self.right_widget,1,34,59,6)


        # 设置按键大小
        btn1.setFixedSize(200, 30)
        # btn2.setFixedSize(200, 30)
        btn3.setFixedSize(200, 30)
        btn4.setFixedSize(200, 30)

        #设置控件背景色和边框圆角属性
        # self.setStyleSheet("QPushButton{border-radius:5px;background: url(./background.png)}")
        # btn2.setStyleSheet("QPushButton{border-radius:5px}")


        # grid=QGridLayout(self)
        # # grid.setSpacing(5)
        # # grid.addWidget(Top_Text, 0, 0,Qt.AlignTop)
        # grid.addWidget(btn1, 0, 0,Qt.AlignTop)
        # # grid.addWidget(btn2, 1, 0,Qt.AlignTop)
        # grid.addWidget(btn3, 2, 0,Qt.AlignTop)
        # grid.addWidget(btn4, 3, 0,Qt.AlignTop)

        self.show()
    def max_or_normal(self):
        text=self.sender().text()
        if text == "1":
            self.showMaximized()
            self.Btn2.setText("0")
        if text == "0":
            self.showNormal()
            self.Btn2.setText("1")
    def wetherpath_exit(self):
        folder = os.path.exists("./pic")
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs("./pic")

        else:
            pass
        self.writeBase64ToPic("./pic/front.ico", image_front)
        self.writeBase64ToPic("./pic/next.ico", image_next)
        self.writeBase64ToPic("./pic/search.ico", image_search)
        self.writeBase64ToPic("./pic/kibana.png", img1)
        self.writeBase64ToPic("./pic/background.png", imag2)
        self.writeBase64ToPic("./pic/min.ico", image_min)
        self.writeBase64ToPic("./pic/max.ico", image_max)
        self.writeBase64ToPic("./pic/close.ico", image_close)
        self.writeBase64ToPic("./pic/loading.gif", image_loading)

    def writeBase64ToPic(self,path,base64_pic_name):
        if not os.path.exists(path):
            f = open(path, "wb")
            f.write(base64.b64decode(base64_pic_name))
            f.close()
        else:
            pass

    def add_widget_toLayout(self,layout,list,rows,cloumns,total_row,total_colum):
        start_row=0
        start_clu=0
        for x in list:
            layout.addWidget(x,start_row,start_clu,rows,cloumns)
            if start_row <total_row-1:
                start_row+=rows
            if start_clu < total_colum-1:
                start_clu+=cloumns
        if start_row<total_row-1 or start_clu < total_colum-1:
            layout.addWidget(QFrame(self),start_row,start_clu,total_row - start_row,total_colum - start_clu)
    def goComprehensive(self):
        list0.append(defineWindow())
    def goonoffline(self,a):#显示子窗口部件
        list0.append(OnOffLine())
    # def goAppServer(self):
    #     List1.append(Oline_Excel_Window())
    def goScheduleLog(self):
        List2.append(ScheduleLog())
    def AppUploadLog(self):
        List3.append(MongoShow())
    def userOnOffLine(self):
        list0.append(UserOnOffline())
    def _7AOnOffSearch(self):
        list0.append(UI())
    def toolbutton(self):
        text=self.sender().text()
        if text == "MD5解密":
            self.openUrl(UrL.url1)
        elif text == "OPS":
            self.openUrl(UrL.url2)
        elif text == "Kibana_7A":
            self.openUrl(UrL.url3)
        elif text == "Kibana_VDMP":
            self.openUrl(UrL.url4)
        elif text == "Kibana_AppServer":
            self.openUrl(UrL.url5)
        elif text == "Kibana_Thirdparty":
            self.openUrl(UrL.url6)
        elif text == "Vesync云平台":
            self.openUrl(UrL.url7)

    def openUrl(self,url):
        try:
            webbrowser.get('windows-default').open_new_tab(url) #使用系统默认浏览器打开，若要使用Google浏览器打开，需要先将google浏览器设为默认浏览器
        except Exception as e:
            # raise e
            webbrowser.open_new_tab(url)  # 使用IE浏览器打开

if __name__ == "__main__":
    app=QApplication(sys.argv)
    list0=[]
    List1=[]
    List2=[]
    List3=[]
    winndow = Main_window()
    app.exec_()
