class Quiz:
    """단일 퀴즈 질문과 정답을 나타내는 클래스"""
    
    # 속성: 문제(question), 선택지(choices), 정답(answer)
    # self는 인스턴스 자신을 가리키는 예약어, 인스턴스란 클래스에서 생성된 객체를 의미
    # 클래스 내에서 정의된 메서드에서 self를 사용하여 인스턴스의 속성에 접근
    def __init__(self, question: str, choices: list, answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    # 메서드: 퀴즈 출력 기능을 구현한다.
    def display(self):
        for choice in self.choices:
            print(choice)

    # 메서드: 퀴즈 정답 확인 기능을 구현한다.
    def check_answer(self, user_answer) -> bool:
        return str(user_answer).strip() == str(self.answer).strip()

    # 속성: 문제(question), 선택지(choices), 정답(answer) -> 딕셔너리 형태로 반환
    def to_dict(self) -> dict:
        return {
            "question": self.question,  # 문제(question)
            "choices": self.choices,  # 선택지(choices)
            "answer": self.answer  # 정답(answer)
        }
