from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class SettingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        layout = QVBoxLayout()
        # 오른쪽 상단 뒤로가기 버튼
        top = QHBoxLayout()
        top.addStretch()
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon("resources/icons/back.png"))
        self.back_btn.setIconSize(QSize(32, 32))
        self.back_btn.setToolTip("뒤로가기")
        self.back_btn.setStyleSheet("background-color: transparent; border: none; margin-top: 3px; margin-right: 3px;")
        self.back_btn.clicked.connect(self.go_back)
        top.addWidget(self.back_btn)
        layout.addLayout(top)
        layout.addWidget(QLabel("설정 / 분석모드 / 다크모드"))
        self.check1 = QCheckBox("저장 / 불러오기")
        self.check2 = QCheckBox("분석 모드")
        self.check3 = QCheckBox("다크 모드")
        layout.addWidget(self.check1)
        layout.addWidget(self.check2)
        layout.addWidget(self.check3)
        self.setLayout(layout)
        self.setStyleSheet("QLabel, QCheckBox { color: black; }")

    def go_back(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)  # SearchBoxView로 이동
