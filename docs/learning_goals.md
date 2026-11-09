# 과제 목표: 이 과제에서 배운 것

이 과제의 학습 목표 네 가지(Python 기초, 클래스와 객체, 파일 입출력, Git 기초)를 정리하고, 각 개념을 이 퀴즈 게임의 어느 코드에서 사용했는지 연결한 문서입니다. 전체 프로젝트 설명은 [README](../README.md)에 있습니다.

## 1. Python 기초

| 개념 | 한 줄 설명 | 비유 |
| --- | --- | --- |
| 변수 | 값에 이름을 붙여 저장 | 이름표 붙은 상자 |
| int / str / bool | 숫자 / 글자 / 참·거짓 | 계산기 숫자, 메모지 글씨, 스위치 ON·OFF |
| list | 순서 있는 여러 값, 번호로 꺼냄 | 번호 붙은 사물함 |
| dict | 키:값 쌍, 이름으로 꺼냄 | 사전 (단어 → 뜻) |
| if / elif / else | 조건에 따라 다른 행동 | 신호등: 빨강이면 멈춤, 초록이면 출발 |
| for | 정해진 대상을 끝까지 반복 | 출석부 이름을 처음부터 끝까지 부르기 |
| while | 조건이 맞는 동안 계속 반복 | 배부를 때까지 밥 먹기 |
| 함수 | 동작을 묶어 이름 붙임, 값 받고(매개변수) 돌려줌(return) | 자판기: 돈 넣으면 음료가 나옴 |

**핵심 한마디:** 데이터는 변수에 담고, 조건문으로 판단하고, 반복문으로 되풀이하고, 함수로 묶어서 재사용한다.

```python
def grade(score):          # 함수
    if score >= 80:        # 조건문
        return "합격"
    return "불합격"

for s in [90, 70]:         # 반복문
    print(grade(s))        # 합격, 불합격
```

**이 프로젝트에서 사용한 곳**

