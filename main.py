import sys ,os
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal ,Qt
import time

from numpy.polynomial import Polynomial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 현재 버전
CURRENT_VERSION = '1.0.1'

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

        self.data_result_layout = QVBoxLayout()
        self.main_layout.addLayout(self.data_result_layout)

        no_collimator_label = QLabel('No collimator')
        no_collimator_label.setAlignment(Qt.AlignCenter)

        no_collimator_label_layout = QHBoxLayout()

        no_collimator_left_layout = QVBoxLayout()
        no_collimator_left_label = QLabel('Left 편차%')
        self.no_collimator_left_edit = QLineEdit()
        self.no_collimator_left_edit.setReadOnly(True)
        self.no_collimator_left_edit.setStyleSheet('background-color: #c0ffc0;')

        no_collimator_left_layout.addWidget(no_collimator_left_label)
        no_collimator_left_layout.addWidget(self.no_collimator_left_edit)

        no_collimator_right_layout = QVBoxLayout()
        no_collimator_right_label = QLabel('right 편차%')
        self.no_collimator_right_edit = QLineEdit()
        self.no_collimator_right_edit.setReadOnly(True)
        self.no_collimator_right_edit.setStyleSheet('background-color: #c0ffc0;')

        no_collimator_right_layout.addWidget(no_collimator_right_label)
        no_collimator_right_layout.addWidget(self.no_collimator_right_edit)

        no_collimator_label_layout.addLayout(no_collimator_left_layout)
        no_collimator_label_layout.addLayout(no_collimator_right_layout)

        no_collimator_fit_label = QLabel('Center')
        self.no_collimator_fit_edit = QLineEdit()
        self.no_collimator_fit_edit.setReadOnly(True)
        self.no_collimator_fit_edit.setStyleSheet('background-color: #c0ffc0;')

        no_collimator_fit_label_original = QLabel('Left')
        self.no_collimator_fit_edit_original = QLineEdit()
        self.no_collimator_fit_edit_original.setReadOnly(True)
        self.no_collimator_fit_edit_original.setStyleSheet('background-color: #c0ffc0;')

        no_collimator_fit_label_original_fight = QLabel('Right')
        self.no_collimator_fit_edit_original_fight = QLineEdit()
        self.no_collimator_fit_edit_original_fight.setReadOnly(True)
        self.no_collimator_fit_edit_original_fight.setStyleSheet('background-color: #c0ffc0;')

        self.data_result_layout.addWidget(no_collimator_label)
        self.data_result_layout.addWidget(no_collimator_fit_label)
        self.data_result_layout.addWidget(self.no_collimator_fit_edit)
        self.data_result_layout.addWidget(no_collimator_fit_label_original)
        self.data_result_layout.addWidget(self.no_collimator_fit_edit_original)
        self.data_result_layout.addWidget(no_collimator_fit_label_original_fight)
        self.data_result_layout.addWidget(self.no_collimator_fit_edit_original_fight)
        self.data_result_layout.addLayout(no_collimator_label_layout)

        blank_label = QLabel(' ')
        self.data_result_layout.addWidget(blank_label)

        collimator_label = QLabel('collimator')
        collimator_label.setAlignment(Qt.AlignCenter)

        collimator_label_layout = QHBoxLayout()

        collimator_left_layout = QVBoxLayout()
        collimator_left_label = QLabel('Left 편차%')
        self.collimator_left_edit = QLineEdit()
        self.collimator_left_edit.setReadOnly(True)
        self.collimator_left_edit.setStyleSheet('background-color: #c0ffc0;')

        collimator_left_layout.addWidget(collimator_left_label)
        collimator_left_layout.addWidget(self.collimator_left_edit)

        collimator_right_layout = QVBoxLayout()
        collimator_right_label = QLabel('right 편차%')
        self.collimator_right_edit = QLineEdit()
        self.collimator_right_edit.setReadOnly(True)
        self.collimator_right_edit.setStyleSheet('background-color: #c0ffc0;')

        collimator_right_layout.addWidget(collimator_right_label)
        collimator_right_layout.addWidget(self.collimator_right_edit)

        collimator_label_layout.addLayout(collimator_left_layout)
        collimator_label_layout.addLayout(collimator_right_layout)

        collimator_fit_label = QLabel('Center')
        self.collimator_fit_edit = QLineEdit()
        self.collimator_fit_edit.setReadOnly(True)
        self.collimator_fit_edit.setStyleSheet('background-color: #c0ffc0;')

        collimator_fit_label_original = QLabel('Left')
        self.collimator_fit_edit_original = QLineEdit()
        self.collimator_fit_edit_original.setReadOnly(True)
        self.collimator_fit_edit_original.setStyleSheet('background-color: #c0ffc0;')

        collimator_fit_label_original_fight = QLabel('Right')
        self.collimator_fit_edit_original_fight = QLineEdit()
        self.collimator_fit_edit_original_fight.setReadOnly(True)
        self.collimator_fit_edit_original_fight.setStyleSheet('background-color: #c0ffc0;')

        self.data_result_layout.addWidget(collimator_label)
        self.data_result_layout.addWidget(collimator_fit_label)
        self.data_result_layout.addWidget(self.collimator_fit_edit)
        self.data_result_layout.addWidget(collimator_fit_label_original)
        self.data_result_layout.addWidget(self.collimator_fit_edit_original)
        self.data_result_layout.addWidget(collimator_fit_label_original_fight)
        self.data_result_layout.addWidget(self.collimator_fit_edit_original_fight)
        self.data_result_layout.addLayout(collimator_label_layout)

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

        sensor_position = data[:, 0]
        no_collimator = data[:, 1]
        collimator = data[:, 2]

        # polynomial fitting

        polynomial_number = 2

        polynomial_no_collimator = Polynomial.fit(sensor_position, no_collimator, polynomial_number)
        polynomial_collimator = Polynomial.fit(sensor_position, collimator, polynomial_number)

        polynomial_no_collimator_fit = polynomial_no_collimator(sensor_position)
        polynomial_collimator_fit = polynomial_collimator(sensor_position)

        # 양끝값과 중앙값 구하기
        no_collimator_max = max(polynomial_no_collimator_fit)
        no_collimator_left = polynomial_no_collimator_fit[-1]
        no_collimator_right = polynomial_no_collimator_fit[0]

        no_collimator_left_uniformity = uniformity(no_collimator_left, no_collimator_max)
        no_collimator_right_uniformity = uniformity(no_collimator_right, no_collimator_max)


        collimator_max = max(polynomial_collimator_fit)
        collimator_left = polynomial_collimator_fit[-1]
        collimator_right = polynomial_collimator_fit[0]

        collimator_left_uniformity = uniformity(collimator_left, collimator_max)
        collimator_right_uniformity = uniformity(collimator_right, collimator_max)

        

        no_collimator_fit_mean = np.mean(polynomial_no_collimator_fit)
        no_collimator_fit_std = np.std(polynomial_no_collimator_fit)

        collimator_fit_mean = np.mean(polynomial_collimator_fit)
        collimator_fit_std = np.std(polynomial_collimator_fit)

        # Calculate the mean and standard deviation for the 'collimator' column
        # collimator_mean = np.mean(collimator)
        # collimator_std = np.std(collimator)

        # no_collimator_mean = np.mean(no_collimator)
        # no_collimator_std = np.std(no_collimator)


        # # 표준편차 / 평균 = 변동계수
        # cv_no_collimator = round(((1- (no_collimator_std / no_collimator_mean)) * 100),2)
        # cv_collimator = round(((1-(collimator_std / collimator_mean)) * 100),2)
        
      
        # # 피팅 데이터 균일도
        # # no collimator
        # cv_no_collimator_fit = round(((1- (no_collimator_fit_std / no_collimator_fit_mean)) * 100),2)
        # cv_collimator_fit = round(((1-(collimator_fit_std / collimator_fit_mean)) * 100),2)

        self.update_data([no_collimator_max, no_collimator_left, no_collimator_right, no_collimator_left_uniformity, no_collimator_right_uniformity,collimator_max,collimator_left,collimator_right,collimator_left_uniformity,collimator_right_uniformity])

        # 그래프 그리기
        plt.subplot(1, 3, 1)
        plt.plot(sensor_position, no_collimator, 'r-', label='no collimator')
        plt.plot(sensor_position, polynomial_no_collimator_fit, 'r--', label='no collimator fit')
        plt.plot(sensor_position, collimator, 'b-', label='collimator')
        plt.plot(sensor_position, polynomial_collimator_fit, 'b--', label='collimator fit')
        plt.legend()

        plt.subplot(1, 3, 2)
        plt.plot(sensor_position, no_collimator, 'r-', label='no collimator')
        plt.plot(sensor_position, polynomial_no_collimator_fit, 'r--', label='no collimator fit')
        plt.hlines(no_collimator_fit_mean,sensor_position[0],sensor_position[-1], colors='gray', linestyles='dashed', label='no collimator mean')
        plt.legend()

        plt.subplot(1, 3, 3)
        plt.plot(sensor_position, collimator, 'b-', label='collimator')
        plt.plot(sensor_position, polynomial_collimator_fit, 'b--', label='collimator fit')
        plt.hlines(collimator_fit_mean,sensor_position[0],sensor_position[-1], colors='gray', linestyles='dashed', label='collimator mean')
        plt.legend()

        plt.show()

        # Calculate the mean and standard deviation for the 'no collimator' column
       

        # # Plotting the 'no collimator' data
        # plt.figure(figsize=(12, 6))
        # plt.plot(sensor_position, no_collimator, label='No Collimator', color='blue')
        # plt.axhline(y=no_collimator_mean, color='red', linestyle='--', label=f'Mean: {no_collimator_mean:.2e}')
        # plt.fill_between(sensor_position, no_collimator_mean - no_collimator_std, no_collimator_mean + no_collimator_std, color='grey', alpha=0.5, label=f'Std Dev: {no_collimator_std:.2e}')

        # plt.xlabel('Sensor position')
        # plt.ylabel('Intensity')
        # plt.title('No Collimator')
        # plt.legend()
        # plt.grid(True)
        # plt.show()
        
        

        # # Plotting the 'collimator' data
        # plt.figure(figsize=(12, 6))
        # plt.plot(sensor_position, collimator, label='Collimator', color='blue')
        # plt.axhline(y=collimator_mean, color='red', linestyle='--', label=f'Mean: {collimator_mean:.2e}')
        # plt.fill_between(sensor_position, collimator_mean - collimator_std, collimator_mean + collimator_std, color='grey', alpha=0.5, label=f'Std Dev: {collimator_std:.2e}')

        # plt.xlabel('Sensor position')
        # plt.ylabel('Intensity')
        # plt.title('Collimator')
        # plt.legend()
        # plt.grid(True)
        # plt.show()
            

    def update_data(self, data):
        self.no_collimator_fit_edit.setText(str(data[0]))
        self.no_collimator_fit_edit_original.setText(str(data[1]))
        self.no_collimator_fit_edit_original_fight.setText(str(data[2]))
        self.no_collimator_left_edit.setText(str(data[3]))
        self.no_collimator_right_edit.setText(str(data[4]))

        self.collimator_fit_edit.setText(str(data[5]))
        self.collimator_fit_edit_original.setText(str(data[6]))
        self.collimator_fit_edit_original_fight.setText(str(data[7]))
        self.collimator_left_edit.setText(str(data[8]))
        self.collimator_right_edit.setText(str(data[9]))
       
        self.statusBar().showMessage('데이터 처리가 완료되었습니다.')
  
    def closeEvent(self, event):
        reply =QMessageBox.question(self, 'Message', 'Are you sure to quit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            
            event.accept()

        else:
            event.ignore() 

def uniformity(a, b):
    return round((((b - a) / b) * 100),2)


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