import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 500, 300)

        self.btn1 = QPushButton("load",self)
        self.btn1.setGeometry(10,10,200,30)
        self.btn1.clicked.connect(self.btn_fun_FileLoad) 

        self.label = QLabel(self) 

    def btn_fun_FileLoad(self):        
        fname=QFileDialog.getOpenFileName(self)        
        if fname[0]:
            pixmap = QPixmap(fname[0])
            self.label.setPixmap(pixmap)
            
        else: 
            QMessageBox.about(self, 'Warning', '파일을 선택하지 않았습니다.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()