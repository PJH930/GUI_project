import os
import subprocess

import sys
import time
from distutils.dir_util import copy_tree
from time import sleep
import cv2
from PyQt5.QtCore import QProcess, QBasicTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import run
from easyocr import config as ms
from trainer.craft import eval as ev

class WorkerThread(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        for _ in range(self.duration):
            time.sleep(1)
        self.finished_signal.emit()


# test
eval_data_set = ""
seved_model_set = ""

# create_imdb_dataset
inputPath_set = ""
gtFile_set = ""
outputPath_set = ""

# modelpath-eval set
model_set = ""

def pathSet():
    global eval_data_set, seved_model_set, inputPath_set, gtFile_set, outputPath_set
    path_list = []
    path_list.append(eval_data_set)
    path_list.append(seved_model_set)
    path_list.append(inputPath_set)
    path_list.append(gtFile_set)
    path_list.append(outputPath_set)
    return path_list


def result_img_path(path):
    global model_result_img_path
    model_result_img_path = path


form_class = uic.loadUiType("GUI_project_16.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

#   ----------------------------↓↓↓변수↓↓↓-----------------------------------
        # 모델
        self.model_path = ""
        self.g_model = None
        # 데이터셋 파일 저장 리스트
        self.dataset_list_dir = ""
        # 데이터셋 적용폴더 저장 리스트
        self.dataset_dir = ""
        # 결과폴더 절대경로
        self.result_dir = ""
        # 텍스트 데이터 모든파일의 절대경로
        self.text_all_list = []
        # 그림 데이터 모든파일의 절대경로
        self.img_all_list = []
        # 화면에 표시된 데이터셋 파일과 결과파일의 절대값 주소
        self.original_img = ""
        self.original_img_split = ""
        self.result_img = ""
        self.result_img_split = ""
        # treeView 목록 파일을 클릭하면 그 파일의 절대값을 저장
        self.tree_View_file_click = ""
        # 더블클릭 한 이미지
        self.img_select = []
        # 결과이미지 경로
        self.result_img_path = ""
        # setting탭
        self.eval_data_get = ""
        self.seved_model_get = ""
        self.inputPath_get = ""
        self.gtFile_get = ""
        self.outputPath_get = ""
        # 프로그래스바
        self.worker_thread = None
        # self.progressBar.hide()

#   ----------------------------↑↑↑변수↑↑↑-----------------------------------

#   ----------------------------↓↓↓버튼↓↓↓-----------------------------------

        # 모델 선택
        self.pushButton_1.clicked.connect(self.modelSelect)
        # 데이터셋 폴더
        self.pushButton_2.clicked.connect(self.datasetDirSelect)
        # 스타트버튼
        self.start_button.clicked.connect(self.runFile)
        # 리셋
        self.pushButton_5.clicked.connect(self.reset)
        # setting 버튼
        self.pushButton_eval.clicked.connect(self.evalPath)
        self.pushButton_seved.clicked.connect(self.sevedModel)
        self.pushButton_inputPath.clicked.connect(self.inputPath)
        self.pushButton_gtFile.clicked.connect(self.gtFile)
        self.pushButton_outputPath.clicked.connect(self.outputPath)
        self.pushButton_setting.clicked.connect(self.setting)

#   ----------------------------↑↑↑버튼↑↑↑-----------------------------------

#   ----------------------------↓↓↓함수↓↓↓-----------------------------------
    # 모델위치 선택 함수
    def modelSelect(self, pyqtExceptionHandler=None):
        global model_path, model_set

        file_path = QFileDialog.getOpenFileNames(self, "Select Files")[0]
        self.model_path = file_path[0]
        model_split = file_path[0].split("/")[-1]
        self.g_model = model_split
        model_set = self.model_path
        ev.path_get('../EasyOCR/trainer/craft/workspace/model/CRAFT_clr_amp_25000_clova_02_14.pth')

        model_path_url = f'D:/makeitreal/PYTHON(PYG)/nextdoor/dataset/projectdata/EasyOCR/trainer/craft/workspace/model/{model_split}'
        model_md5sum = {
            'craft_mlt_25k.pth': '2f8227d2def4037cdb3b34389dcf9ec1',
            'CRAFT_clr_amp_25000_clova_02_14.pth': '41e8c89e45d071d9f6cf14540a1e948e',
            'craft_pyg.pth': '15bc31af6bb99a623ea718b0691e6fa6'
        }
        ms.model_select(model_split, model_path_url, model_md5sum[model_split])
        sys.excepthook = pyqtExceptionHandler

    # 데이터셋이 들어있는 폴더를 선택하는 함수
    def datasetDirSelect(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.dataset_list_dir = file_path
        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(file_path)
        self.model_file_system.setReadOnly(False)
        self.treeView.setModel(self.model_file_system)
        self.treeView.setRootIndex(self.model_file_system.index(file_path))
        self.treeView.doubleClicked.connect(lambda index: self.treeViewDoubleClicked1(index))
        self.treeView.setDragEnabled(True)
        self.treeView.setColumnWidth(0, 300)

        sys.excepthook = pyqtExceptionHandler

    # treeView 더블클릭 시 절대값 추출함수
    def treeViewDoubleClicked1(self, index, pyqtExceptionHandler=None):
        self.tree_View_file_click = self.model_file_system.filePath(index)
        self.original_img = self.tree_View_file_click
        self.original_img_split = self.original_img.split("/")[-1]
        self.img_select.clear()
        self.img_select.append(self.original_img_split)
        run.choose_image(self.img_select)
        print(self.img_select)
        pixmap = QPixmap(self.tree_View_file_click)
        pixmap = pixmap.scaled(self.label_D.size(), aspectRatioMode=True)
        self.label_D.setPixmap(pixmap)
        # self.runFile()
        # eval_run = subprocess.run(["python", "../EasyOCR/trainer/craft/eval.py"], capture_output=True)
        # result = eval_run.stdout.decode()
        # result_split = result.split('\n')[-2]
        # self.label_precision.setText(eval(result_split)['precision'])
        # self.label_recall.setText(eval(result_split)['recall'])
        # self.label_hmean.setText(eval(result_split)['hmean'])
        # self.msg_box_end()
        sys.excepthook = pyqtExceptionHandler

    def treeViewDoubleClicked2(self, index, pyqtExceptionHandler=None):
        self.tree_View_file_click = self.model_file_system.filePath(index)
        self.result_img = self.tree_View_file_click
        pixmap = QPixmap(self.tree_View_file_click)
        pixmap = pixmap.scaled(self.label_R.size(), aspectRatioMode=True)
        self.label_R.setPixmap(pixmap)

        sys.excepthook = pyqtExceptionHandler

    # 실행버튼 함수
    def runFile(self, pyqtExceptionHandler=None):
        global model_result_img_path
        if self.g_model == None:
            self.msg_model_none()
        else:
            self.start_thread()
            run.detection_recogintion('nextdoor')
            eval_run = subprocess.run(["python", "../EasyOCR/trainer/craft/eval.py"], capture_output=True)
            print(eval_run)
            result = eval_run.stdout.decode()
            print(result)
            result_split = result.split('\n')[-2]
            self.label_precision.setText(eval(result_split)['precision'])
            self.label_recall.setText(eval(result_split)['recall'])
            self.label_hmean.setText(eval(result_split)['hmean'])
            self.showCvImage(run.show_img)
            self.msg_box_end()
        sys.excepthook = pyqtExceptionHandler

    def msg_box_end(self):
        msg = QMessageBox()
        msg.setWindowTitle("Detection")
        msg.setText('완료')
        msg.exec_()

    def msg_model_none(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText('model 파일이 없습니다.')
        msg.exec_()
        
    def showCvImage(self, cv_image):
        height, width, channel = cv_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.label_D.size(), aspectRatioMode=True)
        self.label_D.setPixmap(pixmap)

    # 데이터셋을 적용할 폴더 선택 함수
    def datasetDir(self):
        directory_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.dataset_dir = directory_path

    def reset(self):
        self.label_D.clear()
        self.label_R.clear()
        self.label_precision.clear()
        self.label_recall.clear()
        self.label_hmean.clear()
        self.label_eval.clear()
        self.label_seved.clear()
        self.label_inputPath.clear()
        self.label_gtFile.clear()
        self.label_outputPath.clear()
        self.progressBar.hide()

    # setting tap------------
    def setting(self, pyqtExceptionHandler=None):
        global eval_data_set, seved_model_set, inputPath_set, gtFile_set ,outputPath_set
        eval_data_set = self.eval_data_get
        seved_model_set = self.seved_model_get
        inputPath_set = self.inputPath_get
        gtFile_set = self.gtFile_get
        outputPath_set = self.outputPath_get
        # self.process = QProcess(self)
        # self.process.start("python", ["../deep-text-recognition/test.py"])
        # self.process.start("python", ["./deep-text-recognition/create_lmdb_dataset.py"])
        subprocess.run(["python", "../deep-text-recognition/test.py"], capture_output=True)
        subprocess.run(["python", "../deep-text-recognition/create_lmdb_dataset.py"], capture_output=True)
        sys.excepthook = pyqtExceptionHandler

    def evalPath(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.eval_data_get = file_path
        self.label_eval.setText(self.eval_data_get)
        sys.excepthook = pyqtExceptionHandler
    def sevedModel(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        self.seved_model_get = file_path
        self.label_seved.setText(self.seved_model_get)
        sys.excepthook = pyqtExceptionHandler
    def inputPath(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.inputPath_get = file_path
        self.label_inputPath.setText(self.inputPath_get)
        sys.excepthook = pyqtExceptionHandler
    def gtFile(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        self.gtFile_get = file_path
        self.label_gtFile.setText(self.gtFile_get)
        sys.excepthook = pyqtExceptionHandler
    def outputPath(self, pyqtExceptionHandler=None):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.outputPath_get = file_path
        self.label_outputPath.setText(self.outputPath_get)
        sys.excepthook = pyqtExceptionHandler
    # setting tap------------end



    def start_thread(self):
        if self.worker_thread is not None and self.worker_thread.isRunning():
            return

        self.progressBar.show()
        self.start_button.setEnabled(False)

        self.worker_thread = WorkerThread(10)  # Set the duration of the task
        self.worker_thread.finished_signal.connect(self.thread_finished)
        self.worker_thread.start()

    def thread_finished(self):
        self.progressBar.hide()
        self.start_button.setEnabled(True)

#   ----------------------------↑↑↑함수↑↑↑-----------------------------------

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


