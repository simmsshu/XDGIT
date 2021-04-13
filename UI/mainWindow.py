# from BASE_ABOUT.needClass import TempleteWindow
# from MAIN_CODE.schedule_log import *
from PyQt5.QtWidgets import QApplication,QWidget,QTreeWidget,QHBoxLayout,QVBoxLayout,QTreeWidgetItem,QPushButton,\
                            QHBoxLayout,QLabel,QSizePolicy,QLayoutItem,QLineEdit,QButtonGroup,QFrame
from PyQt5.QtGui import QPalette,QIcon
from PyQt5.QtCore import Qt,QSize
from copy import deepcopy
from needBase import TempleteWindow
import sys
import os
import json
import logging
import threading
import importlib

#图片文件夹路径
PIC_BASE_DIR = "./SOURCES/pic/"
ROOTSONTREEFLAG = False
LABEL_LABEL = []
LABEL_NUMBER = 0
#右侧主窗口启动一个界面启动一个线程
THREADS = []
logging.basicConfig(level=logging.INFO)
def get_json_data():
    with open("package.json","r",encoding="utf-8") as f:
        data = json.loads(f.read())
        return data
QTREESTYLE = '''
        QHeaderView::section { 
            height:25px;
            color:white;
            font-family:黑体;
            background:#505050;
            border-left:0px solid gray; 
            border-right:1px solid gray; 
            border-top:0px solid gray; 
            border-bottom:0px solid gray;
        }
        
        QTreeView {
            border:none;
            font-family:楷体;            
            background: #404040;
            show-decoration-selected: 1;
            border-bottom-left-radius:10px;
        }
        QTreeView::item {
            height: 25px;
            border: none;
            color: white;
            background: transparent;
        }
        QTreeView::item:hover {
            background: transparent;
        }
        QTreeView::item:selected{
            background: #1E90FF;
        }
        QTreeView::branch {
            background: transparent;
        }
        QTreeView::branch:hover {
            background: transparent;
        }
        QTreeView::branch:selected {
            background: #1E90FF;
        }
        QTreeView::branch:closed:has-children{
            image: url(D:/pycharmproject/project1/venv/pic/haschild2.png);
        }
        QTreeView::branch:open:has-children{
            image: url(D:/pycharmproject/project1/venv/pic/openchild2.png);
        }'''


