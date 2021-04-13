from BASE_ABOUT.needClass import TempleteWindow
from MAIN_CODE.ConfigDataAnalys.ts_mysql import MongoConfigDetailInfo
from MAIN_CODE.ConfigDataAnalys.getConfigData import Mongodb_connect
from PyQt5.QtWidgets import QApplication
import sys
class Window(TempleteWindow):
    def __init__(self):
        super().__init__()
        self.show()

if __name__ == "__main__":
    s = QApplication(sys.argv)
    d = Window()
    s.exec_()