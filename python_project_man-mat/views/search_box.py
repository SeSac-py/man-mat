from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

class SearchBoxView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        layout = QVBoxLayout()

        # 상단 설정 버튼 및 analyze 버튼
        top = QHBoxLayout()
        top.addStretch()
        self.setting_btn = QPushButton()
        self.setting_btn.setIcon(QIcon("resources/icons/settings.png"))
        self.setting_btn.setIconSize(QSize(32, 32))
        self.setting_btn.setToolTip("설정")
        self.setting_btn.setStyleSheet("background-color: transparent; border: none; margin-top: 3px; margin-right: 3px;")

        self.analyze_btn = QPushButton()
        self.analyze_btn.setIcon(QIcon("resources/icons/analyze.png"))
        self.analyze_btn.setIconSize(QSize(32, 32))
        self.analyze_btn.setToolTip("분석")
        self.analyze_btn.setStyleSheet("background-color: transparent; border: none; margin-top: 3px; margin-right: 3px;")
        self.analyze_btn.clicked.connect(self.show_analyze2)

        top.addStretch()
        top.addWidget(self.setting_btn)
        top.addWidget(self.analyze_btn)
        layout.addLayout(top)

        # 중앙 검색창 및 버튼
        mid = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("검색어를 입력하세요")
        self.search_edit.setMinimumSize(300, 40)
        self.search_edit.setStyleSheet("border: 2px solid black; border-radius: 10px; color: black;")
        self.search_btn = QPushButton()
        self.search_btn.setIcon(QIcon("resources/icons/search.png"))
        self.search_btn.setIconSize(QSize(40, 40))
        self.search_btn.setStyleSheet("background-color: black; border: 5px solid black; border-radius: 5px;")
        mid.addWidget(self.search_edit)
        mid.addWidget(self.search_btn)
        layout.addStretch()
        layout.addLayout(mid)
        layout.addStretch()
        self.setLayout(layout)
        self.setting_btn.clicked.connect(self.goto_setting)

    def goto_setting(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(2)  # Setting Window로 이동

    def show_analyze2(self):
        # Analyze2 창 표시 (실제로는 QWidget이나 QDialog로 구현)
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
        analyze2 = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("분석 결과"))
        layout.addWidget(QTextEdit("Analyze2 화면 내용"))
        analyze2.setLayout(layout)
        analyze2.setWindowTitle("분석 결과")
        analyze2.resize(400, 300)
        analyze2.show()
