from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class CenteredButtonDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setStyleSheet("color: black; font-size: 16px;")  # 라벨에 스타일시트 적용
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_btn = QPushButton("확인")
        ok_btn.setStyleSheet("""
            background-color: #e0e0e0;
            color: black;
            border: none;
            padding: 10px;
            min-width: 100px;
        """)
        ok_btn.clicked.connect(self.accept)
        button_layout.addWidget(ok_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        self.setLayout(layout)
