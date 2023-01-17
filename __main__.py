import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("KUIAI/design.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.mode = None

        self.btn_loadImage.clicked.connect(self.loadImageFunction)
        self.btn_predict.clicked.connect(self.PredictStyleFunction)
        self.groupBox_supplier.clicked.connect(self.groupboxRadFunction)
        self.groupBox_customer.clicked.connect(self.groupboxRadFunction)

    def loadImageFunction(self) :
        fname=QFileDialog.getOpenFileName(self)
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(fname[0])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.InputStyle.setPixmap(self.qPixmapFileVar)
        self.inputImageName = fname

    def PredictStyleFunction(self):
        if self.mode == None:
            QMessageBox.information(self,'Warning','모드를 선택해주세요')
        elif self.mode == 'S':
            pass
        elif self.mode == 'C':
            pass

    def groupboxRadFunction(self):
        if self.groupBox_supplier.isChecked(): self.mode = 'S'
        else: self.mode = 'C'


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()