class MainWindow(TempleteWindow,QWidget):
    def __init__(self):
        super().__init__()
        #左侧窗口显示因隐藏按键标记
        self.hide_show_flag = False
        #存放导入包对应的索引
        self.importdict = {}
        # 设置主窗体水平分布
        self.set_title("查询工具")
        self.layout = QHBoxLayout()
        self.left_main_widget = QWidget(self.contentWindow)
        self.left_main_widget.setStyleSheet(QTREESTYLE)
        self.left_main_widget.setObjectName("leftmain")
        self.right_main_widget = QWidget(self.contentWindow)
        self.right_main_widget.setStyleSheet("{border-bottom-right-radius:10px;}")
        self.contentWindow.setLayout(self.layout)
        self.layout.addWidget(self.left_main_widget, 1)
        self.layout.addWidget(self.right_main_widget, 9)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # 设置子类传递给父类的方法和参数（当父类resiziEvent执行时一并执行）
        self.set_son_attr({"Module": "mainWindow", "class": "MainWindow", "method": "windowResize", "args": self})
        # 设置左侧树形结构试图
        self.left_main_layout = QVBoxLayout()
        self.left_main_layout.setContentsMargins(0, 0, 0, 0)
        self.roottree = QTreeWidget(self.left_main_widget)
        self.roottree.setObjectName("maintree")
        self.left_main_widget.setLayout(self.left_main_layout)
        self.left_main_layout.addWidget(self.roottree)
        self.roottree.setColumnCount(1)
        self.roottree.setHeaderLabels(["Kibana日志"])
        self.roottree.clicked.connect(self.treeclicked)
        self.setwindow()

    def root_son_tree_click_setting(self):
        # 设置右侧内容界面
        logging.debug("root_son_tree_click_setting into")
        # self.main_widget_top_label = QLabel(self.right_main_widget)
        self.main_widget_top_label = NetworkLabel()
        self.main_widget_top_label.setParent(self.right_main_widget)
        #设置标题点击触发事件
        self.main_widget_top_label.labelclicked_method = self.right_main_lable_btn_clicked
        self.main_widget_top_label.clobtnclicked_method = self.right_main_lable_close_btn_clicked
        self.main_widget_content_window = QWidget(self.right_main_widget)
        self.main_widget_content_window.setStyleSheet(self._get_main_content_style(0))
        self.main_widget_content_window.setObjectName("main")
        self.main_widget_content_window_layout = QVBoxLayout()
        self.main_widget_content_window_layout.setSpacing(0)
        self.main_widget_content_window_layout.setContentsMargins(0,0,0,0)
        self.main_widget_content_window.setLayout(self.main_widget_content_window_layout)
        #设置右侧主界面布局
        self.right_main_layout = QVBoxLayout()
        self.right_main_layout.addWidget(self.main_widget_top_label,1)
        self.right_main_layout.addWidget(self.main_widget_content_window,39)
        self.right_main_layout.setSpacing(0)
        self.right_main_layout.setContentsMargins(0,0,0,0)
        self.right_main_widget.setLayout(self.right_main_layout)

        # 添加显示隐藏按钮
        self.hide_show_btn = QPushButton(self.right_main_widget)
        self.hide_show_btn.setGeometry(0, 0, 8, 8)
        self.hide_show_btn.setIcon(QIcon(PIC_BASE_DIR + "openchild.png"))
        self.hide_show_btn.setToolTip("隐藏")
        self.hide_show_btn.clicked.connect(self.show_or_hide_left_main_widget)

        self.main_widget_top_label.show()
        self.main_widget_content_window.show()
        self.hide_show_btn.show()
        logging.debug("root_son_tree_click_setting achived")

    #设置右侧窗口跟随左侧隐藏按钮变化，default = 1表示左侧窗口未隐藏状态
    def right_window_size_setting(self):
        if not self.hide_show_flag:
            self.main_widget_content_window.setStyleSheet(self._get_main_content_style(0))
        else:
            self.main_widget_content_window.setStyleSheet(self._get_main_content_style(10))

    #设置左侧树形结构目录
    def setwindow(self):
        # 添加目录
        self.trees = get_json_data()["left_tree_list"]
        for s in self.trees.keys():
            d = QTreeWidgetItem(self.roottree)
            d.setText(0, s)
            if len(self.trees[s].keys()) > 0:
                for k in self.trees[s].keys():
                    self.add_child_to_front(d,k)
                    if self.trees[s][k]["trace"] == "":
                        self.importdict[k] = importlib.import_module(self.trees[s][k]["file"])
                    else:
                        self.importdict[k] = importlib.import_module(
                            self.trees[s][k]["trace"] + "." + self.trees[s][k]["file"])
        # logging.debug("self.importdict:{}".format(self.importdict))

    def _get_main_content_style(self,raidus):
        return  f'''.QWidget{{border-bottom-left-radius:{raidus}px;border-bottom-right-radius:10px;background-color:#EFEFEF;}}
                    QWidget > QWidget > QPushButton:hover{{background-color:#DEDEDE;}}'''

    # 点击树形结构子树显示右侧label界面
    def treeclicked(self,treeattr):
        global  ROOTSONTREEFLAG,THREADS
        if treeattr.data() not in self.trees.keys():
            if ROOTSONTREEFLAG:
                try:
                    self.add_label_to_mainwidget_label(treeattr)
                except Exception as f:
                    raise
                    logging.debug(f)
            else:
                ROOTSONTREEFLAG = True
                self.root_son_tree_click_setting()
                try:
                    self.add_label_to_mainwidget_label(treeattr)
                except Exception as f:
                    raise
                    logging.debug(f)

    #切换右侧内容窗口函数
    def change_main_widget_content_window(self):
        global LABEL_LABEL
        for d in self.main_widget_content_window.children():
            if d.isWidgetType():
                d.setHidden(True)
        LABEL_LABEL[-1]["showwidget"].setHdden(False)

    # 关闭右侧内容窗口函数
    def right_main_lable_close_btn_clicked(self):
        # print("LABEL-LABLE:{}".format(LABEL_LABEL))
        for d in range(len(LABEL_LABEL)):
            if LABEL_LABEL[d]["closelabel"] == self.sender().objectName():
                del LABEL_LABEL[LABEL_LABEL.index(LABEL_LABEL[d])]
                self.main_widget_content_window_layout.itemAt(d).widget().deleteLater()
                break
        if d:
            self.main_widget_top_label.labeldict[self.main_widget_top_label.labellist[-1]]["widget"].setChecked(True)
            self.main_widget_top_label.labeldict[self.main_widget_top_label.labellist[-1]]["closebtn"].setHidden(False)
        self.main_widget_content_window_show()

    #添加主菜单内容
    def add_label_to_mainwidget_label(self,tree):
        global LABEL_LABEL,LABEL_NUMBER
        logging.debug("son tree clicked:{},{}".format(tree.data(),tree.parent().data()))
        self.main_widget_top_label.addtitle(tree.data(),"label"+str(LABEL_NUMBER),QIcon(PIC_BASE_DIR + "close1.ico"))
        wid = getattr(self.importdict[tree.data()],self.trees[tree.parent().data()][tree.data()]["class"])
        logging.debug("add_label_to_mainwidget_label—wid:{}".format(wid))
        self.add_widget_to_right_label(
            self.main_widget_top_label.labeldict[self.main_widget_top_label.labellist[-1]]["widget"].objectName(),
            self.main_widget_top_label.labeldict[self.main_widget_top_label.labellist[-1]]["closebtn"].objectName(),
            wid(self.right_main_widget))
        self.right_main_lable_btn_clicked()
        # lab.show()
        LABEL_NUMBER += 1

    #右侧主窗口显示最新widget
    def right_main_lable_btn_clicked(self):
        sender = self.sender().objectName()
        global LABEL_LABEL
        #隐藏所有窗口
        for d in self.main_widget_content_window.children():
            if d.isWidgetType():
                d.setHidden(True)
        #显示点击窗口
        for s in range(len(LABEL_LABEL)):
            if LABEL_LABEL[s]["label"] == sender:
                LABEL_LABEL.append(LABEL_LABEL[s])
                del LABEL_LABEL[s]
                break
            else:
               pass
        self.main_widget_content_window_layout.addWidget(LABEL_LABEL[-1]["showwidget"])
        self.main_widget_content_window_show()

    def main_widget_content_window_show(self):
        try:
            LABEL_LABEL[-1]["showwidget"].setHidden(False)
            LABEL_LABEL[-1]["showwidget"].show()
        except AttributeError as f:
            logging.warning(f)
        except IndexError:
            pass


    def add_widget_to_right_label(self,label,closelabel,showwidget = None):
        global LABEL_LABEL
        LABEL_LABEL.append({"label":label,"closelabel":closelabel,"showwidget":showwidget})
        logging.debug("LABEL_LABEL:{}".format(LABEL_LABEL))
        # self.main_widget_content_window_show()


    def windowResize(self):
        print("self.width:{}".format(self.width()))
        print("self.left_main_widget:{}".format(self.left_main_widget()))
        print("self.right_main_widget:{}".format(self.right_main_widgetwidth()))
        print("self.main_widget_top_label.width:{}".format(self.main_widget_top_labelwidth()))
        print("self.main_widget_content_window.width:{}".format(self.main_widget_content_window.width()))
        # print("self.width:{}".format(self.width()))
        # print("self.width:{}".format(self.width()))
        return

    def add_child_to_front(self,front,text,check = None):
        QTreeWidgetItem(front).setText(0, text)

    def mainwidget_label(self,labelname,labelUI):
        pass
    #左侧菜单点击隐藏和显示
    def show_or_hide_left_main_widget(self):
        if not self.hide_show_flag:
            self.hide_show_flag = True
            self.left_main_widget.setHidden(True)
            self.hide_show_btn.setIcon(QIcon(PIC_BASE_DIR + "haschild.png"))
            self.hide_show_btn.setToolTip("展开")
        else:
            self.hide_show_flag = False
            self.left_main_widget.setHidden(False)
            self.hide_show_btn.setIcon(QIcon(PIC_BASE_DIR + "openchild.png"))
            self.hide_show_btn.setToolTip("隐藏")
        self.right_window_size_setting()
        logging.debug("show_or_hide_left_main_widget-right_main_widget.width:{}".format(self.right_main_widget.width()))

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_F1:
            self.show_or_hide_left_main_widget()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = MainWindow()
    d.show()
    app.exec_()
