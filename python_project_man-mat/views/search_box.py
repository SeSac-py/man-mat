from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import os

class SearchBoxView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        layout = QVBoxLayout()

        # 상단 설정 버튼 및 analyze 버튼 (위아래로, 각각 오른쪽 정렬)
        top = QVBoxLayout()
        # 설정 버튼 (오른쪽 정렬)
        setting_row = QHBoxLayout()
        setting_row.addStretch()
        self.setting_btn = QPushButton()
        self.setting_btn.setIcon(QIcon("resources/icons/settings.png"))
        self.setting_btn.setIconSize(QSize(32, 32))
        self.setting_btn.setToolTip("설정")
        self.setting_btn.setStyleSheet("background-color: transparent; border: none; margin: 3px;")
        setting_row.addWidget(self.setting_btn)
        top.addLayout(setting_row)
        # 분석 버튼 (오른쪽 정렬)
        analyze_row = QHBoxLayout()
        analyze_row.addStretch()
        self.analyze_btn = QPushButton()
        self.analyze_btn.setIcon(QIcon("resources/icons/analyze.png"))
        self.analyze_btn.setIconSize(QSize(32, 32))
        self.analyze_btn.setToolTip("분석")
        self.analyze_btn.setStyleSheet("background-color: transparent; border: none; margin: 3px;")
        self.analyze_btn.clicked.connect(self.show_analyze2)
        analyze_row.addWidget(self.analyze_btn)
        top.addLayout(analyze_row)
        layout.addLayout(top)

        # 중앙 검색창 및 버튼
        mid = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("검색어를 입력하세요")
        self.search_edit.setMinimumSize(300, 40)
        self.search_edit.setStyleSheet("border: 2px solid black; border-radius: 10px; color: black;")
        self.search_btn = QPushButton()
        self.search_btn.setIcon(QIcon("resources/icons/search.png"))
        self.search_btn.setIconSize(QSize(40, 40))
        self.search_btn.setStyleSheet("background-color: black; border: 5px solid black; border-radius: 5px;")
        mid.addWidget(self.search_edit)
        mid.addWidget(self.search_btn)
        layout.addStretch()
        layout.addLayout(mid)
        layout.addStretch()
        self.setLayout(layout)
        self.setting_btn.clicked.connect(self.goto_setting)

        # 검색창 엔터 및 버튼 클릭 연결
        self.search_edit.returnPressed.connect(self.on_search)
        self.search_btn.clicked.connect(self.on_search)

    def on_search(self):
        keyword = self.search_edit.text().strip()
        print(f"검색어: {keyword}")  # 실제 검색 로직은 여기에 추가
        # Result 창으로 이동 (인덱스 3)
        if self.parent() is not None:
            self.parent().setCurrentIndex(3)  # ResultView로 이동

    def goto_setting(self):
        if self.parent() is not None:
            self.parent().setCurrentIndex(2)

    def show_analyze2(self):
        # Analyze 창으로 이동 (인덱스 6)
        if self.parent() is not None:
            analyze = self.parent().widget(6)  # Analyze 인덱스 6
            if hasattr(analyze, 'show_best_score'):
                # 점수 기록 파일에서 최고 점수 읽기
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
                analyze.show_best_score(max_score)
                self.parent().setCurrentIndex(6)
