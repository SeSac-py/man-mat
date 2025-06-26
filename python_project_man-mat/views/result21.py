from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QSizePolicy, QScrollArea
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import csv
import os
from views.problem_sets import ProblemSet
from views.custom_dialog import CenteredButtonDialog

class Result21View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("mat-mat")
        self.problem_sets = []  # ProblemSet 위젯 리스트
        self.problem_data = []  # 문제/답안/키워드 저장용 리스트

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

        # 1. 키워드 입력창 (상단 고정)
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText("검색 키워드 입력")
        self.keyword_edit.setStyleSheet("font-size: 16px; color: black;")
        self.container_layout.addWidget(self.keyword_edit)

        # 문제 세트가 추가되는 위치 (아래에 자동으로 추가)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # 2. plus 버튼 (하단 고정)
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        self.add_btn = QPushButton()
        self.add_btn.setIcon(QIcon("resources/icons/plus.png"))
        self.add_btn.setIconSize(QSize(45, 45))
        self.add_btn.setStyleSheet("background-color: transparent; border: none;")
        self.add_btn.clicked.connect(self.add_problem_set)
        center_layout.addWidget(self.add_btn)
        center_layout.addStretch()
        main_layout.addLayout(center_layout)

        # 3. 하단 버튼 (모두 삭제, 문제 생성)
        bottom = QHBoxLayout()
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

    def add_problem_set(self):
        """새로운 문제 세트 추가"""
        problem_set = ProblemSet(self)
        # 삭제 버튼 클릭 시 해당 세트 삭제
        problem_set.delete_btn.clicked.connect(
            lambda: self.remove_problem_set(problem_set)
        )
        self.problem_sets.append(problem_set)
        # 키워드 입력창 아래에 추가
        self.container_layout.insertWidget(
            self.container_layout.count() - 0,  # 마지막에 추가 (키워드 입력창 아래)
            problem_set
        )

    def remove_problem_set(self, problem_set):
        """문제 세트 삭제"""
        self.problem_sets.remove(problem_set)
        problem_set.deleteLater()

    def clear_all(self):
        """모든 문제 세트 삭제"""
        for problem_set in self.problem_sets[:]:
            self.remove_problem_set(problem_set)
        dialog = CenteredButtonDialog("알림", "모든 문제가 삭제되었습니다.", self)
        dialog.exec_()
        # 모두 삭제 후 SearchBoxView로 이동
        if self.parent() is not None:
            self.parent().setCurrentIndex(1)  # SearchBoxView 인덱스 1

    def save_to_csv(self):
        """문제/답안/키워드를 CSV로 저장"""
        # 데이터 수집
        self.problem_data = []
        keyword = self.keyword_edit.text().strip()
        for problem_set in self.problem_sets:
            problem = problem_set.problem_edit.toPlainText().strip()
            answer = problem_set.answer_edit.toPlainText().strip()
            if problem and answer:
                self.problem_data.append((keyword, problem, answer))
        if not self.problem_data:
            dialog = CenteredButtonDialog("경고", "저장할 문제가 없습니다.", self)
            dialog.exec_()
            return
        filename = "sample.csv"
        header = ["keyword", "problem", "answer"]
        try:
            # 파일이 없으면 헤더 추가, 있으면 이어서 저장
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(filename) == 0:
                    writer.writerow(header)
                writer.writerows(self.problem_data)
            dialog = CenteredButtonDialog("알림", "문제가 저장되었습니다.", self)
            dialog.exec_()
            self.problem_data = []
            # 문제 생성 후 SearchBoxView로 이동
            if self.parent() is not None:
                self.parent().setCurrentIndex(1)  # SearchBoxView 인덱스 1
        except Exception as e:
            dialog = CenteredButtonDialog("오류", f"파일 저장 중 오류 발생: {e}", self)
            dialog.exec_()
