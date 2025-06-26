from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize  

class ProblemSet(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        # 문제 입력창과 delete 버튼을 가로로 배치
        problem_row = QHBoxLayout()
        self.problem_edit = QTextEdit()
        self.problem_edit.setPlaceholderText("문제 입력")
        self.problem_edit.setStyleSheet("font-size: 16px; color: black;")
        self.problem_edit.setMinimumHeight(60)
        problem_row.addWidget(self.problem_edit, stretch=1)  # 문제 입력창이 늘어남

        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon("resources/icons/delete.png"))
        self.delete_btn.setIconSize(QSize(25, 25))
        self.delete_btn.setStyleSheet("border: none;")
        problem_row.addWidget(self.delete_btn)
        layout.addLayout(problem_row)

        # 답안 입력창
        self.answer_edit = QTextEdit()
        self.answer_edit.setPlaceholderText("모범 답안 입력")
        self.answer_edit.setStyleSheet("font-size: 16px; color: black;")
        self.answer_edit.setMinimumHeight(60)
        layout.addWidget(self.answer_edit)

        self.setLayout(layout)
