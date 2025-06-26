from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import os
from datetime import datetime
from AES import evaluate  # 추가

class Result12View(QWidget):
    goto_analyze_signal = pyqtSignal(int)

    def __init__(self, user_answers, correct_answers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("man-mat")
        self.user_answers = user_answers
        self.correct_answers = correct_answers
        self.scores = self.calculate_scores()  # 각 문항별 점수
        self.total_score = self.calculate_total_score()  # 전체 평균 점수(0~100)
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
        self.score_value = QLabel(str(self.total_score))
        self.score_value.setAlignment(Qt.AlignHCenter)
        self.score_value.setFont(QFont("Arial", 55, QFont.Bold))
        self.score_value.setStyleSheet("color: red;")
        layout.addWidget(self.score_value)

        # 각 문항별 점수 표시
        for idx, (user, correct, score) in enumerate(zip(self.user_answers, self.correct_answers, self.scores), 1):
            detail_label = QLabel(f"{idx}번: {score} / 10")
            detail_label.setFont(QFont("Arial", 14))
            detail_label.setAlignment(Qt.AlignHCenter)
            layout.addWidget(detail_label)

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

    def calculate_scores(self):
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

    def set_user_answers(self, user_answers, correct_answers):
        self.user_answers = user_answers
        self.correct_answers = correct_answers
        self.scores = self.calculate_scores()
        self.total_score = self.calculate_total_score()
        self.score_value.setText(str(self.total_score))
        # 각 문항별 점수 표시 갱신 (레이아웃 클리어 후 다시 추가)
        layout = self.layout()
        # 기존 점수 표시 위젯 삭제 (SCORE, 점수, 버튼은 제외)
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget and widget not in (self.score_value, self.analyze_btn, self.retry_btn, self.end_btn, self.save_btn):
                if widget.text() != "SCORE":
                    layout.removeWidget(widget)
                    widget.deleteLater()
        # 각 문항별 점수 표시 다시 추가
        for idx, (user, correct, score) in enumerate(zip(self.user_answers, self.correct_answers, self.scores), 1):
            detail_label = QLabel(f"{idx}번: {score} / 10")
            detail_label.setFont(QFont("Arial", 14))
            detail_label.setAlignment(Qt.AlignHCenter)
            layout.insertWidget(2 + idx, detail_label)  # SCORE, 점수 다음에 추가

    def goto_analyze(self):
        self.goto_analyze_signal.emit(self.total_score)

    def goto_result1(self):
        if self.parent() is not None:
            result1 = self.parent().widget(4)  # Result1View의 인덱스가 4라고 가정
            if hasattr(result1, 'init_timer_and_answers'):
                result1.init_timer_and_answers()
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
        current_score = self.total_score  # 총점 사용
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