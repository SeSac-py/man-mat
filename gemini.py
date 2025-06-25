# import time
# import google.generativeai as genai

# GOOGLE_API_KEY = "AIzaSyAk0eLuUUs4f0hr3WYyUu_vnnD8coF44KQ"
# genai.configure(api_key=GOOGLE_API_KEY)
# # The Gemini 1.5 models are versatile and work with both text-only and multimodal prompts
# model = genai.GenerativeModel('gemini-1.5-flash')


# start_time = time.time()
# user_prompt = """
#     모든 대답은 한국어로 대답해줘.
#     뉴턴의 법칙에 대해서 초등학생도 이해할 수 있을 만큼 쉽게 설명해줘.
# """
# response = model.generate_content(
#     user_prompt,
#     generation_config=genai.types.GenerationConfig(
#     # Only one candidate for now.
#     candidate_count=1,
#     stop_sequences=['x'],
#     #max_output_tokens=40,
#     temperature=1.0)
# )
# print(response.text)
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"실행 시간: {execution_time:.2f} 초")


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from google import genai
# 1. Gemini API 키 입력
API_KEY = "AIzaSyAk0eLuUUs4f0hr3WYyUu_vnnD8coF44KQ"
# 2. Gemini API 클라이언트 생성
client = genai.Client(api_key=API_KEY)
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gemini API Example")
        self.setGeometry(100, 100, 400, 300)
        # 레이아웃 및 위젯 구성
        layout = QVBoxLayout()
        self.input_label = QLabel("답안을 입력하세요:")
        layout.addWidget(self.input_label)

        self.input_edit = QLineEdit()
        layout.addWidget(self.input_edit)
        self.send_button = QPushButton("Gemini API에 보내기")
        self.send_button.clicked.connect(self.send_to_gemini)
        layout.addWidget(self.send_button)
        self.result_label = QLabel("Gemini 응답:")
        layout.addWidget(self.result_label)
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)
        layout.addWidget(self.result_edit)
        self.setLayout(layout)
    def send_to_gemini(self):
        # 3. 사용자 입력값 가져오기
        user_input = self.input_edit.text()
        # 4. Gemini API로 답안 전송 및 결과 받기
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # 또는 본인이 원하는 모델명
                contents=user_input
            )
            # 5. 응답 결과를 GUI에 표시
            self.result_edit.setText(response.text)
        except Exception as e:
            self.result_edit.setText(f"에러 발생: {e}")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())