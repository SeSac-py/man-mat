from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QTextEdit, QSizePolicy, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal
import csv
import os

class AutoResizingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.document().documentLayout().documentSizeChanged.connect(self.adjustHeight)
        self.setMinimumHeight(60)

    def adjustHeight(self):
        doc_height = self.document().size().height()
        margins = self.contentsMargins()
        new_height = int(doc_height + margins.top() + margins.bottom())
        self.setFixedHeight(new_height)

class Result21View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        self.problem_list = []  # 입력된 문제 저장용 리스트
        self.current_problem = None  # 현재 선택된 문제 인덱스

        # 메인 레이아웃 (전체)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 스크롤 영역 생성
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(10)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # 1. 검색 키워드 입력창
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText("검색 키워드 입력")
        self.keyword_edit.setStyleSheet("font-size: 16px; color: black;")
        self.container_layout.addWidget(self.keyword_edit)

        # 2. 문제 입력창
        self.problem_edit = AutoResizingTextEdit()
        self.problem_edit.setPlaceholderText("문제 입력")
        self.problem_edit.setStyleSheet("font-size: 16px; color: black;")
        self.container_layout.addWidget(self.problem_edit)

        # 3. 문제 삭제 버튼 (문제와 답안이 지워짐)
        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon("resources/icons/delete.png"))
        self.delete_btn.setIconSize(QSize(45, 45))
        self.delete_btn.setStyleSheet("""
            border: none;
        """)
        self.delete_btn.clicked.connect(self.clear_inputs)
        self.container_layout.addWidget(self.delete_btn)

        # 답안 입력창
        self.answer_edit = AutoResizingTextEdit()
        self.answer_edit.setPlaceholderText("모범 답안 입력")
        self.answer_edit.setStyleSheet("font-size: 16px; color: black;")
        self.container_layout.addWidget(self.answer_edit)

        # 5. 문제 추가 입력버튼 (가로 기준 중앙 정렬)
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        self.add_btn = QPushButton()
        self.add_btn.setIcon(QIcon("resources/icons/plus.png"))
        self.add_btn.setIconSize(QSize(45, 45))
        self.add_btn.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)
        self.add_btn.clicked.connect(self.add_problem)
        center_layout.addWidget(self.add_btn)
        center_layout.addStretch()
        self.container_layout.addLayout(center_layout)

        # 6. 하단 버튼 (삭제, 생성)
        bottom = QHBoxLayout()
        # 하단 좌측 삭제 버튼 (1/2)
        self.clear_all_btn = QPushButton("모두 삭제")
        self.clear_all_btn.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            padding: 10px;
            font-size: 16px;
            min-width: 120px;
            text-align: center;
        """)
        self.clear_all_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.clear_all_btn.clicked.connect(self.clear_all)
        bottom.addWidget(self.clear_all_btn)
        # 하단 우측 생성 버튼 (1/2)
        self.create_btn = QPushButton("문제 생성")
        self.create_btn.setStyleSheet("""
            background-color: transparent;
            color: black;
            border: none;
            padding: 10px;
            font-size: 16px;
            min-width: 120px;
            text-align: center;
        """)
        self.create_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.create_btn.clicked.connect(self.save_to_csv)
        bottom.addWidget(self.create_btn)
        main_layout.addLayout(bottom)

    def clear_inputs(self):
        """문제, 답안, 키워드 입력창 초기화"""
        self.problem_edit.clear()
        self.answer_edit.clear()
        self.keyword_edit.clear()

    def clear_all(self):
        """모든 문제 및 입력창 초기화"""
        self.problem_list = []
        self.clear_inputs()
        QMessageBox.information(self, "알림", "모든 문제가 삭제되었습니다.")

    def add_problem(self):
        """문제 추가: 입력된 문제, 답안, 키워드를 리스트에 저장"""
        keyword = self.keyword_edit.text().strip()
        problem = self.problem_edit.toPlainText().strip()
        answer = self.answer_edit.toPlainText().strip()
        if not problem or not answer:
            QMessageBox.warning(self, "경고", "문제와 답안을 모두 입력하세요.")
            warning.setStyleSheet("color: black;")
            return
        self.problem_list.append((keyword, problem, answer))
        self.clear_inputs()
        QMessageBox.information(self, "알림", "문제가 추가되었습니다.")
        information.setStyleSheet("color: black;")

    def save_to_csv(self):
        """sample.csv에 문제 저장"""
        if not self.problem_list:
            QMessageBox.warning(self, "경고", "저장할 문제가 없습니다.")
            warning.setStyleSheet("color: black;")
            return
        filename = "../sample.csv"
        header = ["keyword", "problem", "answer"]
        try:
            # 파일이 없으면 헤더 추가, 있으면 이어서 저장
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(filename) == 0:
                    writer.writerow(header)
                writer.writerows(self.problem_list)
            QMessageBox.information(self, "알림", "문제가 저장되었습니다.")
            information.setStyleSheet("color: black;")
            self.problem_list = []
        except Exception as e:
            QMessageBox.critical(self, "오류", f"파일 저장 중 오류 발생: {e}")
            critical.setStyleSheet("color: black;")
