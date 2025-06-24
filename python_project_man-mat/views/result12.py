from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Result12View(QWidget):
    def __init__(self, user_answers, correct_answers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("man-mat")
        self.user_answers = user_answers
        self.correct_answers = correct_answers
        self.score = self.calculate_score()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # SCORE 텍스트
        score_label = QLabel("SCORE")
        score_label.setAlignment(Qt.AlignHCenter)
        score_label.setFont(QFont("Arial", 18))
        score_label.setStyleSheet(" color:black; ")
        layout.addWidget(score_label)

        # 점수(빨간색, 크게)
        score_value = QLabel(str(self.score))
        score_value.setAlignment(Qt.AlignHCenter)
        score_value.setFont(QFont("Arial", 48, QFont.Bold))
        score_value.setStyleSheet("color: red;")
        layout.addWidget(score_value)

        # 버튼들 (분석하기, 다시하기, 종료, 저장)
        btn_font = QFont("Arial", 16)
        self.analyze_btn = QPushButton("분석 하기")
        self.analyze_btn.setFont(btn_font)
        self.analyze_btn.setStyleSheet("color: black; background: white; border: none;")
        layout.addWidget(self.analyze_btn)

        self.retry_btn = QPushButton("다시 하기")
        self.retry_btn.setFont(btn_font)
        self.retry_btn.setStyleSheet("color: black; background: white; border: none;")
        layout.addWidget(self.retry_btn)

        self.end_btn = QPushButton("종료")
        self.end_btn.setFont(btn_font)
        self.end_btn.setStyleSheet("color: black; background: white; border: none;")
        layout.addWidget(self.end_btn)

        self.save_btn = QPushButton("저장")
        self.save_btn.setFont(btn_font)
        self.save_btn.setStyleSheet("color: black; background: white; border: none;")
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def calculate_score(self):
        correct_count = 0
        total = len(self.correct_answers)
        for user, correct in zip(self.user_answers, self.correct_answers):
            if user.strip().lower() == correct.strip().lower():
                correct_count += 1
        return int((correct_count / total) * 100)
