from quiz import Quiz
from quiz_game import QuizGame

class QuizBonus(Quiz):
    """A quiz that provides hints."""
    
    def __init__(self, question: str, choices: list, answer: int, hint: str):
        super().__init__(question, choices, answer)
        self.hint = hint

    def show_hint(self):
        pass

class QuizBonusGame(QuizGame):
    """Game mode with extended functionalities."""
    
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
