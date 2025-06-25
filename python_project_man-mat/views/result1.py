from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QTextEdit, QSizePolicy, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal

class Result1View(QWidget):
    submit_all_answers = pyqtSignal(list)

    def __init__(self, questions, answers, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        self.current_index = 0
        self.time_left = 10 * 60  # 10분(초 단위)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.questions = questions  
        self.total_questions = len(self.questions)
        self.user_answers = [""] * self.total_questions
        self.init_ui()
        self.update_ui()
        self.timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(10)

        # 시계 아이콘 + 남은 시간
        clock_layout = QVBoxLayout()
        clock_layout.setAlignment(Qt.AlignHCenter)
        self.clock_icon = QLabel()
        self.clock_icon.setPixmap(QIcon("resources/icons/time.png").pixmap(QSize(50, 50)))
        self.clock_icon.setAlignment(Qt.AlignHCenter)
        clock_layout.addWidget(self.clock_icon)
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignHCenter)
        self.time_label.setStyleSheet('font-size: 15px; color: black;')
        font = QFont()
        font.setPointSize(14)
        self.time_label.setFont(font)
        clock_layout.addWidget(self.time_label)
        layout.addLayout(clock_layout)

        # 문제 텍스트
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 20px; color: black;")
        layout.addWidget(self.question_label)

        # 답안 입력 박스
        self.answer_edit = QTextEdit()
        self.answer_edit.setStyleSheet("font-size: 20px; color: black;")
        self.answer_edit.setPlaceholderText("여기에 답안을 입력해주세요.")
        self.answer_edit.setFixedHeight(60)
        layout.addWidget(self.answer_edit)

        # 제출 버튼
        self.submit_btn = QPushButton("제출하기")
        self.submit_btn.setStyleSheet("font-size: 16px; color: black;")
        self.submit_btn.setFixedHeight(40)
        self.submit_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.submit_btn.clicked.connect(self.submit_answers)
        layout.addSpacing(20)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignHCenter)

        # 문제수/페이지 표기
        page_layout = QHBoxLayout()
        page_layout.setAlignment(Qt.AlignCenter)
        self.page_edit = QLineEdit()
        self.page_edit.setText(str(self.current_index + 1))
        self.page_edit.setFixedWidth(40)
        self.page_edit.setAlignment(Qt.AlignCenter)
        self.page_edit.setMaxLength(3)
        self.page_edit.setStyleSheet("font-size: 16px; color: black;")
        self.page_edit.returnPressed.connect(self.goto_page)
        self.page_label = QLabel(f"/{self.total_questions}")
        self.page_label.setStyleSheet("font-size: 16px; color: black;")
        page_layout.addWidget(self.page_edit)
        page_layout.addWidget(self.page_label)
        layout.addLayout(page_layout)

        # 네비게이션
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(30)
        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(QIcon("resources/icons/left.png"))
        self.prev_btn.setIconSize(QSize(40, 40))
        self.prev_btn.setFixedSize(60, 60)
        self.prev_btn.setStyleSheet("background: transparent; border: none;")
        self.prev_btn.clicked.connect(self.goto_prev)
        self.next_btn = QPushButton()
        self.next_btn.setIcon(QIcon("resources/icons/right.png"))
        self.next_btn.setIconSize(QSize(40, 40))
        self.next_btn.setFixedSize(60, 60)
        self.next_btn.setStyleSheet("background: transparent; border: none;")
        self.next_btn.clicked.connect(self.goto_next)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        layout.addLayout(nav_layout)

        self.setLayout(layout)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.time_label.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.submit_answers()

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h:02}:{m:02}:{s:02}"

    def update_ui(self):
        self.question_label.setText(self.questions[self.current_index])
        self.page_edit.setText(str(self.current_index + 1))
        self.page_label.setText(f"/{self.total_questions}")
        self.answer_edit.setText(self.user_answers[self.current_index])

    def goto_prev(self):
        self.user_answers[self.current_index] = self.answer_edit.toPlainText()
        if self.current_index == 0:
            self.current_index = self.total_questions - 1
        else:
            self.current_index -= 1
        self.update_ui()

    def goto_next(self):
        self.user_answers[self.current_index] = self.answer_edit.toPlainText()
        if self.current_index == self.total_questions - 1:
            self.current_index = 0
        else:
            self.current_index += 1
        self.update_ui()

    def goto_page(self):
        self.user_answers[self.current_index] = self.answer_edit.toPlainText()
        try:
            page = int(self.page_edit.text())
            if 1 <= page <= self.total_questions:
                self.current_index = page - 1
            else:
                self.page_edit.setText(str(self.current_index + 1))
        except ValueError:
            self.page_edit.setText(str(self.current_index + 1))
        self.update_ui()

    def submit_answers(self):
        self.user_answers[self.current_index] = self.answer_edit.toPlainText()
        self.timer.stop()
        self.submit_all_answers.emit(self.user_answers)

    # "다시하기" 시 초기화용 함수 추가
    def init_timer_and_answers(self):
        self.current_index = 0
        self.time_left = 10 * 60  # 10분(초 단위)
        self.user_answers = [""] * self.total_questions
        self.timer.stop()
        self.timer.start(1000)
        self.update_ui()
