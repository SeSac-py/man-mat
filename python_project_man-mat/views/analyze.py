import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize
from google import genai

API_KEY = "AIzaSyAk0eLuUUs4f0hr3WYyUu_vnnD8coF44KQ"
client = genai.Client(api_key=API_KEY)

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
        self.score_label = QLabel("Your Score")
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
        # 5. 분석 결과 (검은색)
        lack_label = QLabel("부족한 분야")
        lack_label.setStyleSheet("color: black; font-size: 14px; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(lack_label)
        self.lack_text = QTextEdit("4줄 요약 1\n4줄 요약 2\n4줄 요약 3\n4줄 요약 4")
        self.lack_text.setReadOnly(True)
        self.lack_text.setMinimumHeight(60)
        self.lack_text.setStyleSheet("color: black; font-size: 14px;")
        self.container_layout.addWidget(self.lack_text)
        # 6. 개선하면 좋을 점 (검은색)
        improve_label = QLabel("개선하면 좋을 점")
        improve_label.setStyleSheet("color: black; font-size: 14px; margin: 0px; padding: 0px;")
        self.container_layout.addWidget(improve_label)
        self.improve_text = QTextEdit("개선점 1\n개선점 2\n개선점 3\n개선점 4")
        self.improve_text.setReadOnly(True)
        self.improve_text.setMinimumHeight(60)
        self.improve_text.setStyleSheet("color: black; font-size: 14px;")
        self.container_layout.addWidget(self.improve_text)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # 문제/정답/사용자 답 저장
        self.questions = []
        self.correct_answers = []
        self.user_answers = []

    def update_score(self, score, questions=None, correct_answers=None, user_answers=None):
        self.score_label.setText("Your Score")
        self.score_value.setText(str(score))
        if questions is not None:
            self.questions = questions
        if correct_answers is not None:
            self.correct_answers = correct_answers
        if user_answers is not None:
            self.user_answers = user_answers
        self.analyze_with_gemini()

    def analyze_with_gemini(self):
        prompt = "아래는 문제, 정답, 사용자 답입니다.\n"
        for idx, (q, c, u) in enumerate(zip(self.questions, self.correct_answers, self.user_answers), 1):
            prompt += f"\n문제 {idx}: {q}\n정답: {c}\n사용자 답: {u}\n"

        prompt += """
                    위 정보를 바탕으로, 사용자가 부족한 분야를 4줄로 요약해주세요.
                    그리고 개선하면 좋은 점도 4줄로 요약해주세요.
                    답변은 반드시 아래 형식으로 해주세요.

                    부족한 분야:
                    1. ...
                    2. ...
                    3. ...
                    4. ...

                    개선하면 좋을 점:
                    1. ...
                    2. ...
                    3. ...
                    4. ...
                """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )
            result = response.text

            lack = []
            improve = []
            lines = result.split('\n')
            section = None
            for line in lines:
                if "부족한 분야:" in line or "부족한 분야 :" in line:
                    section = "lack"
                elif "개선하면 좋을 점:" in line or "개선하면 좋을 점 :" in line:
                    section = "improve"
                elif section == "lack" and line.strip() and line[0].isdigit():
                    lack.append(line.strip())
                elif section == "improve" and line.strip() and line[0].isdigit():
                    improve.append(line.strip())

            # QTextEdit에 출력
            self.lack_text.setText("\n".join(lack[:4]))
            self.improve_text.setText("\n".join(improve[:4]))
        except Exception as e:
            self.lack_text.setText(f"에러 발생: {e}")
            self.improve_text.setText("")

    def go_back(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(7)  # Result12로 이동
