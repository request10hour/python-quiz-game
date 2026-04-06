from quiz import Quiz
from quiz_game import QuizGame

class QuizBonus(Quiz):
    """힌트를 제공하는 퀴즈 클래스"""
    
    def __init__(self, question: str, choices: list, answer: int, hint: str):
        super().__init__(question, choices, answer)
        self.hint = hint

    def show_hint(self):
        pass

class QuizBonusGame(QuizGame):
    """확장된 기능을 갖춘 게임 모드 클래스"""
    
    def __init__(self):
        super().__init__()
        self.score_history = []

    def delete_quiz(self):
        pass

    def play_random_quiz(self):
        pass

    def select_quiz_count(self):
        pass

    def show_history(self):
        pass
