import os
import shutil
import subprocess
import sys
from datetime import time
from distutils.dir_util import copy_tree

import cv2

import qdarkstyle
from PyQt5.QtCore import QProcess, pyqtSignal, QSize, QModelIndex
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.Qt import Qt
import matplotlib.pyplot as plt
from click import command
from isapi.threaded_extension import WorkerThread

# from PyQt5.QtWidgets.QGridLayout import setGeometry

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("GUI_project.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        # setFixedSize : 윈도우 창 사이즈 고정하기
        # self.setFixedSize(QSize(780, 460))
        self.setupUi(self)

        # 실행 파일의 절대값을 저장 리스트
        self.open_list = []

        # 데이터셋 파일 저장 리스트
        self.dataset_list_dir = []

        # 데이터셋 적용폴더 저장 리스트
        self.dataset_dir = []

        # 텍스트 데이터 모든파일의 절대경로
        self.text_all_list = []

        # 그림 데이터 모든파일의 절대경로
        self.img_all_list = []


        # ======test
        # self.tree_view = QTreeView()
        # self.setCentralWidget(self.tree_view)
        #
        # self.file_system_model = QFileSystemModel()
        # self.file_system_model.setRootPath("")
        # self.tree_view.setModel(self.file_system_model)
        # self.tree_view.setRootIndex(self.file_system_model.index(""))
        #
        # self.tree_view.doubleClicked.connect(self.item_double_clicked)
        # ======





        # 모델/데이터셋 불러오기 버튼
        self.pushButton_1.clicked.connect(self.attachFile_1)
        self.pushButton_2.clicked.connect(self.attachFile_2)

        # open_list에 저장해둔 파일 실행하는버튼
        self.pushButton_3.clicked.connect(self.runFile)

        # 데이터셋을 복사
        self.pushButton_4.clicked.connect(self.datasetDir)

        # 결과확인 버튼 test
        # self.pushButton_result.clicked.connect(self.result)





#   ----------------------------↓↓↓텍스트 검출 함수들↓↓↓-----------------------------------
    # 모델위치 선택 함수
    def attachFile_1(self):
        # QFileDialog() : 파일 선택상자 열기
        # .setText() : 텍스트 출력
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        self.textEdit_1.setText(file_path)
        self.open_list[0] = file_path
        print('Selected File:', file_path)

    # 데이터셋이 들어있는 폴더를 선택하는 함수
    def attachFile_2(self):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.textEdit_2.setText(file_path)
        self.dataset_list_dir[0] = file_path
        print('Selected Dir:', file_path)
        # 선택한 데이터셋 폴더 안의 파일들을 전부 file_list에 저장 후 textEdit에 보여줌
        file_list = os.listdir(file_path)
        self.textEdit.clear()
        for file in file_list:
            exist = self.textEdit.toPlainText()
            self.textEdit.setText(f'{exist} {file}\n')

    # 실행버튼 함수
    def runFile(self):
        # 분석할 데이터셋폴더 파일들을 >> 덮어쓰기 >> 모델 데이터셋 폴더로
        copy_tree(self.dataset_list_dir[0], self.dataset_dir[0])
        # 모델의 실행파일을 실행
        file_path = self.open_list[0]
        process = QProcess(self)
        process.start('python', [file_path])

    # 데이터셋을 적용할 폴더 선택 함수
    def datasetDir(self):
        directory_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.textEdit_4.setText(directory_path)
        self.dataset_dir[0] = directory_path

    # ======test
    # def item_double_clicked(self, index: QModelIndex):
    #     file_path = self.file_system_model.filePath(index)
    #
    #     print("Double clicked:", file_path)
    # ======
#   ----------------------------↑↑↑텍스트 검출 함수들↑↑↑-----------------------------------







#   ----------------------------↓↓↓이미지 검출 함수들↓↓↓-----------------------------------
#   ----------------------------↑↑↑이미지 검출 함수들↑↑↑-----------------------------------








if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