| 개념 | 사용한 코드 |
| --- | --- |
| 변수 | 맞힌 문제 수를 세는 `correct = 0` ([main.py:126](../main.py#L126)) |
| int / str / bool | 정답 번호 `answer`(int), 문제 `question`(str), 저장 가능 여부 `save_allowed`(bool) ([main.py:72](../main.py#L72)) |
| list | 퀴즈 목록 `self.quizzes`, 선택지 `choices` 4개 |
| dict | 최고 점수 `{"correct": correct, "total": total}` ([main.py:150](../main.py#L150)), 저장용 `to_dict()` |
| if / elif / else | 정답이면 "정답입니다!", 아니면 "오답입니다" ([main.py:136](../main.py#L136)) |
| for | 출제할 문제를 하나씩 보여 주는 `for index, quiz in enumerate(quizzes, 1)` ([main.py:133](../main.py#L133)) |
| while | 올바른 숫자가 들어올 때까지 다시 묻는 `while True` ([main.py:47](../main.py#L47)), 메뉴 반복 ([main.py:215](../main.py#L215)) |
| 함수 | `read_number(prompt, minimum, maximum)`: 매개변수로 범위를 받고 숫자를 `return` ([main.py:46](../main.py#L46)) |

```python
# main.py - 함수 + while + if
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
```

## 2. 클래스와 객체

| 개념 | 한 줄 설명 | 비유 |
| --- | --- | --- |
| 클래스 | 객체를 만드는 설계도 | 붕어빵 틀 |
| 객체 | 설계도로 만든 실제 것 | 붕어빵 하나하나 |
| `__init__` | 객체가 생길 때 처음 값을 넣는 곳 | 붕어빵에 팥/슈크림 넣기 |
| `self` | 지금 이 객체 자신 | "나의" 속재료 |
| 속성 | 객체가 가진 데이터 | 붕어빵의 맛, 크기 |
| 메서드 | 객체가 하는 동작 | 붕어빵을 "데우기" |

**핵심 한마디:** 클래스는 데이터와 기능을 한 덩어리로 묶어서, 같은 모양의 객체를 여러 개 쉽게 만들게 해 준다.

```python
class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check(self, user_answer):
        return user_answer == self.answer

q = Quiz("1+1은?", "2")
print(q.check("2"))   # True
```

**이 프로젝트에서 사용한 곳**

| 개념 | 사용한 코드 |
| --- | --- |
| 클래스 | `Quiz`(문제), `QuizGame`(게임 진행·저장), `GameRecord`(게임 기록, 보너스) |
| 객체 | 기본 문제 5개는 `Quiz` 객체 5개 ([main.py:36](../main.py#L36)), 게임 기록 한 줄은 `GameRecord` 객체 하나 |
| `__init__` | `Quiz.__init__`에서 문제·선택지·정답을 받아 검증한 뒤 저장 ([main.py:12](../main.py#L12)) |
| `self` | `self.question`, `self.choices`, `self.answer`: 각 문제 객체 자신의 값 |
| 속성 | `question`, `choices`, `answer` |
| 메서드 | `display`(문제 출력), `is_correct`(정답 확인), `to_dict`(저장용 변환) |

```python
# main.py - 위 예시의 check와 같은 역할을 하는 is_correct
class Quiz:
    def is_correct(self, answer):
        return self.answer == answer
```

## 3. 파일 입출력

| 개념 | 한 줄 설명 | 비유 |
| --- | --- | --- |
| 파일 열기/읽기/쓰기 | `open` → `read`/`write` → 닫기 | 공책 펴기 → 읽거나 쓰기 → 덮기 |
| `with` | 다 쓰면 자동으로 닫아 줌 | 자동으로 닫히는 문 |
| JSON | dict처럼 생긴 텍스트 저장 형식 | 누구나 읽을 수 있는 공용 양식 |
| try / except | 오류가 나도 멈추지 않고 대처 | 비 오면 우산 쓰기 (플랜 B) |

**핵심 한마디:** 프로그램을 꺼도 데이터가 남도록 JSON 파일에 저장하고, 파일이 없거나 깨져도 try/except로 안전하게 처리한다.

```python
import json
try:
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}   # 파일이 없으면 빈 데이터로 시작
```

**이 프로젝트에서 사용한 곳**

| 개념 | 사용한 코드 |
| --- | --- |
| 파일 열기/읽기/쓰기 | `state.json`을 UTF-8로 읽기 ([main.py:77](../main.py#L77)), 쓰기 ([main.py:115](../main.py#L115)) |
| `with` | `with self.state_file.open("r", encoding="utf-8") as file:` |
| JSON | `json.load`로 불러오고 `json.dump(..., ensure_ascii=False)`로 한글 그대로 저장 |
| try / except | 파일이 없으면 기본 퀴즈(`FileNotFoundError`, [main.py:97](../main.py#L97)), 깨졌으면 기본 퀴즈로 초기화, 읽기 오류면 저장 중지 |

```python
# main.py - load_state의 구조 (위 예시와 같은 흐름)
try:
    with self.state_file.open("r", encoding="utf-8") as file:
        state = json.load(file)
    ...
except FileNotFoundError:
    print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")
except (json.JSONDecodeError, UnicodeDecodeError, ValueError, KeyError, TypeError):
    print("저장된 데이터가 손상되어 기본 퀴즈로 초기화합니다.")
```

## 4. Git 기초

**Git이란?** 코드의 "세이브 파일" 관리 도구. 언제든 이전 상태로 돌아갈 수 있고, 여럿이 함께 작업할 수 있다. GitHub는 그 세이브를 올려 두는 온라인 저장소.

| 명령어 | 쉬운 뜻 | 비유 |
| --- | --- | --- |
| init | 이 폴더를 Git으로 관리 시작 | 게임 새로 시작 |
| add | 저장할 파일 고르기 | 택배 상자에 물건 담기 |
| commit | 메시지와 함께 기록 | 상자 봉인하고 송장 붙이기 |
| push | GitHub에 올리기 | 택배 보내기 |
| pull | GitHub의 새 내용 받아오기 | 택배 받기 |
| clone | 저장소 통째로 복사 | 남의 공책 전체 복사 |
| checkout | 다른 브랜치로 이동 | 다른 세이브 슬롯 불러오기 |
| branch / merge | 따로 작업하고 나중에 합치기 | 평행세계에서 실험 후 본편에 합치기 |

**핵심 한마디:** `add → commit → push`로 올리고, `clone`은 처음 한 번 복사, `pull`은 최신으로 맞추기. 브랜치로 안전하게 실험한 뒤 `merge`로 합친다.

```bash
git checkout -b feature   # 새 브랜치에서 작업
git add .
git commit -m "기능 추가"
git checkout main
git merge feature         # main에 합치기
git push origin main
```

**이 프로젝트에서 사용한 곳**

| 명령어 | 이 프로젝트에서 한 일 |
| --- | --- |
| init | `E1-2` 폴더를 Git 저장소로 만들고 `main` 브랜치에서 시작 |
| add / commit | 기능, 테스트, 문서를 나눠서 커밋 (총 20개 이상, `Feat:`, `Docs:`, `Test:` 형식) |
| push | GitHub 저장소 https://github.com/lstldg77-gif/E1-2 에 `main`과 기능 브랜치 업로드 |
| clone | 다른 폴더 `quiz-clone`에 저장소를 통째로 복사 |
| pull | `quiz-clone`에서 수정해 push한 내용을 원래 폴더에서 `git pull`로 받아옴 |
| checkout | `git checkout -b feat/score-history`로 브랜치를 만들고, 끝나면 `git checkout main`으로 돌아옴 |
| branch / merge | 무작위 출제, 퀴즈 삭제, 프로젝트 개요, 점수 기록 히스토리를 각각 브랜치에서 작업하고 `git merge --no-ff`로 4번 병합 |

```bash
# 보너스 기능을 브랜치에서 개발해 병합한 실제 순서
git checkout -b feat/score-history
git add history.py main.py test_main.py
git commit -m "Feat: 보너스 - 점수 기록 히스토리 저장과 조회"
git checkout main
git merge --no-ff feat/score-history -m "Merge: 보너스 점수 기록 히스토리"
git push origin main feat/score-history
```

## 30초 요약

1. **Python 기초**: 변수에 담고, if로 판단하고, for/while로 반복하고, 함수로 묶는다.
   → 퀴즈 채점(`if`), 문제 출제(`for`), 입력 재시도(`while`), `read_number` 함수
2. **클래스**: 붕어빵 틀(클래스)로 붕어빵(객체)을 찍어내고, `__init__`으로 속을 채운다.
   → `Quiz` 틀로 문제 객체를 만들고, `QuizGame`이 게임을 진행
3. **파일**: JSON으로 저장해서 꺼도 남게 하고, try/except로 오류에 대비한다.
   → `state.json`에 퀴즈·최고 점수·게임 기록 저장, 파일이 없거나 깨져도 기본 퀴즈로 시작
4. **Git**: add(담기) → commit(기록) → push(올리기), pull로 받아오고, 브랜치로 안전하게 작업한다.
   → 커밋 20개 이상, 브랜치 병합 4회, clone·pull 실습 완료
