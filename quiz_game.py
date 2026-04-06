import json
from quiz import Quiz


class QuizGame:
    """메인 게임 로직 및 상태를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.state_file = "state.json"

    def load_state(self):
        with open(self.state_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.best_score = data.get("best_score", 0)
        self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": [],
        }
        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def show_menu(self):
        print("파이썬 퀴즈 프로그램 시작")
        print("1. 퀴즈 풀기 / 2. 퀴즈 추가 / 3. 퀴즈 목록 / 4. 점수 확인 / 5. 종료")
        return input("메뉴를 입력하세요: ")

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}번 문제")
            quiz.display()
            user_answer = input("정답 번호를 입력하세요: ")
            if quiz.check_answer(user_answer):
                score += 1

        print(f"점수: {score}/{len(self.quizzes)}")
        if score > self.best_score:
            self.best_score = score
            self.save_state()

    def add_quiz(self):
        question = input("질문을 입력하세요: ")
        choice_1 = input("1번 보기를 입력하세요: ")
        choice_2 = input("2번 보기를 입력하세요: ")
        choice_3 = input("3번 보기를 입력하세요: ")
        choice_4 = input("4번 보기를 입력하세요: ")
        answer = input("정답 번호를 입력하세요: ")

        choices = [
            f"1. {choice_1}",
            f"2. {choice_2}",
            f"3. {choice_3}",
            f"4. {choice_4}",
        ]
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("퀴즈가 추가되었습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def show_best_score(self):
        print(f"최고 점수: {self.best_score}")
