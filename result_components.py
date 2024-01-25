import sys ,os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ResultComponents(QWidget):
    def __init__(self , name , result):
        super().__init__()
        self.name = name
        self.result = result

        self.initUI()

    def initUI(self):

        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.frame.setLineWidth(1)
        self.main_layout = QVBoxLayout()

        self.components_name_label = QLabel(self.name)
        self.components_name_label.setAlignment(Qt.AlignCenter)
        # 글씨 크게 만들기
        font = self.components_name_label.font()
        font.setPointSize(15)
        self.components_name_label.setFont(font)

        self.center_label = QLabel("Center")
        self.center_edit = QLineEdit()
        self.center_edit.setReadOnly(True)
        self.center_edit.setStyleSheet('background-color: #c0ffc0;')
        self.center_edit.setText("{:.3e}".format(self.result[0]))

        self.left_label = QLabel("Left")
        self.left_edit = QLineEdit()
        self.left_edit.setReadOnly(True)
        self.left_edit.setStyleSheet('background-color: #c0ffc0;')
        self.left_edit.setText("{:.3e}".format(self.result[1]))

        self.right_label = QLabel("Right")
        self.right_edit = QLineEdit()
        self.right_edit.setReadOnly(True)
        self.right_edit.setStyleSheet('background-color: #c0ffc0;')
        self.right_edit.setText("{:.3e}".format(self.result[2]))

        self.deviation_layout = QHBoxLayout()

        self.left_deviation_layout = QVBoxLayout()
        self.left_deviation_label = QLabel("Left %")
        self.left_deviation_edit = QLineEdit()
        self.left_deviation_edit.setReadOnly(True)
        self.left_deviation_edit.setStyleSheet('background-color: #c0ffc0;')
        self.left_deviation_edit.setText(str(self.result[3]))

        self.left_deviation_layout.addWidget(self.left_deviation_label)
        self.left_deviation_layout.addWidget(self.left_deviation_edit)

        self.right_deviation_layout = QVBoxLayout()
        self.right_deviation_label = QLabel("Right %")
        self.right_deviation_edit = QLineEdit()
        self.right_deviation_edit.setReadOnly(True)
        self.right_deviation_edit.setStyleSheet('background-color: #c0ffc0;')
        self.right_deviation_edit.setText(str(self.result[4]))

        self.right_deviation_layout.addWidget(self.right_deviation_label)
        self.right_deviation_layout.addWidget(self.right_deviation_edit)

        self.deviation_layout.addLayout(self.left_deviation_layout)
        self.deviation_layout.addLayout(self.right_deviation_layout)


        self.main_layout.addWidget(self.components_name_label)
        self.main_layout.addWidget(self.center_label)
        self.main_layout.addWidget(self.center_edit)
        self.main_layout.addWidget(self.left_label)
        self.main_layout.addWidget(self.left_edit)
        self.main_layout.addWidget(self.right_label)
        self.main_layout.addWidget(self.right_edit)
        self.main_layout.addLayout(self.deviation_layout)

        self.frame.setLayout(self.main_layout)
        top_level_layout = QVBoxLayout(self) 
        top_level_layout.addWidget(self.frame) 

        self.adjustSize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ResultComponents("name" , ["value1","value2","value3","value4","value5"])
    ex.show()
    sys.exit(app.exec_())