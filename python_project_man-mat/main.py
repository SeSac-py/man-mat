import sys
import os
from PyQt5.QtWidgets import QApplication, QStackedWidget
from views.start_end_splash import StartEndSplash
from views.search_box import SearchBoxView
from views.setting_window import SettingWindow
from views.result import ResultView
from views.result1 import Result1View
from views.result2 import Result2View
from views.result12 import Result12View
from views.analyze import Analyze
from views.result21 import Result21View
from controllers.search_controller import SearchController
from preprocess import QuestionAnswerLoader

class MainApp(QStackedWidget):
    def __init__(self, gif_path, win_width, win_height):
        super().__init__()
        self.splash = StartEndSplash(gif_path, win_width, win_height, parent=self)
        self.search_box = SearchBoxView(self)
        self.setting = SettingWindow(self)
        self.result = ResultView(self)

        self.total_questions = 5
        self.qa_loader = QuestionAnswerLoader('./data/questions.csv')
        self.qa_loader.load_data()
        self.questions, self.correct_answers = self.qa_loader.get_random_qa(self.total_questions)
        
        self.result1 = Result1View(self.questions, self.correct_answers, self)
        self.result2 = Result2View(self)
        self.result12 = Result12View([], [], self)
        self.analyze = Analyze(win_width, win_height, parent=self)
        self.result21 = Result21View(self)

        self.addWidget(self.splash)     # 0
        self.addWidget(self.search_box) # 1
        self.addWidget(self.setting)    # 2
        self.addWidget(self.result)     # 3
        self.addWidget(self.result1)    # 4
        self.addWidget(self.result2)    # 5
        self.addWidget(self.analyze)    # 6
        self.addWidget(self.result12)   # 7
        self.addWidget(self.result21)   # 8

        self.setCurrentIndex(0)
        self.search_controller = SearchController(self.search_box)
        self.last_user_answers = []  # 사용자 답 저장용

        self.result12.goto_analyze_signal.connect(self.goto_analyze)    # 시그널 연결
        self.result1.submit_all_answers.connect(self.update_result12)   # 제출 시그널 연결 (예시: Result1View에서 제출 시 Result12로 이동 및 점수 전달)

    def update_result12(self, user_answers):
        # 틀린 문항 계산
        wrong = [i+1 for i, (u, c) in enumerate(zip(user_answers, self.correct_answers))
                 if u.strip().lower() != c.strip().lower()]
        # Result12에 점수 및 틀린 문항 전달
        self.result12.set_user_answers(user_answers, self.correct_answers)
        # [수정] Analyze에 점수 및 틀린 문항 전달 (self.result12.total_score 사용!)
        score = self.result12.total_score  # [수정]
        self.analyze.update_score(score, wrong)
        # Result12로 이동
        self.setCurrentIndex(7)

    def goto_analyze(self, score):
        # Analyze로 이동 (틀린 문항 리스트는 이미 update_result12에서 전달됨)
        self.setCurrentIndex(6)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: white; }")
    screen = app.primaryScreen()
    size = screen.size()
    screen_height = size.height()
    win_height = int(screen_height / 2)
    win_width = int(win_height * 1.2)
    gif_path = os.path.join(os.path.dirname(__file__), "resources", "start_end_splash.gif")
    main_window = MainApp(gif_path, win_width, win_height)
    main_window.setWindowTitle("main-mat")
    main_window.resize(win_width, win_height)
    main_window.show()
    sys.exit(app.exec_())
