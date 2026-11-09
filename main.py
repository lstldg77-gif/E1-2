import json
import random
from pathlib import Path


STATE_FILE = Path(__file__).resolve().parent / "state.json"


class Quiz:
    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        if (not isinstance(choices, list) or len(choices) != 4
                or any(not isinstance(choice, str) or not choice.strip() for choice in choices)):
            raise ValueError("선택지는 비어 있지 않은 문자열 4개여야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4까지의 숫자여야 합니다.")
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number):
        print(f"\n[문제 {number}] {self.question}")
        for index, choice in enumerate(self.choices, 1):
            print(f"{index}. {choice}")

    def is_correct(self, answer):
        return self.answer == answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}


def default_quizzes():
    return [
        Quiz("Python에서 화면에 값을 출력하는 함수는?", ["print", "input", "open", "len"], 1),
        Quiz("여러 값을 순서대로 저장하는 자료형은?", ["int", "bool", "list", "float"], 3),
        Quiz("조건에 따라 코드를 실행하는 키워드는?", ["for", "if", "def", "import"], 2),
        Quiz("함수를 정의할 때 사용하는 키워드는?", ["class", "return", "while", "def"], 4),
        Quiz("JSON 파일을 처리할 때 사용하는 표준 모듈은?", ["random", "json", "math", "time"], 2),
    ]


def read_number(prompt, minimum, maximum):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if minimum <= number <= maximum:
                return number
        except ValueError:
            pass
        print(f"{minimum}부터 {maximum}까지의 숫자를 입력하세요.")


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("빈칸을 입력할 수 없습니다. 다시 입력하세요.")


class QuizGame:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = Path(state_file)
        self.quizzes = default_quizzes()
        self.best_score = None
        self.save_allowed = True
        self.load_state()

    def load_state(self):
        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                state = json.load(file)
            if not isinstance(state, dict) or not isinstance(state.get("quizzes"), list):
                raise ValueError("퀴즈 목록의 형식이 올바르지 않습니다.")
            quizzes = [Quiz(item["question"], item["choices"], item["answer"])
                       for item in state["quizzes"]]
            score = state["best_score"]
            if score is not None:
                if (not isinstance(score, dict) or type(score.get("correct")) is not int
                        or type(score.get("total")) is not int
                        or score["total"] <= 0 or not 0 <= score["correct"] <= score["total"]):
                    raise ValueError("최고 점수의 형식이 올바르지 않습니다.")
            self.quizzes = quizzes
            self.best_score = score
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        except FileNotFoundError:
            print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError, KeyError, TypeError):
            print("저장된 데이터가 손상되어 기본 퀴즈로 초기화합니다.")
        except OSError as error:
            self.save_allowed = False
            print(f"데이터를 읽을 수 없어 저장을 중지합니다: {error}")

    def save_state(self):
        if not self.save_allowed:
            print("기존 데이터를 보호하기 위해 저장하지 않았습니다.")
            return False
        state = {"quizzes": [quiz.to_dict() for quiz in self.quizzes],
                 "best_score": self.best_score}
        try:
            temporary_file = self.state_file.with_name(self.state_file.name + ".tmp")
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(state, file, ensure_ascii=False, indent=2)
            temporary_file.replace(self.state_file)
            return True
        except OSError as error:
            print(f"데이터를 저장하지 못했습니다: {error}")
            return False

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return
        correct = 0
        wrong_quizzes = []
        count = read_number(f"풀 문제 수 (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        quizzes = list(self.quizzes)
        random.shuffle(quizzes)
        quizzes = quizzes[:count]
        print(f"\n퀴즈를 시작합니다. (총 {len(quizzes)}문제, 무작위 순서)")
        for index, quiz in enumerate(quizzes, 1):
            quiz.display(index)
            answer = read_number("정답 번호 (1-4): ", 1, 4)
            if quiz.is_correct(answer):
                correct += 1
                print("정답입니다!")
            else:
                wrong_quizzes.append(quiz)
                print(f"오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}")
        total = len(quizzes)
        print(f"\n결과: {total}문제 중 {correct}문제 정답 ({correct / total * 100:.1f}점)")
        if wrong_quizzes:
            print("\n[오답 노트]")
            for quiz in wrong_quizzes:
                print(f"- {quiz.question} → 정답: {quiz.choices[quiz.answer - 1]}")
        if (self.best_score is None
                or correct * self.best_score["total"] > self.best_score["correct"] * total):
            self.best_score = {"correct": correct, "total": total}
            print("새로운 최고 점수입니다!")
            self.save_state()

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {index}: ") for index in range(1, 5)]
        answer = read_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("퀴즈가 추가되고 저장되었습니다.")
        else:
            print("퀴즈가 추가되었지만 파일에는 저장되지 않았습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for index, quiz in enumerate(self.quizzes, 1):
            print(f"[{index}] {quiz.question}")

    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_number(f"삭제할 퀴즈 번호 (0: 취소, 1-{len(self.quizzes)}): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)
        if self.save_state():
            print(f"'{removed.question}' 퀴즈를 삭제하고 저장했습니다.")
        else:
            print("퀴즈를 삭제했지만 파일에는 저장되지 않았습니다.")

    def show_score(self):
        if self.best_score is None:
            print("아직 퀴즈를 푼 기록이 없습니다.")
            return
        correct = self.best_score["correct"]
        total = self.best_score["total"]
        print(f"최고 점수: {correct / total * 100:.1f}점 ({total}문제 중 {correct}문제 정답)")

    def run(self):
        menu = [
            ("퀴즈 풀기", self.play),
            ("퀴즈 추가", self.add_quiz),
            ("퀴즈 목록", self.list_quizzes),
            ("퀴즈 삭제", self.delete_quiz),
            ("점수 확인", self.show_score),
            ("종료", None),
        ]
        try:
            while True:
                print("\n========== 파이썬 입문 퀴즈 ==========")
                for number, (title, _) in enumerate(menu, 1):
                    print(f"{number}. {title}")
                _, action = menu[read_number("선택: ", 1, len(menu)) - 1]
                if action is None:
                    print("게임을 종료합니다.")
                    break
                action()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 종료되어 게임을 안전하게 종료합니다.")
        finally:
            self.save_state()


def main():
    QuizGame().run()


if __name__ == "__main__":
    main()