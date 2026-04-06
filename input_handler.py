class InputHandler:
    """입력값 검증과 변환을 담당하는 클래스"""

    def input_int_in_range(self, prompt: str, min_value: int, max_value: int) -> int:
        while True:
            raw = input(prompt).strip()  # 앞뒤 공백 제거
            if raw == "":
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue

            try:
                value = int(raw)
            except ValueError:
                print("숫자만 입력하세요.")
                continue

            if value < min_value or value > max_value:
                print(f"허용 범위는 {min_value}~{max_value} 입니다.")
                continue

            return value

    def input_non_empty_text(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()  # 앞뒤 공백 제거
            if value == "":
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return value

    def validate_quizzes_data(self, data: dict):
        quizzes_data = data.get("quizzes")  # JSON에서 quizzes 필드 조회
        if not isinstance(quizzes_data, list):  # quizzes가 리스트인지 확인
            raise TypeError  # 리스트가 아니면 손상 데이터 처리

        validated = []
        for item in quizzes_data:  # 퀴즈 항목 순회
            if not isinstance(item, dict):  # 각 항목이 딕셔너리인지 확인
                raise TypeError

            question = item.get("question")  # 문제 텍스트 추출
            choices = item.get("choices")  # 선택지 목록 추출
            answer = item.get("answer")  # 정답 번호 추출
            hint = item.get("hint")  # 힌트 텍스트 추출

            if not isinstance(question, str) or question.strip() == "":  # 문제가 빈 문자열이 아닌지 확인
                raise ValueError
            if not isinstance(choices, list) or len(choices) != 4:  # 선택지가 정확히 4개인지 확인
                raise ValueError
            if not all(isinstance(choice, str) for choice in choices):  # 선택지 요소가 모두 문자열인지 확인
                raise ValueError
            if not isinstance(hint, str) or hint.strip() == "":  # 힌트가 빈 문자열이 아닌지 확인
                raise ValueError

            answer_number = int(str(answer).strip())  # 정답 번호를 정수로 변환
            if answer_number < 1 or answer_number > 4:  # 정답 번호 범위(1~4) 검증
                raise ValueError

            validated.append({
                "question": question,
                "choices": choices,
                "answer": str(answer_number),
                "hint": hint,
            })

        return validated
