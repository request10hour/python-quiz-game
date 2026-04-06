class Quiz:
    """단일 퀴즈 질문과 정답을 나타내는 클래스"""
    
    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(f"질문: {self.question}")
        for choice in self.choices:
            print(choice)

    def check_answer(self, user_answer) -> bool:
        return str(user_answer).strip() == str(self.answer).strip()

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["question"], data["choices"], data["answer"])
