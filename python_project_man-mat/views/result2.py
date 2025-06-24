from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

class Result2View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # 문제 정보
        info = QLabel("Q. RAID를 패리티비트로 사용하며\n분산저장하는 방법을\n방식으로 쓰는 RAID는?")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("font-size: 20px;")
        layout.addWidget(info)

        # 객관식 선택지
        self.options = QListWidget()
        for text in ["RAID 0", "RAID 1", "RAID 5", "RAID 10"]:
            item = QListWidgetItem(text)
            self.options.addItem(item)
        layout.addWidget(self.options)

        # 삭제 버튼
        self.del_btn = QPushButton("삭제")
        self.del_btn.setStyleSheet("background: #ff4444; color: white; font-size: 16px;")
        layout.addWidget(self.del_btn)

        # 네비게이션(좌우 화살표)
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(30)

        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(QIcon("resources/icons/left.png"))
        self.prev_btn.setIconSize(QSize(40, 40))
        self.prev_btn.setFixedSize(60, 60)
        self.prev_btn.setStyleSheet("background: transparent; border: none;")

        self.next_btn = QPushButton()
        self.next_btn.setIcon(QIcon("resources/icons/right.png"))
        self.next_btn.setIconSize(QSize(40, 40))
        self.next_btn.setFixedSize(60, 60)
        self.next_btn.setStyleSheet("background: transparent; border: none;")

        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)

        self.setLayout(layout)
