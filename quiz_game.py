import json
from quiz import Quiz
from input_handler import InputHandler


class QuizGame:
    """메인 게임 로직 및 상태를 관리하는 클래스"""

    def __init__(self):  # 게임 초기 상태 설정
        self.quizzes = []  # 퀴즈 목록
        self.best_score = 0  # 최고 점수
        self.state_file = "state.json"  # 상태 저장 파일 경로
        self.default_state_file = "state_default.json"  # 기본 상태 파일 경로
        self.input_handler = InputHandler()  # 공통 입력/검증 처리기

    def _reset_with_default_data(self):  # 기본 파일 기준 상태 복구
        with open(self.default_state_file, "r", encoding="utf-8") as file:  # 기본 상태 파일 읽기
            default_data = json.load(file)  # 기본 JSON 데이터 로드
        self.best_score = default_data.get("best_score", 0)  # 최고 점수 초기화
        validated = self.input_handler.validate_quizzes_data(default_data)  # 기본 데이터 유효성 검증
        self.quizzes = [Quiz(item["question"], item["choices"], item["answer"]) for item in validated]  # 기본 퀴즈 적용

    def load_state(self):  # 저장 상태 로드
        try:  # 저장된 상태 파일 로드 시도
            with open(self.state_file, "r", encoding="utf-8") as file:  # 저장된 상태 파일 읽기
                data = json.load(file)  # 저장된 상태 JSON 데이터 로드
            validated = self.input_handler.validate_quizzes_data(data)  # 저장된 상태 데이터 유효성 검증
            self.quizzes = [Quiz(item["question"], item["choices"], item["answer"]) for item in validated]  # 저장된 상태 퀴즈 적용
            self.best_score = data.get("best_score", 0)  # 최고 점수 불러오기
            if not self.quizzes:  # 퀴즈 비어 있음 확인
                raise ValueError("퀴즈 데이터가 비어 있습니다.")  # 복구 분기 유도
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):  # 로드 실패 예외 처리
            print("\n[기본 퀴즈 데이터로 복구]")  # 복구 안내 제목 출력
            print("state.json 파일을 불러올 수 없어 state_default.json 데이터를 불러옵니다.")  # 복구 사유 출력
            self._reset_with_default_data()  # 기본 데이터로 상태 복구

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
        return self.input_handler.input_int_in_range("메뉴를 입력하세요: ", 1, 5)  # 메뉴 번호 입력 반환

    def play_quiz(self):
        if not self.quizzes:  # 퀴즈가 없는 경우 확인
            print("등록된 퀴즈가 없습니다.")  # 안내 문구 출력
            return  # 함수 종료

        score = 0  # 현재 플레이 점수
        result_marks = []  # 문제별 정오 이모티콘 기록
        for index, quiz in enumerate(self.quizzes, start=1):  # 퀴즈 순회
            print(f"\n[{index}번 문제] {quiz.question}")  # 문제 번호와 질문 출력
            quiz.display()  # 문제와 보기 출력
            user_answer = self.input_handler.input_int_in_range("정답 번호를 입력하세요: ", 1, len(quiz.choices))  # 사용자 답 입력
            if quiz.check_answer(str(user_answer)):  # 정답 여부 확인
                score += 1  # 점수 증가
                result_marks.append("✅")  # 정답 기록
                print("✅")  # 정답 표시
            else:
                result_marks.append("❌")  # 오답 기록
                print("❌")  # 오답 표시

        result_line = " / ".join([f"{index}. {mark}" for index, mark in enumerate(result_marks, start=1)])  # 최종 결과 라인 생성
        print("\n[결과 요약]")  # 결과 요약 제목 출력
        print(result_line)  # 문제별 최종 결과 출력
        print(f"\n점수: {score}/{len(self.quizzes)}")  # 결과 점수 출력
        if score > self.best_score:  # 최고 점수 갱신 여부 확인
            self.best_score = score  # 최고 점수 갱신
            self.save_state()  # 변경 상태 저장

    def add_quiz(self):
        print("\n[새로운 퀴즈 등록]")  # 퀴즈 등록 제목 출력
        question = self.input_handler.input_non_empty_text("질문을 입력하세요: ")  # 질문 입력
        choices = []  # 보기 목록 생성
        for index in range(1, 5):  # 1~4번 보기 반복 입력
            choice_text = self.input_handler.input_non_empty_text(f"{index}번 보기를 입력하세요: ")  # 보기 입력
            choices.append(f"{index}. {choice_text}")  # 번호가 포함된 보기 저장
        answer = self.input_handler.input_int_in_range("정답 번호를 입력하세요: ", 1, 4)  # 정답 번호 입력

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
