from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import os
from datetime import datetime

class Result12View(QWidget):
    goto_analyze_signal = pyqtSignal(int)  # 점수 신호

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
        score_label.setStyleSheet("color:black; margin-top: 30")
        layout.addWidget(score_label)

        # 점수(빨간색, 크게)
        self.score_value = QLabel(str(self.score))
        self.score_value.setAlignment(Qt.AlignHCenter)
        self.score_value.setFont(QFont("Arial", 55, QFont.Bold))
        self.score_value.setStyleSheet("color: red;")
        layout.addWidget(self.score_value)

        # 버튼들 (분석하기, 다시하기, 종료, 저장)
        btn_font = QFont("Arial", 16)
        self.analyze_btn = QPushButton("분석 하기")
        self.analyze_btn.setFont(btn_font)
        self.analyze_btn.setStyleSheet("color: black; background: white; border: none;")
        self.analyze_btn.clicked.connect(self.goto_analyze)
        layout.addWidget(self.analyze_btn)

        self.retry_btn = QPushButton("다시 하기")
        self.retry_btn.setFont(btn_font)
        self.retry_btn.setStyleSheet("color: black; background: white; border: none;")
        self.retry_btn.clicked.connect(self.goto_result1)
        layout.addWidget(self.retry_btn)

        self.end_btn = QPushButton("종료")
        self.end_btn.setFont(btn_font)
        self.end_btn.setStyleSheet("color: black; background: white; border: none;")
        self.end_btn.clicked.connect(self.end_program)
        layout.addWidget(self.end_btn)

        self.save_btn = QPushButton("저장")
        self.save_btn.setFont(btn_font)
        self.save_btn.setStyleSheet("color: black; background: white; border: none;")
        self.save_btn.clicked.connect(self.save_result)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def calculate_score(self):
        correct_count = 0
        total = len(self.correct_answers)
        if total == 0:
            return 0
        for user, correct in zip(self.user_answers, self.correct_answers):
            if user.strip().lower() == correct.strip().lower():
                correct_count += 1
        return int((correct_count / total) * 100)

    def set_user_answers(self, user_answers, correct_answers):
        self.user_answers = user_answers
        self.correct_answers = correct_answers
        self.score = self.calculate_score()
        self.score_value.setText(str(self.score))

    def goto_analyze(self, score):
        self.goto_analyze_signal.emit(self.score)  # 점수 신호 발송

    def goto_result1(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(4)  # Result1로 이동

    def end_program(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(0)  # StartEndSplash로 이동
            QTimer.singleShot(2200, self.parent().close)  # 2.2초 후 창 닫기

    def save_result(self):
        msg = QMessageBox()
        msg.setStyleSheet('color: black;')
        msg.setWindowTitle("저장 확인")
        msg.setText("저장하겠습니까?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        ret = msg.exec_()
        if ret == QMessageBox.Yes:
            self.save_to_file()

    def save_to_file(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"score_{now}.txt"
        current_score = self.score

        # 기존 파일에서 최고 점수 읽기
        max_score = 0
        for fname in os.listdir('.'):
            if fname.startswith("score_"):
                try:
                    with open(fname, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if lines and lines[0].startswith("점수:"):
                            s = int(lines[0].split(":")[1].strip())
                            if s > max_score:
                                max_score = s
                except:
                    pass

        if current_score >= max_score or max_score == 0:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"점수: {current_score}\n")
                f.write(f"날짜: {now}\n")
                wrong = [i+1 for i, (u, c) in enumerate(zip(self.user_answers, self.correct_answers))
                         if u.strip().lower() != c.strip().lower()]
                f.write(f"틀린 문항: {wrong}\n")
                f.write("부족한 분야:\n4줄 요약 1\n4줄 요약 2\n4줄 요약 3\n4줄 요약 4\n")
                f.write("개선하면 좋을 점:\n개선점 1\n개선점 2\n개선점 3\n개선점 4\n")
