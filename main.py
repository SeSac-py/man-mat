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
        self.result12 = None  # 점수화면(동적으로 생성)
        self.correct_answers = [
            "RSA", "트래픽 필터링", "입력값 검증 미흡", "보안 터널링", "복호화 가능"
        ]
        self.addWidget(self.splash)      # 0
        self.addWidget(self.search_box)  # 1
        self.addWidget(self.setting)     # 2
        self.addWidget(self.result)      # 3
        self.addWidget(self.result1)     # 4
        self.addWidget(self.result2)     # 5
        self.setCurrentIndex(0)
        self.search_controller = SearchController(self.search_box)

        # 제출 시그널 연결
        self.result1.submit_all_answers.connect(self.show_result12)

    def show_result12(self, user_answers):
        if self.result12 is not None:
            self.removeWidget(self.result12)
            self.result12.deleteLater()
        self.result12 = Result12View(user_answers, self.correct_answers, self) 
        self.addWidget(self.result12)
        self.setCurrentWidget(self.result12)

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
