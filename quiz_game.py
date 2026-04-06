import json
from quiz import Quiz


class QuizGame:
    """메인 게임 로직 및 상태를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []  # 퀴즈 목록
        self.best_score = 0  # 최고 점수
        self.state_file = "state.json"  # 상태 저장 파일 경로
        self.default_state_file = "state_default.json"  # 기본 상태 파일 경로

    def _default_state_data(self):
        with open(self.default_state_file, "r", encoding="utf-8") as file:  # 기본 상태 파일 읽기
            data = json.load(file)  # 기본 JSON 데이터 로드
        if not isinstance(data.get("quizzes"), list):
            raise TypeError
        return data

    def _reset_with_default_data(self):
        default_data = self._default_state_data()  # 기본 상태 데이터 로드
        self.best_score = default_data.get("best_score", 0)  # 최고 점수 초기화
        self.quizzes = [Quiz.from_dict(item) for item in default_data.get("quizzes", [])]  # 기본 퀴즈 적용

    def _input_int_in_range(self, prompt: str, min_value: int, max_value: int) -> int:
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

    def load_state(self):
        try:
            with open(self.state_file, "r", encoding="utf-8") as file:  # 상태 파일 읽기
                data = json.load(file)  # JSON 데이터 로드
            self.quizzes = [Quiz.from_dict(item) for item in data.get("quizzes", [])]  # 퀴즈 목록 객체 변환
            self.best_score = data.get("best_score", 0)  # 최고 점수 불러오기
            if not self.quizzes:
                self._reset_with_default_data()
                self.save_state()
        except FileNotFoundError:
            print("state.json 파일이 없어 state_default.json 데이터를 불러옵니다.")
            self._reset_with_default_data()
            self.save_state()
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("state.json 파일을 불러올 수 없어 state_default.json 데이터를 불러옵니다.")
            self._reset_with_default_data()
            self.save_state()

    def save_state(self):
        data = {  # 저장할 상태 데이터 구성
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],  # 퀴즈 목록 직렬화
            "best_score": self.best_score,  # 최고 점수 저장
            "history": [],  # 기록 목록 기본값
        }
        with open(self.state_file, "w", encoding="utf-8") as file:  # 상태 파일 쓰기
            json.dump(data, file, ensure_ascii=False, indent=2)  # JSON 형태로 저장

    def show_menu(self):
        print("\n파이썬 퀴즈 프로그램 시작")  # 프로그램 시작 문구 출력
        print("1. 퀴즈 풀기 / 2. 퀴즈 추가 / 3. 퀴즈 목록 / 4. 점수 확인 / 5. 종료")  # 메뉴 출력
        return self._input_int_in_range("메뉴를 입력하세요: ", 1, 5)  # 메뉴 번호 입력 반환

    def play_quiz(self):
        if not self.quizzes:  # 퀴즈가 없는 경우 확인
            print("등록된 퀴즈가 없습니다.")  # 안내 문구 출력
            return  # 함수 종료

        score = 0  # 현재 플레이 점수
        for index, quiz in enumerate(self.quizzes, start=1):  # 퀴즈 순회
            print(f"\n[{index}번 문제] {quiz.question}")  # 문제 번호와 질문 출력
            quiz.display()  # 문제와 보기 출력
            user_answer = self._input_int_in_range("정답 번호를 입력하세요: ", 1, len(quiz.choices))  # 사용자 답 입력
            if quiz.check_answer(str(user_answer)):  # 정답 여부 확인
                score += 1  # 점수 증가

        print(f"\n점수: {score}/{len(self.quizzes)}")  # 결과 점수 출력
        if score > self.best_score:  # 최고 점수 갱신 여부 확인
            self.best_score = score  # 최고 점수 갱신
            self.save_state()  # 변경 상태 저장

    def add_quiz(self):
        question = input("질문을 입력하세요: ")  # 질문 입력
        choice_1 = input("1번 보기를 입력하세요: ")  # 1번 보기 입력
        choice_2 = input("2번 보기를 입력하세요: ")  # 2번 보기 입력
        choice_3 = input("3번 보기를 입력하세요: ")  # 3번 보기 입력
        choice_4 = input("4번 보기를 입력하세요: ")  # 4번 보기 입력
        answer = self._input_int_in_range("정답 번호를 입력하세요: ", 1, 4)  # 정답 번호 입력

        choices = [  # 보기 목록 생성
            f"1. {choice_1}",  # 첫 번째 보기
            f"2. {choice_2}",  # 두 번째 보기
            f"3. {choice_3}",  # 세 번째 보기
            f"4. {choice_4}",  # 네 번째 보기
        ]
        self.quizzes.append(Quiz(question, choices, str(answer)))  # 새 퀴즈 추가
        self.save_state()  # 변경 상태 저장
        print("퀴즈가 추가되었습니다.")  # 완료 문구 출력

    def list_quizzes(self):
        if not self.quizzes:  # 퀴즈 목록 비어있는지 확인
            print("등록된 퀴즈가 없습니다.")  # 안내 문구 출력
            return  # 함수 종료

        print("\n[퀴즈 목록 확인]")  # 목록 제목 출력
        for index, quiz in enumerate(self.quizzes, start=1):  # 퀴즈 목록 순회
            print(f"{index}. {quiz.question}")  # 번호와 질문 출력

    def show_best_score(self):
        print(f"최고 점수: {self.best_score}")  # 최고 점수 출력
