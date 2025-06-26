from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

def get_wrong_question_message(wrong_indices):
    count = len(wrong_indices)
    if count == 0:
        return "perfect score"
    elif count > 3:
        return f"{count}개 틀렸습니다"
    else:
        return "틀린 문항: " + ", ".join(str(i) for i in wrong_indices)

class Analyze(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        self.setFixedSize(width, height)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(10)

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
        self.container_layout.addLayout(top)

        # 2. 분석 아이콘 (중앙정렬)
        icon_layout = QVBoxLayout()
        icon_layout.setAlignment(Qt.AlignHCenter)
        self.analyze_icon = QLabel()
        self.analyze_icon.setPixmap(QIcon("resources/icons/analyze.png").pixmap(QSize(70, 70)))
        self.analyze_icon.setStyleSheet("margin: 0px; padding: 0px;")
        self.analyze_icon.setAlignment(Qt.AlignHCenter)
        icon_layout.addWidget(self.analyze_icon)
        self.container_layout.addLayout(icon_layout)

        # 3. SCORE 텍스트 (검은색)
        self.score_label = QLabel("Best Score")
        self.score_label.setAlignment(Qt.AlignHCenter)
        self.score_label.setFont(QFont("Arial", 14))
        self.score_label.setStyleSheet("color: black; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(self.score_label)

        # 4. 점수 라벨 (빨간색, 크게)
        self.score_value = QLabel("")
        self.score_value.setAlignment(Qt.AlignHCenter)
        self.score_value.setFont(QFont("Arial", 22, QFont.Bold))
        self.score_value.setStyleSheet("color: red; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(self.score_value)

        # 5. 틀린 문항 메시지
        self.wrong_msg_label = QLabel()
        self.wrong_msg_label.setAlignment(Qt.AlignHCenter)
        self.wrong_msg_label.setFont(QFont("Arial", 14))
        self.wrong_msg_label.setStyleSheet("color: black; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(self.wrong_msg_label)

        # 6. 부족한 분야 (검은색)
        lack_label = QLabel("부족한 분야")
        lack_label.setStyleSheet("color: black; font-size: 14px; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(lack_label)
        self.lack_text = QTextEdit("4줄 요약 1\n4줄 요약 2\n4줄 요약 3\n4줄 요약 4")
        self.lack_text.setReadOnly(True)
        self.lack_text.setMinimumHeight(60)
        self.lack_text.setStyleSheet("color: black; font-size: 14px;")
        self.container_layout.addWidget(self.lack_text)

        # 7. 개선하면 좋을 점 (검은색)
        improve_label = QLabel("개선하면 좋을 점")
        improve_label.setStyleSheet("color: black; font-size: 14px; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(improve_label)
        self.improve_text = QTextEdit("개선점 1\n개선점 2\n개선점 3\n4줄 요약 4")
        self.improve_text.setReadOnly(True)
        self.improve_text.setMinimumHeight(60)
        self.improve_text.setStyleSheet("color: black; font-size: 14px;")
        self.container_layout.addWidget(self.improve_text)

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # 틀린 문항 리스트 (초기값)
        self.wrong_indices = []

    def update_score(self, score, wrong_indices=None):
        self.score_label.setText("Best Score")
        self.score_value.setText(str(score))
        if wrong_indices is not None:
            self.wrong_indices = wrong_indices
        self.wrong_msg_label.setText(get_wrong_question_message(self.wrong_indices))

    def show_best_score(self, score, wrong_indices=None):
        self.score_label.setText("Best Score")
        self.score_value.setText(str(score))
        if wrong_indices is not None:
            self.wrong_indices = wrong_indices
        self.wrong_msg_label.setText(get_wrong_question_message(self.wrong_indices))

    def go_back(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)  # SearchBoxView로 이동
