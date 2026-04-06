"""보너스 퀴즈 기능을 제공하는 모듈"""

import random

from quiz import Quiz


class RandomQuiz:
    """보너스 출제 규칙을 담당하는 클래스"""

    def _input_yes_no(self, input_handler, prompt: str) -> bool:
        while True:
            value = input_handler.input_non_empty_text(prompt).strip().lower()
            if value in ("y", "yes"):
                return True
            if value in ("n", "no"):
                return False
            print("y 또는 n만 입력하세요.")

    def select_quizzes_for_play(self, quizzes, input_handler):
        """출제할 퀴즈 목록을 결정하는 함수"""
        use_random = self._input_yes_no(input_handler, "랜덤 출제 사용(y/n): ")
        use_count = self._input_yes_no(input_handler, "문제 수 선택 사용(y/n): ")

        selected_quizzes = list(quizzes)
        if use_random:
            random.shuffle(selected_quizzes)  # 시드 고정 없이 매번 다른 순서 생성

        if use_count:
            quiz_count = input_handler.input_int_in_range("몇 문제를 풀까요: ", 1, len(selected_quizzes))
            selected_quizzes = selected_quizzes[:quiz_count]

        return selected_quizzes


class HintQuiz(Quiz):
    """힌트 입력 처리 기능을 포함하는 퀴즈 클래스"""

    def show_hint(self):
        """현재 퀴즈의 힌트를 출력하는 함수"""
        print(f"힌트: {self.hint}")

    def input_answer_with_optional_hint(self, input_handler):
        """정답 번호 또는 힌트 입력을 처리하는 함수"""
        used_hint_in_question = False

        while True:
            raw_answer = input_handler.input_non_empty_text("정답 번호를 입력하세요(h: 힌트): ").lower()  # 정답 또는 힌트 입력
            if raw_answer == "h":
                self.show_hint()  # 힌트 표시
                used_hint_in_question = True
                user_answer = input_handler.input_int_in_range("정답 번호를 입력하세요: ", 1, len(self.choices))  # 힌트 확인 후 정답 입력
                return user_answer, used_hint_in_question

            if raw_answer.isdigit():
                user_answer = int(raw_answer)
                if 1 <= user_answer <= len(self.choices):
                    return user_answer, used_hint_in_question
                print(f"허용 범위는 1~{len(self.choices)} 입니다.")
                continue

            print("숫자 또는 h만 입력하세요.")
