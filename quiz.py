class Quiz:
    """단일 퀴즈 질문과 정답을 나타내는 클래스"""
    
    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        pass

    def check_answer(self, user_answer) -> bool:
        pass

    def to_dict(self) -> dict:
        pass

    @classmethod
    def from_dict(cls, data: dict):
        pass
