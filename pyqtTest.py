import shutil
import subprocess
import sys
from datetime import time

import qdarkstyle
from PyQt5.QtCore import QProcess, pyqtSignal, QSize
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
from click import command
from isapi.threaded_extension import WorkerThread

# from PyQt5.QtWidgets.QGridLayout import setGeometry

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("qt2.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        # setFixedSize : 윈도우 창 사이즈 고정하기
        self.setFixedSize(QSize(780, 460))
        self.setupUi(self)

        # 실행 파일의 절대값을 저장 리스트
        self.open_list = ["", ""]

        # 데이터셋 파일 저장 리스트
        self.dataset_list = []

        # 데이터셋 적용폴더 저장 리스트
        self.dataset_dir = [""]

        # 모델/데이터셋 불러오기 버튼
        self.pushButton_1.clicked.connect(self.attachFile_1)
        self.pushButton_2.clicked.connect(self.attachFile_2)

        # open_list에 저장해둔 파일 실행하는버튼
        self.pushButton_3.clicked.connect(self.runFile)

        # 데이터셋을 복사
        self.pushButton_4.clicked.connect(self.datasetDir)


    # 모델위치 지정 함수
    def attachFile_1(self):
        # QFileDialog() : 파일 선택상자 열기
        # .setText() : 텍스트 출력
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        self.textEdit_1.setText(file_path)
        self.open_list[0] = file_path
        print('Selected File:', file_path)

    # 데이터셋 위치 지정 함수
    def attachFile_2(self):
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        self.textEdit_2.setText(file_path)
        self.open_list[1] = file_path
        # if file_path:
        print('Selected File:', file_path)

    # 실행버튼 함수
    def runFile(self):
        # 데이터셋을 모델데이터셋 적용 파일로 먼저 이동
        shutil.copy(self.open_list[1], self.dataset_dir[0])
        # 모델의 실행파일을 실행
        file_path = self.open_list[0]
        process = QProcess(self)
        process.start('python', [file_path])

    # 데이터셋을 적용할 폴더 선택 함수
    def datasetDir(self):
        directory_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.textEdit_4.setText(directory_path)
        self.dataset_dir[0] = directory_path


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()