import pandas as pd
import random

class QuestionAnswerLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self._df = None
        self._questions_list = []
        self._answers_list = []

    def load_data(self):
        self._df = pd.read_csv(self.file_path)
        self.questions_list = self._df['문제'].to_list()    # _questions_list
        self.answers_list = self._df['정답'].to_list()  # _answers_list

    # @property
    # def questions_list(self):
    #     return self._questions_list

    # @property
    # def answers_list(self):
    #     return self._answers_list
    
    def get_random_qa(self, n):
        """
        문제와 정답을 랜덤으로 n개 선택하여 반환
        :param n: 선택할 개수
        :return: (questions, answers) 튜플 (각각 리스트)
        """
        qa_pairs = list(zip(self.questions_list, self.answers_list))
        selected = random.sample(qa_pairs, n)
        questions, answers = zip(*selected)
        return list(questions), list(answers)

if __name__ == "__main__":
    loader = QuestionAnswerLoader('./data/questions.csv')
    loader.load_data()
    print(loader.questions_list)
    print(loader.answers_list)

