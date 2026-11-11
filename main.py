import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    # 문제와 선택지 출력
    def show_question(self):
        print("\n" + self.question)

        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    # 정답 확인
    def check_answer(self, user_answer):
        return user_answer == self.answer


# 초기 퀴즈 데이터 생성
def create_initial_quizzes():
    quizzes = [
        Quiz(
            "1. AI는 무엇의 약자일까요?",
            [
                "Artificial Intelligence",
                "Automatic Internet",
                "Advanced Information",
                "Artificial Integration"
            ],
            1
        ),
        Quiz(
            "2. 머신러닝의 주요 특징은 무엇일까요?",
            [
                "컴퓨터를 직접 조립한다",
                "데이터를 통해 패턴을 학습한다",
                "인터넷 속도를 높인다",
                "파일을 자동 삭제한다"
            ],
            2
        ),
        Quiz(
            "3. 딥러닝은 어떤 기술을 기반으로 할까요?",
            [
                "인공신경망",
                "스프레드시트",
                "웹 브라우저",
                "운영체제"
            ],
            1
        ),
        Quiz(
            "4. 생성형 AI의 대표적인 기능은 무엇일까요?",
            [
                "컴퓨터 전원 끄기",
                "새로운 텍스트와 이미지 생성",
                "인터넷 케이블 연결",
                "하드웨어 수리"
            ],
            2
        ),
        Quiz(
            "5. 자연어 처리(NLP)는 무엇을 다루는 기술일까요?",
            [
                "사람의 언어",
                "컴퓨터 부품",
                "네트워크 장비",
                "전기 회로"
            ],
            1
        ),
        Quiz(
            "6. 컴퓨터 비전은 어떤 분야일까요?",
            [
                "음악 작곡",
                "이미지와 영상 분석",
                "데이터 백업",
                "문서 인쇄"
            ],
            2
        ),
        Quiz(
            "7. AI 윤리에서 중요하게 다루는 것은 무엇일까요?",
            [
                "컴퓨터 색상",
                "키보드 종류",
                "개인정보 보호와 공정성",
                "모니터 크기"
            ],
            3
        )
    ]

    return quizzes


