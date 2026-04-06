import json
from quiz_bonus import DeleteQuiz, HintQuiz, QuizHistory, RandomQuiz
from input_handler import InputHandler


class QuizGame:
    """메인 게임 로직 및 상태를 관리하는 클래스"""

    def __init__(self):  # 게임 초기 상태 설정
        self.quizzes = []  # 퀴즈 목록
        self.best_score = 0  # 최고 점수
        self.has_played = False  # 퀴즈 응시 여부
        self.history = []  # 게임 기록 목록
        self.state_file = "state.json"  # 상태 저장 파일 경로
        self.default_state_file = "state_default.json"  # 기본 상태 파일 경로
        self.input_handler = InputHandler()  # 공통 입력/검증 처리기
        self.bonus_game = RandomQuiz()  # 보너스 출제 규칙 처리기
        self.delete_game = DeleteQuiz()  # 퀴즈 삭제 처리기
        self.history_game = QuizHistory()  # 게임 기록 처리기

    # --- 상태 저장/로드 영역 시작 ---

    def _reset_with_default_data(self):  # 기본 파일 기준 상태 복구
        with open(self.default_state_file, "r", encoding="utf-8") as file:  # 기본 상태 파일 읽기
            default_data = json.load(file)  # 기본 JSON 데이터 로드
        self.best_score = default_data.get("best_score", 0)  # 최고 점수 초기화
        self.has_played = default_data.get("has_played", False)  # 퀴즈 응시 여부 초기화
        self.history = default_data.get("history", [])  # 게임 기록 초기화
        validated = self.input_handler.validate_quizzes_data(default_data)  # 기본 데이터 유효성 검증
        self.quizzes = [HintQuiz(item["question"], item["choices"], item["answer"], item["hint"]) for item in validated]  # 기본 퀴즈 적용

    def load_state(self):  # 저장된 상태 파일 로드
        try:  # 저장된 상태 파일 로드 시도
            with open(self.state_file, "r", encoding="utf-8") as file:  # 저장된 상태 파일 읽기
                data = json.load(file)  # 저장된 상태 JSON 데이터 로드
            validated = self.input_handler.validate_quizzes_data(data)  # 저장된 상태 데이터 유효성 검증
            self.quizzes = [HintQuiz(item["question"], item["choices"], item["answer"], item["hint"]) for item in validated]  # 저장된 상태 퀴즈 적용
            self.best_score = data.get("best_score", 0)  # 최고 점수 불러오기
            self.has_played = data.get("has_played", False)  # 퀴즈 응시 여부 불러오기
            self.history = data.get("history", [])  # 게임 기록 불러오기
            if not self.quizzes:  # 퀴즈 비어 있음 확인
                raise ValueError("퀴즈 데이터가 비어 있습니다.")  # 비어 있는 퀴즈 데이터 예외 발생
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError):  # 로드 실패 예외 처리
            print("\n[기본 퀴즈 데이터로 복구]")  # 복구 안내 제목 출력
            print("state.json 파일을 불러올 수 없어 state_default.json 데이터를 불러옵니다.")  # 복구 안내 문구 출력
            self._reset_with_default_data()  # 기본 데이터로 상태 복구

    def save_state(self): # 현재 상태를 파일에 저장
        data = {  # 저장할 상태 데이터 구성
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],  # 퀴즈 목록을 딕셔너리 형태로 저장
            "best_score": self.best_score,  # 최고 점수 저장
            "has_played": self.has_played,  # 퀴즈 응시 여부 저장
            "history": self.history,  # 기록 목록 저장
        }
        with open(self.state_file, "w", encoding="utf-8") as file:  # 상태 파일 쓰기
            json.dump(data, file, ensure_ascii=False, indent=2)  # JSON 형태로 저장

    # --- 상태 저장/로드 영역 끝 ---
    # --- 퀴즈 게임 메뉴 영역 시작 ---

    def show_menu(self):
        print("\n파이썬 퀴즈 프로그램 시작")  # 프로그램 시작 문구 출력
        print("1. 퀴즈 풀기 / 2. 퀴즈 추가 / 3. 퀴즈 목록 / 4. 점수 확인 / 5. 퀴즈 삭제 / 6. 히스토리 / 7. 종료")  # 메뉴 출력
        return self.input_handler.input_int_in_range("메뉴를 입력하세요: ", 1, 7)  # 메뉴 번호 입력 반환

    def play_quiz(self):
        selected_quizzes = self.bonus_game.select_quizzes_for_play(self.quizzes, self.input_handler)  # 출제할 퀴즈 목록 결정
        result_marks = []  # 문제별 결과 기록 리스트
        for index, quiz in enumerate(selected_quizzes, start=1):  # 선택된 퀴즈 순회
            print(f"\n[{index}번 문제] {quiz.question}")  # 문제 번호와 질문 출력
            quiz.display()  # 문제와 보기 출력
            user_answer, used_hint_in_question = quiz.input_answer_with_optional_hint(self.input_handler)  # 정답/힌트 입력 처리
            is_correct = quiz.check_answer(str(user_answer))  # 정답 여부 확인
            if is_correct and used_hint_in_question:
                mark = "⚠️"  # 힌트 사용 후 정답
            elif is_correct:
                mark = "✅"  # 정답
            else:
                mark = "❌"  # 오답
            result_marks.append(mark)  # 결과 기록
            print(mark)  # 결과 출력
        score = result_marks.count("✅") + (result_marks.count("⚠️") * 0.5)  # 최종 점수 일괄 계산
        result_line = " / ".join([f"{index}. {mark}" for index, mark in enumerate(result_marks, start=1)])  # 최종 결과 라인 생성
        print("\n[결과 요약]")  # 결과 요약 제목 출력
        print(result_line)  # 문제별 최종 결과 출력
        print(f"\n점수: {score}")  # 결과 점수 출력
        self.history_game.append_record(self.history, len(selected_quizzes), score)  # 게임 기록 저장
        self.has_played = True  # 퀴즈 응시 여부 갱신
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
        hint = self.input_handler.input_non_empty_text("힌트를 입력하세요: ")  # 힌트 입력

        self.quizzes.append(HintQuiz(question, choices, str(answer), hint))  # 새 퀴즈 추가
        self.save_state()  # 변경 상태 저장
        print("퀴즈가 추가되었습니다.")  # 완료 문구 출력

    def list_quizzes(self):
        print("\n[퀴즈 목록 확인]")  # 목록 제목 출력
        for index, quiz in enumerate(self.quizzes, start=1):  # 퀴즈 목록 순회
            print(f"{index}. {quiz.question}")  # 번호와 질문 출력

    def show_best_score(self):
        if not self.has_played:  # 미응시 상태 확인
            print("아직 퀴즈를 풀지 않았습니다.")  # 미응시 안내 문구 출력
            return  # 함수 종료
        print(f"\n[최고 점수] {self.best_score}")  # 최고 점수 출력

    def delete_quiz(self):
        deleted = self.delete_game.delete_quiz_by_number(self.quizzes, self.input_handler)  # 번호 기반 퀴즈 삭제
        if deleted:
            self.save_state()  # 삭제 결과 파일 반영

    def show_history(self):
        print("\n[게임 히스토리]")
        if not self.history:
            print("기록이 없습니다.")
            return

        for index, record in enumerate(self.history, start=1):
            played_at = record.get("played_at", "-")
            question_count = record.get("question_count", 0)
            score = record.get("score", 0)
            print(f"{index}. {played_at} / 문제 수: {question_count} / 점수: {score}")

    # --- 퀴즈 게임 메뉴 영역 끝 ---