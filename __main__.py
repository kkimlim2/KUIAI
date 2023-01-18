import sys
import json

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from prediction import *

main_class = uic.loadUiType("KUIAI/main.ui")[0]
second_class = uic.loadUiType("KUIAI/second.ui")[0]
model_path = 'KUIAI/model_class23.pt'
inf_path = 'KUIAI/inf_info.csv'
file_path = 'KUIAI/output.json'

class MainClass(QMainWindow, main_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.mode = None
        self.gender = None
        self.size = None
        self.inf_id = None
        self.inf_img = None


        self.btn_loadImage.clicked.connect(self.loadImageFunction)
        self.btn_predict.clicked.connect(self.PredictStyleFunction) 
        self.set_use.currentTextChanged.connect(self.setuseFunction)
        self.set_gender.currentTextChanged.connect(self.setgenderFunction)
        self.set_size.currentTextChanged.connect(self.setsizeFunction)


    def setuseFunction(self):
        mode =  str(self.set_use.currentText())
        if mode == '제조자' : self.mode = 'S'
        elif mode == '소비자' : self.mode = 'C'
        else: self.mode == None
        print(self.mode)

    def setgenderFunction(self):
        gender =  str(self.set_gender.currentText())
        if gender == '남성' : self.gender = 'M'
        elif gender == '여성' : self.gender = 'F'
        else: self.gender == None
        print(self.gender)

    def setsizeFunction(self):
        size =  str(self.set_size.currentText())
        if size == '어쩌구' : self.size = 'S'
        elif size == '저쩌구' : self.size = 'L'
        else: self.size == None
        print(self.size)    
        
    def loadImageFunction(self) :
        fname=QFileDialog.getOpenFileName(self)
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(fname[0])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.InputStyle.setPixmap(self.qPixmapFileVar)
        self.inputImageName = fname[0]

    def PredictStyleFunction(self):
        if self.mode == None:
            QMessageBox.information(self,'Warning','모드를 선택해주세요')
        else:
            self.style = predict_style(self.inputImageName, model_path, 'cpu')
            QMessageBox.information(self,'Information',f'{self.style}로 예측되었습니다. 해당 스타일의 인플루언서를 추천드리겠습니다.')
            if (self.gender == None) or (self.size == None): 
                QMessageBox.information(self,'Warning','성별을 선택해주세요')
                QMessageBox.information(self,'Warning','체형을 선택해주세요')
            else:
                if self.mode == 'S':
                    inf_id, inf_img = recomm_inf_sup(inf_path, self.gender, self.size, self.style)
                    pass
                elif self.mode == 'C':
                    inf_id, inf_img = recomm_inf_cust(inf_path, self.gender, self.size, self.style)
                    pass
                ## 이거를 text 파일을 만들어서 써야겠다
                data = {}
                data['infs'] = inf_id
                data['imgs'] = inf_img
                with open(file_path, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

                ans = QMessageBox.question(self, '새 창 알림','새 창에서 결과를 확인하겠습니까?', 
                                    QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

                if ans == QMessageBox.Yes:
                    self.secondwindow = SecondClass()


class SecondClass(QMainWindow, second_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()

        ## 파일 저장한 걸 열어서 그려

        file_path = "./sample.json"
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            self.inf_id = json_data['infs']
            self.inf_img = json_data['imgs']

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(self.inf_img[0])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.Style1.setPixmap(self.qPixmapFileVar)

        self.qPixmapFileVar.load(self.inf_img[1])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.Style2.setPixmap(self.qPixmapFileVar)

        self.qPixmapFileVar.load(self.inf_img[2])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.Style3.setPixmap(self.qPixmapFileVar)

        self.inf1.setText(self.inf_id[0])
        self.inf1.setText(self.inf_id[1])
        self.inf1.setText(self.inf_id[2])
        self.InfoText.setText('짜잔~ 뭔가 좋은 문구가 뭐 없을까')

if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = MainClass() 
    myWindow.show()
    app.exec_()