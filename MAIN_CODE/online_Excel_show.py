from PyQt5.QtWidgets import QMainWindow,QPushButton,QLabel,QTableWidget,QLineEdit,QWidget,QApplication,QFrame,QCheckBox,QTextEdit,QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from online_Excel import Deal_data
import threading
from random import choice
# import webbrowser

class Oline_Excel_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.show_excel_window()
    def show_excel_window(self):
        self.setWindowIcon(QIcon("kibana.png"))
        self.setWindowTitle("在线表格问题处理")
        self.setGeometry(40,40,1000,900)
        self.frame=QFrame(self)
        self.frame.setGeometry(0,20,1000,60)
        # self.frame.setStyleSheet('background-color:green;')
        self.frame.setFrameShape(1)
        self.lab0=QLabel(self)
        self.lab0.setText("请选择需要统计的表格")
        self.lab0.setGeometry(0,0,950,20)
        self.lab1 = QLabel(self.frame)
        self.lab1.setGeometry(0, 0 , 80, 20)
        self.lab1.setOpenExternalLinks(True)
        self.lab1.setText(u'<a href="https://docs.qq.com/sheet/DSGNaUWFkY3lEZU5m?tab=BB08J3&c=M211A0HA0" style="color:#0000ff;"><b> 在线问题 </b></a>')
        self.lab2 = QLabel(self.frame)
        self.lab2.setGeometry(0, 20, 80, 20)
        self.lab2.setOpenExternalLinks(True)
        self.lab2.setText(u'<a href="https://docs.qq.com/sheet/DZWN3a1hGU1pTVnlo?tab=BB08JN&coord=C20A0M0" style="color:#0000ff;"><b> 131S问题 </b></a>')
        self.lab3 = QLabel(self.frame)
        self.lab3.setGeometry(0, 40, 80, 20)
        self.lab3.setOpenExternalLinks(True)
        self.lab3.setText(u'<a href="https://docs.qq.com/sheet/DSEZIc25uRlhzVk5G?tab=BB08J2&c=H2A0B0" style="color:#0000ff;"><b> 空气炸锅 </b></a>')
        self.radio1=QCheckBox(self.frame)
        self.radio1.setGeometry(80, 0, 20, 20)
        self.radio1.setChecked(True)
        self.radio2=QCheckBox(self.frame)
        self.radio2.setGeometry(80, 20, 20, 20)
        self.radio2.setChecked(True)
        self.radio3=QCheckBox(self.frame)
        self.radio3.setGeometry(80, 40, 20, 20)
        self.radio3.setChecked(True)

        self.btn1=QPushButton(self)
        self.btn1.setText("开始")
        self.btn1.setGeometry(950,0,50,20)

        self.text_box=QTextEdit(self)
        self.grid=QGridLayout(self)
        self.grid.addWidget(self.lab0,0,0,2,18,Qt.AlignTop|Qt.AlignLeft)
        self.grid.addWidget(self.btn1,0,18,2,2,Qt.AlignTop|Qt.AlignHCenter)
        self.grid.addWidget(self.frame,2,0,6,20)
        self.grid.addWidget(self.text_box,8,0,60,20)
        self.btn1.clicked.connect(self.godownload)
        self.show()
    def godownload(self):
        header1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/80.0.3987.122 Safari/537.36"}
        header2 = {"User-Agent": "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
                Version/5.1Safari/534.50"}
        header3 = {"User-Agent": "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)\
                Version/5.1Safari/534.50"}
        header4 = {"User-Agent": "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)\
                Chrome/17.0.963.56Safari/535.11"}
        header5 = {"User-Agent": "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)"}
        headers = [header1, header2, header3, header4, header5]
        header = choice(headers)
        url=[]
        cookie = {"cookie": "pgv_pvi=9702543360; RK=3Pp4u8PG1H; ptcz=cb201b67953a7fb1fa3cc1c6e689ccb3a30454416589677022ac5a4f1b9a2b65; ptui_loginuin=simmsshu@etekcity.com.cn; hashkey=dc690184; \
        pgv_si=s2740144128; uin=o3004044439; skey=@eK3AbIxTh; p_uin=o3004044439; pt4_token=ekn1WfWZ5rkyJJy1lbvUOa4sJkP1cjTdEsYUYBNWevY_; p_skey=EMvBRBs7afNLl3giDAIPESR3FWGmMEWeZ8JZ6G9Mv1s_; \
        p_luin=o3004044439; p_lskey=00040000e37ee1343238282876b6e6688b02838077902fd10b4ac30eaad75e346c63c51e3f0adea6e687af69; has_been_login=1; uid=144115212495570955; utype=qq; \
        vfwebqq=f353b87adf777a77783225407fa7b52dfc336a1a4b9eb26eafe0906133f9a2e7ebe98efc74993414; loginTime=1584092545059; uid_key=2BB1DW0%2Ffr%2BG3ZbyvwV12hYDeJcT6PBRmG79YZ3JdOYxiC3j9vOZvkDrn%2FIvwD\
        8Hwa9RiMwPjYB9oTJukEzti5KqSlFHyFYa; ES2=5eda814a1c3bc794; TOK=1c1522118bcff6fe; _qpsvr_localtk=1585207360764"}
        if self.radio1.isChecked() == True:
            url.append("https://docs.qq.com/ep/pad/exportfile/HcZQadcyDeNf?s=f770a00607006a669115bc2b3c07faa4")
        if self.radio2.isChecked() == True:
            url.append("https://docs.qq.com/ep/pad/exportfile/ecwkXFSZSVyh?s=e95bccfa4b7ccfb1feeffad3ab124a54")
        if self.radio3.isChecked() == True:
            url.append("https://docs.qq.com/ep/pad/exportfile/HFHsnnFXsVNF?s=42c6ee01b1c15c4b4e184fcbe4fcab56")
        if len(url) == 0:
            self.choice_empty()
        else:
            for key in range(len(url)-1):
                ss=Deal_data(header, cookie)
                t=threading.Thread(target=ss.get_url_data(url[key]))
                t.start()
                self.text_box.append("开始从"+"{}".format(url[key])+"下载，下载中........"+"\n")
            t.join()


    def choice_empty(self):
        pass
    def write_info_into_textbox(self,str=""):
        pass




#
#
#
# ss = Deal_data(header, cookie)
# data = ss.get_url_data(url=url0)
# ss.write_excel_data(data, name="在线问题")