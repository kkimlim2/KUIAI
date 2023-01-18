import sys
import json

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from prediction import *
import argparse   

#parser 로 정보 입력받기(사전훈련된 모델, 컴퓨팅소스, 인플루언서 스타일 예측 정보)
parser = argparse.ArgumentParser(description='이 프로그램의 설명(그 외 기타등등 아무거나)')    # 2. parser를 만든다.
parser.add_argument('--model', required=False, default = 'KUIAI/model_class23.pt')
parser.add_argument('--device', required=False, default='cpu')
parser.add_argument('--info', required=False, default = 'KUIAI/inf_info.csv')
args = parser.parse_args()

#초기 설정 
main_class = uic.loadUiType("KUIAI/main.ui")[0]
second_class = uic.loadUiType("KUIAI/second.ui")[0]
model_path = args.model
inf_path = args.info
file_path = 'KUIAI/output.json'

#프로토타입의 메인 창 
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

    #이용자가 제조자인지, 소비자인지 입력값 받기
    def setuseFunction(self):
        mode =  str(self.set_use.currentText())
        if mode == '제조자' : self.mode = 'S'
        elif mode == '소비자' : self.mode = 'C'
        else: self.mode == None
        print(self.mode)

    #매칭되기를 원하는 인플루언서의 성별 입력값 받기
    def setgenderFunction(self):
        gender =  str(self.set_gender.currentText())
        if gender == '남성' : self.gender = 'M'
        elif gender == '여성' : self.gender = 'F'
        else: self.gender == None
        print(self.gender)

    #매칭되기를 원하는 인플루언서의 체형 입력값 받기
    def setsizeFunction(self):
        size =  str(self.set_size.currentText())
        if size == '어쩌구' : self.size = 'S'
        elif size == '저쩌구' : self.size = 'L'
        else: self.size == None
        print(self.size)    
        
    #원하는 사진 입력값 받기
    def loadImageFunction(self) :
        fname=QFileDialog.getOpenFileName(self)
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(fname[0])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.InputStyle.setPixmap(self.qPixmapFileVar)
        self.inputImageName = fname[0]

    #입력값 기반으로 스타일 예측
    def PredictStyleFunction(self):
        #입력값이 다 주어지지 않았을 경우 경고 메세지
        if self.mode == None:
            QMessageBox.information(self,'Warning','모드를 선택해주세요')
        else:
            #사진 기반으로 스타일 예측
            self.style = predict_style(self.inputImageName, model_path, args.device)
            QMessageBox.information(self,'Information',f'{self.style}로 예측되었습니다. 해당 스타일의 인플루언서를 추천드리겠습니다.')
            if (self.gender == None) or (self.size == None): 
                QMessageBox.information(self,'Warning','성별을 선택해주세요')
                QMessageBox.information(self,'Warning','체형을 선택해주세요')
            else:
                #제조자에게 추천될 인플루언서 정보
                if self.mode == 'S':
                    inf_id, inf_img = recomm_inf_sup(inf_path, self.gender, self.size, self.style)
                    pass
                #소비자에게 추천될 인플루언서 정보
                elif self.mode == 'C':
                    inf_id, inf_img = recomm_inf_cust(inf_path, self.gender, self.size, self.style)
                    pass
                # 정보를 외부 파일에 저장
                data = {}
                data['infs'] = inf_id
                data['imgs'] = inf_img
                with open(file_path, 'w') as outfile:
                    json.dump(data, outfile, indent=4)

                #새 창에서 확인하기 위해 넘어가는 과정
                ans = QMessageBox.question(self, '새 창 알림','새 창에서 결과를 확인하겠습니까?', 
                                    QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

                if ans == QMessageBox.Yes:
                    self.secondwindow = SecondClass()


#추천하는 인플루언서 정보 확인 위한 두번째 창
class SecondClass(QMainWindow, second_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.show()
        
        #외부 데이터 읽기
        file_path = "./sample.json"
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            self.inf_id = json_data['infs']
            self.inf_img = json_data['imgs']

        #이미지 보여주기
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

        #인플루언서 아이디 반환
        self.inf1.setText(self.inf_id[0])
        self.inf1.setText(self.inf_id[1])
        self.inf1.setText(self.inf_id[2])
        self.InfoText.setText('짜잔~ 뭔가 좋은 문구가 뭐 없을까')

#실행
if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = MainClass() 
    myWindow.show()
    app.exec_()