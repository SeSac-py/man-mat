from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class SettingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        
        # 메인 레이아웃 (전체)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 1. 뒤로가기 버튼 (상단 오른쪽에 배치)
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

        # 2. 설정 아이콘 (중앙정렬)
        icon_layout = QVBoxLayout()
        icon_layout.setAlignment(Qt.AlignHCenter)
        self.analyze_icon = QLabel()
        self.analyze_icon.setPixmap(QIcon("resources/icons/settings.png").pixmap(QSize(70, 70)))
        self.analyze_icon.setStyleSheet("margin: 0px; padding: 0px;")
        self.analyze_icon.setAlignment(Qt.AlignHCenter)
        icon_layout.addWidget(self.analyze_icon)
        layout.addLayout(icon_layout)

        # 3. 체크박스 (설정 옵션, 중앙정렬)
        self.check1 = QCheckBox("저장 · 불러오기")
        self.check2 = QCheckBox("분석 모드")
        self.check3 = QCheckBox("다크 모드")
        layout.addWidget(self.check1, alignment=Qt.AlignHCenter)
        layout.addWidget(self.check2, alignment=Qt.AlignHCenter)
        layout.addWidget(self.check3, alignment=Qt.AlignHCenter)

        # 4. 하단 버튼 (재설정, 확인)
        bottom = QHBoxLayout()
        # 하단 좌측 재설정 버튼 (1/2)
        self.reset_btn = QPushButton("재설정")
        self.reset_btn.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            padding: 0px;
            margin-top: 15px;
            text-align: center;
        """)
        self.reset_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        bottom.addWidget(self.reset_btn)
        # 하단 우측 확인 버튼 (1/2)
        self.ok_btn = QPushButton("확인")
        self.ok_btn.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            padding: 0px;
            margin-top: 15px;
            text-align: center;
        """)
        self.ok_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.ok_btn.clicked.connect(self.go_back)
        bottom.addWidget(self.ok_btn)
        layout.addLayout(bottom)

        self.setLayout(layout)
        self.setStyleSheet("QLabel, QCheckBox { color: black; }")

    def go_back(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)  # SearchBoxView로 이동
