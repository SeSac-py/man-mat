from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class ResultView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
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
        # 문제 풀기 버튼
        self.btn_solve = QPushButton("정보 보안 기사 문제 풀기")
        self.btn_solve.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: none;
                padding: 50px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
        """)
        self.btn_solve.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 문제 만들기 버튼
        self.btn_create = QPushButton("정보 보안 기사 문제 만들기")
        self.btn_create.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: none;
                padding: 50px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
        """)
        self.btn_create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.btn_solve)
        layout.addWidget(self.btn_create)
        self.setLayout(layout)
        self.btn_solve.clicked.connect(self.goto_result1)
        self.btn_create.clicked.connect(self.goto_result21)  # 이 부분 추가

    def go_back(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)  # SearchBoxView로 이동

    def goto_result1(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(4)  # Result1View로 이동

    def goto_result21(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(8)  # Result21View 인덱스로 이동 (실제 인덱스 맞춰주세요)
