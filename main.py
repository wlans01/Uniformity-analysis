import sys ,os
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
import time

from numpy.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from result_components import ResultComponents

# 현재 버전
CURRENT_VERSION = '1.0.3'

# exe 파일을 만들었을때 경로 인식을 위한 함수
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:

        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def convert_slashes(path):
        return path.replace('/', '\\')

class MacroGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_path = None
        self.output_path = None
        self.thread = None
        self.initUI()

    def initUI(self):
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)

        self.data_result_layout = QHBoxLayout()
        self.main_layout.addLayout(self.data_result_layout)

        

        self.total_control_layout = QVBoxLayout(self.main_widget)
        self.path_widget = QWidget(self.main_widget)
        # border black
        # self.path_widget.setStyleSheet('border: 1px solid black')
        self.path_layout = QVBoxLayout(self.path_widget)
        self.data_path_layout = QHBoxLayout()
        self.data_path_label = QLabel('데이터 경로')
        self.data_path_edit = QLineEdit()
        self.data_path_edit.setReadOnly(True)
        self.data_path_button = QPushButton('Browse')
        self.data_path_layout.addWidget(self.data_path_label)
        self.data_path_layout.addWidget(self.data_path_edit)
        self.data_path_layout.addWidget(self.data_path_button)
        self.path_layout.addLayout(self.data_path_layout)

        self.data_path_button.clicked.connect(self.data_path_button_clicked)

        self.total_control_layout.addWidget(self.path_widget)

        self.control_widget = QWidget(self.main_widget)
        # border black
        # self.control_widget.setStyleSheet('border: 1px solid black')
        self.control_layout = QHBoxLayout(self.control_widget)

        self.control_button_widget = QWidget(self.main_widget)
        self.control_button_layout = QHBoxLayout(self.control_button_widget)
        self.control_button_layout.addStretch(1)
        self.start_button = QPushButton('시작')
        self.quit_button = QPushButton('종료')
        self.start_button.clicked.connect(self.start_button_clicked)
        self.quit_button.clicked.connect(self.close)
        self.control_button_layout.addWidget(self.start_button)
        self.control_button_layout.addWidget(self.quit_button)
        self.control_layout.addWidget(self.control_button_widget)

        self.total_control_layout.addWidget(self.control_widget)

        self.main_layout.addLayout(self.total_control_layout)

        self.statusBar().showMessage('데이터 경로를 설정해주세요')

        self.setWindowTitle(f' v.{CURRENT_VERSION}' )
        self.setGeometry(0, 0, self.width(), self.height())

    def data_path_button_clicked(self):
        self.data_path = QFileDialog.getOpenFileName(self, '데이터 경로', os.getcwd(), "Excel Files (*.xlsx *.xls)")
        self.data_path_edit.setText(self.data_path[0])

        if self.data_path:

            self.statusBar().showMessage('시작 버튼을 눌러주세요')

    def start_button_clicked(self):
        ''''''
        data = pd.read_excel(self.data_path[0])
        data = data.to_numpy()

        # 데이터 행 개수
        data_len = data.shape[1] -1

        sensor_position = data[:, 0]

        polynomial_number = 2
       
        for i in range(data_len):
            y = data[:, i+1]

            polynomial_data = Polynomial.fit(sensor_position, y, polynomial_number)
            polynomial_data_fit = polynomial_data(sensor_position)

            polynomial_data_max = max(polynomial_data_fit)
            polynomial_data_left = polynomial_data_fit[-1]
            polynomial_data_right = polynomial_data_fit[0]
        
            collimator_left_uniformity = uniformity(polynomial_data_left, polynomial_data_max)
            collimator_right_uniformity = uniformity(polynomial_data_right, polynomial_data_max)

    
            self.result_components = ResultComponents(f"{i+1}" ,[polynomial_data_max, polynomial_data_left, polynomial_data_right, collimator_left_uniformity, collimator_right_uniformity])
            self.data_result_layout.addWidget(self.result_components)

            plt.plot(sensor_position, y , label = f'{i+1}')
            plt.plot(sensor_position, polynomial_data_fit, label = f'{i+1} fit')
            plt.legend()

        self.statusBar().showMessage('분석 완료')

        plt.ylabel('Intensity')
        plt.xlabel('Sensor Position')
        plt.show()
 
  
    def closeEvent(self, event):
        reply =QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            
            event.accept()

        else:
            event.ignore() 

def uniformity(a, b):
    return round((((b - a) / b) * 100),3)


class ExceptionHandler:
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # PyQt5 메시지 박스 생성
        error_msg = QMessageBox()
        error_msg.setWindowTitle("에러 발생")
        error_msg.setText(f"예외 유형: {exc_type.__name__}\n메시지: {exc_value}")
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.exec_()

if __name__ == '__main__':
    from utils import extract_version

    sys.excepthook = ExceptionHandler().handle_exception
    app = QApplication(sys.argv)
    ex = MacroGui()
    extract_version.update_cheak(ex)
    ex.show()
    sys.exit(app.exec_())