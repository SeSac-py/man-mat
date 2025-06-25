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
from controllers.search_controller import SearchController

class MainApp(QStackedWidget):
    def __init__(self, gif_path, win_width, win_height):
        super().__init__()
        self.splash = StartEndSplash(gif_path, win_width, win_height, parent=self)
        self.search_box = SearchBoxView(self)
        self.setting = SettingWindow(self)
        self.result = ResultView(self)
        self.result1 = Result1View(self)
        self.result2 = Result2View(self)
        self.analyze = Analyze(win_width, win_height, parent=self)
        self.result12 = Result12View([], [], self)  # 빈 데이터로 초기화
        self.result12.goto_analyze_signal.connect(self.goto_analyze)
        self.addWidget(self.result12)  # QStackedWidget에 추가
        self.correct_answers = [
            "RSA", "트래픽 필터링", "입력값 검증 미흡", "보안 터널링", "복호화 가능"
        ]
        self.addWidget(self.splash)     # 0
        self.addWidget(self.search_box) # 1
        self.addWidget(self.setting)    # 2
        self.addWidget(self.result)     # 3
        self.addWidget(self.result1)    # 4
        self.addWidget(self.result2)    # 5
        self.addWidget(self.analyze)    # 6
        self.addWidget(self.result12)   # 7

        self.setCurrentIndex(0)
        self.search_controller = SearchController(self.search_box)
        # 제출 시그널 연결
        self.result1.submit_all_answers.connect(self.update_result12)

    def update_result12(self, user_answers):
        # Result12를 재설정
        self.result12.set_user_answers(user_answers, self.correct_answers)
        self.setCurrentIndex(7)  # Result12로 이동
    
    def show_result12(self, user_answers):
        self.result12.set_user_answers(user_answers, self.correct_answers)
        self.setCurrentWidget(self.result12)

    def goto_analyze(self, score):
        self.analyze.update_score(score)  # main이 Analyze에 점수 전달
        self.setCurrentIndex(6)  # Analyze로 이동



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
