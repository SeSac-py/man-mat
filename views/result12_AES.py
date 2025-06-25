from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from AES import evaluate  

class Result12View(QWidget):
    def __init__(self, user_answers, correct_answers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("main-mat")
        self.user_answers = user_answers
        self.correct_answers = correct_answers
        self.scores = self.calculate_scores()  
        self.total_score = self.calculate_total_score()  

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
        score_value = QLabel(str(self.total_score))
        score_value.setAlignment(Qt.AlignHCenter)
        score_value.setFont(QFont("Arial", 48, QFont.Bold))
        score_value.setStyleSheet("color: red;")
        layout.addWidget(score_value)

        # 각 문항별 점수 표시 (옵션)
        for idx, (user, correct, score) in enumerate(zip(self.user_answers, self.correct_answers, self.scores), 1):
            detail_label = QLabel(f"{idx}번: {score} / 10")
            detail_label.setFont(QFont("Arial", 14))
            detail_label.setAlignment(Qt.AlignHCenter)
            layout.addWidget(detail_label)

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

    def calculate_scores(self):
        # 각 문항별 evalutat() 점수 계산 (0~10점)
        scores = []
        for user, correct in zip(self.user_answers, self.correct_answers):
            score = evaluate(correct, user)  
            scores.append(score)
        return scores

    def calculate_total_score(self):
        if not self.scores:
            return 0
        avg = sum(self.scores) / len(self.scores)
        return int(avg * 10)  # 0~100점 환산