# 퀴즈 게임 관리 클래스
class QuizGame:
    def __init__(self):
        self.state_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "state.json"
        )

        self.quizzes = create_initial_quizzes()
        self.best_score = 0

        self.load_data()
    # 메인 메뉴 출력
    def show_menu(self):
        print("\n========== AI Knowledge Quiz ==========")
        print("1. 퀴즈 시작")
        print("2. 문제 등록")
        print("3. 문제 모아보기")
        print("4. 나의 기록")
        print("5. 프로그램 종료")
        print("6. 문제 수정")
        print("7. 문제 삭제")
        print("=======================================")

    # 메뉴 선택 및 실행
    def run(self):
        while True:
            self.show_menu()
            choice = input("메뉴를 선택하세요: ")

            if choice == "1":
                self.play_quiz()

            elif choice == "2":
                self.add_quiz()

            elif choice == "3":
                self.show_quizzes()

            elif choice == "4":
                self.show_record()

            elif choice == "6":
                self.edit_quiz()

            elif choice == "7":
                self.delete_quiz()

            elif choice == "5":
                print("퀴즈 프로그램을 종료합니다.")
                break

            else:
                print("잘못된 메뉴입니다. 1~5 사이의 숫자를 입력하세요.")

    # 전체 퀴즈 개수 확인
    def show_quiz_count(self):
        print(f"\n현재 등록된 퀴즈: {len(self.quizzes)}개")

    # 퀴즈 진행
    def play_quiz(self):
        score = 0

        print("\n========== 퀴즈 시작 ==========")

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{i}/{len(self.quizzes)}]")
            quiz.show_question()

            while True:
                try:
                    user_answer = int(input("정답 번호를 입력하세요 (1~4): "))

                    if 1 <= user_answer <= len(quiz.choices):
                        break

                    print("1~4 사이의 숫자를 입력하세요.")

                except ValueError:
                    print("숫자로 입력해야 합니다.")

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print("\n========== 퀴즈 종료 ==========")
        print(f"최종 점수: {score}/{len(self.quizzes)}")

        # 최고 점수 갱신
        if score > self.best_score:
            self.best_score = score
            print("최고 점수가 갱신되었습니다!")
            self.save_data()

    # 새로운 퀴즈 등록
    def add_quiz(self):
        print("\n========== 새 문제 등록 ==========")

        question = input("문제를 입력하세요: ").strip()

        if not question:
            print("문제 내용은 비워둘 수 없습니다.")
            return

        choices = []

        for i in range(4):
            while True:
                choice = input(f"{i + 1}번 선택지를 입력하세요: ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("선택지 내용은 비워둘 수 없습니다.")

        while True:
            try:
                answer = int(input("정답 번호를 입력하세요 (1~4): "))

                if 1 <= answer <= 4:
                    break

                print("정답은 1~4 사이의 숫자로 입력하세요.")

            except ValueError:
                print("숫자로 입력해야 합니다.")

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_data()

        print("\n새로운 문제가 등록되었습니다!")
        self.show_quiz_count()

        # 등록된 퀴즈 수정
    def edit_quiz(self):
        print("\n========== 문제 수정 ==========")

        if not self.quizzes:
            print("수정할 문제가 없습니다.")
            return

        self.show_quizzes()

        # 수정할 문제 번호 확인
        while True:
            try:
                quiz_number = input(
                    "\n수정할 문제 번호를 입력하세요 (취소: 0): "
                ).strip()

                if quiz_number == "0":
                    print("문제 수정이 취소되었습니다.")
                    return

                quiz_number = int(quiz_number)

                if 1 <= quiz_number <= len(self.quizzes):
                    break

                print("존재하는 문제 번호를 입력하세요.")

            except ValueError:
                print("숫자로 입력해야 합니다.")

            except (EOFError, KeyboardInterrupt):
                print("\n문제 수정이 취소되었습니다.")
                return

        # 기존 문제를 임시 변수에 복사
        quiz = self.quizzes[quiz_number - 1]

        new_question = quiz.question
        new_choices = quiz.choices.copy()
        new_answer = quiz.answer

        try:
            print("\n========== 수정할 내용 입력 ==========")
            print("Enter를 누르면 기존 내용이 유지됩니다.")

            # 문제 수정
            print(f"\n기존 문제: {new_question}")
            question_input = input("새로운 문제: ").strip()

            if question_input:
                new_question = question_input

            # 선택지 수정
            for i in range(4):
                print(f"\n기존 {i + 1}번 선택지: {new_choices[i]}")

                choice_input = input(
                    f"새로운 {i + 1}번 선택지: "
                ).strip()

                if choice_input:
                    new_choices[i] = choice_input

            # 정답 수정
            while True:
                answer_input = input(
                    f"\n새로운 정답 번호 (현재 {new_answer}번): "
                ).strip()

                if answer_input == "":
                    break

                try:
                    answer_input = int(answer_input)

                    if 1 <= answer_input <= 4:
                        new_answer = answer_input
                        break

                    print("1~4 사이의 숫자를 입력하세요.")

                except ValueError:
                    print("숫자로 입력해야 합니다.")

            # 수정 내용 최종 확인
            print("\n========== 수정 내용 확인 ==========")
            print(new_question)

            for i, choice in enumerate(new_choices, start=1):
                print(f"{i}. {choice}")

            print(f"정답: {new_answer}번")

            confirm = input("\n수정 내용을 저장할까요? (y/n): ").strip().lower()

            if confirm != "y":
                print("수정이 취소되었습니다.")
                return

            # 모든 입력이 끝난 후 실제 데이터에 반영
            quiz.question = new_question
            quiz.choices = new_choices
            quiz.answer = new_answer

            self.save_data()

            print("\n문제가 성공적으로 수정되었습니다!")

        except (EOFError, KeyboardInterrupt):
            print("\n수정이 취소되었습니다. 기존 문제는 유지됩니다.")
            return

    
    # 등록된 퀴즈 삭제
    def delete_quiz(self):
        print("\n========== 문제 삭제 ==========")

        if not self.quizzes:
            print("삭제할 문제가 없습니다.")
            return

        self.show_quizzes()

        while True:
            try:
                quiz_number = input(
                    "\n삭제할 문제 번호를 입력하세요 (취소: 0): "
                ).strip()

                if quiz_number == "0":
                    print("문제 삭제가 취소되었습니다.")
                    return

                quiz_number = int(quiz_number)

                if 1 <= quiz_number <= len(self.quizzes):
                    break

                print("존재하는 문제 번호를 입력하세요.")

            except ValueError:
                print("숫자로 입력해야 합니다.")

            except (EOFError, KeyboardInterrupt):
                print("\n문제 삭제가 취소되었습니다.")
                return

        # 삭제할 문제 확인
        quiz = self.quizzes[quiz_number - 1]

        print("\n========== 삭제할 문제 확인 ==========")
        print(quiz.question)

        confirm = input(
            "\n정말 삭제하시겠습니까? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("문제 삭제가 취소되었습니다.")
            return

        # 문제 삭제 및 저장
        self.quizzes.pop(quiz_number - 1)
        self.save_data()

        print("\n문제가 성공적으로 삭제되었습니다!")


    # 등록된 퀴즈 목록 출력
    def show_quizzes(self):
        print("\n========== 등록된 퀴즈 목록 ==========")

        if not self.quizzes:
            print("등록된 문제가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n{i}. {quiz.question}")

            for j, choice in enumerate(quiz.choices, start=1):
                print(f"   {j}. {choice}")

        print("\n=====================================")
        self.show_quiz_count()

    # 나의 기록 확인
    def show_record(self):
        print("\n========== 나의 기록 ==========")
        print(f"등록된 문제 수: {len(self.quizzes)}개")
        print(f"최고 점수: {self.best_score}/{len(self.quizzes)}")
        print("================================")

        # JSON 파일에서 데이터 불러오기
    def load_data(self):
        if not os.path.exists(self.state_file):
            print("저장된 데이터가 없습니다. 기본 데이터를 사용합니다.")
            self.save_data()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("JSON 데이터 형식이 올바르지 않습니다.")

            saved_quizzes = data["quizzes"]

            if not isinstance(saved_quizzes, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            loaded_quizzes = []

            for item in saved_quizzes:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제 내용이 올바르지 않습니다.")

                if not isinstance(choices, list) or len(choices) != 4:
                    raise ValueError("선택지 형식이 올바르지 않습니다.")

                if not all(
                    isinstance(choice, str) and choice.strip()
                    for choice in choices
                ):
                    raise ValueError("선택지 내용이 올바르지 않습니다.")

                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호가 올바르지 않습니다.")

                loaded_quizzes.append(Quiz(question, choices, answer))

            best_score = data.get("best_score", 0)

            if type(best_score) is not int or not 0 <= best_score <= len(loaded_quizzes):
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            self.quizzes = loaded_quizzes
            self.best_score = best_score

            print("저장된 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"저장 데이터에 문제가 있습니다: {e}")
            print("기본 데이터를 사용합니다.")

            self.quizzes = create_initial_quizzes()
            self.best_score = 0

    # JSON 파일에 데이터 저장하기
    def save_data(self):
        data = {
            "best_score": self.best_score,
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ]
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("데이터가 저장되었습니다!")

        except OSError as e:
            print(f"데이터 저장 중 오류가 발생했습니다: {e}")

# 프로그램 실행
if __name__ == "__main__":
    game = QuizGame()
    game.run()
