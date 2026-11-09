# 파이썬 입문 퀴즈

터미널에서 퀴즈를 풀고 직접 문제를 추가하는 Python 콘솔 게임입니다. 추가한 문제와 최고 점수는 프로그램을 종료해도 유지됩니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초 문법**입니다. 프로그래밍을 처음 배우면서 출력, 자료형, 조건문, 함수, JSON을 퀴즈로 복습할 수 있도록 선택했습니다. 기본 문제는 5개입니다.

## 개발 환경

- OS: Windows 11 Pro
- Python: 3.11.6 (표준 라이브러리만 사용)
- Git: 2.56.0.windows.4
- 편집기: Visual Studio Code

## 실행 방법

Python 3.10 이상이 필요하며 외부 라이브러리는 사용하지 않습니다. 프로젝트 폴더에서 다음 명령을 실행합니다.

```powershell
python --version
python main.py
```

메뉴에서 번호를 입력합니다. Windows에서 `python` 명령이 동작하지 않으면 `py main.py`를 사용해 보세요.

자동 테스트 실행:

```powershell
python -m unittest -v
```

## 기능 목록

- 퀴즈 풀기: 풀 문제 수를 고른 뒤 저장된 문제 중에서 무작위 순서로 풀고 문제별 정답과 최종 점수를 확인합니다. 틀린 문제는 마지막에 오답 노트로 다시 보여 줍니다. 저장된 문제 순서는 바뀌지 않습니다.
- 퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력해 저장합니다.
- 퀴즈 목록: 저장된 문제를 확인합니다.
- 퀴즈 삭제: 목록에서 번호를 골라 문제를 삭제하고 저장합니다. 0을 입력하면 취소합니다.
- 점수 확인: 최고 점수와 당시 정답 수 및 문제 수를 표시합니다.
- 종료: 데이터를 저장하고 프로그램을 종료합니다.
- 잘못된 숫자, 범위 밖 숫자, 빈 입력을 안내하고 다시 입력받습니다.
- Ctrl+C 또는 입력 종료 시 안내 후 가능한 범위에서 저장합니다. 진행 중이던 문제 등록이나 미완료 게임은 기록하지 않습니다.
- 데이터 파일이 없거나 손상되면 기본 문제를 사용합니다. 파일 읽기 오류 시 기존 데이터 보호를 위해 저장을 중지합니다.

최고 점수는 정답률로 비교합니다. 풀 문제 수나 저장된 퀴즈 수가 달라져도 점수를 공정하게 비교할 수 있으며, 같은 정답률이면 기존 기록을 유지합니다.

## 실행 결과

데이터 파일이 없는 상태에서 모든 메뉴를 한 번씩 사용한 결과입니다. 화면별 기록은 [results/README.md](results/README.md), 전체 실행 기록은 [results/run_log.txt](results/run_log.txt), 저장된 데이터는 [results/state_result.json](results/state_result.json)에 있습니다.

| 단계 | 입력 | 결과 |
| --- | --- | --- |
| 퀴즈 목록 | `3` | 기본 퀴즈 5개 표시 |
| 퀴즈 추가 | `2` → 리스트의 길이를 구하는 함수는? / len, size, count, length / 정답 `1` | 저장 완료, 퀴즈 6개 |
| 퀴즈 풀기 | `1` → 풀 문제 수 `6` | 6문제 중 5문제 정답 (83.3점), 새로운 최고 점수 |
| 점수 확인 | `5` | 최고 점수 83.3점 (6문제 중 5문제 정답) |
| 퀴즈 삭제 | `4` → `0` | 삭제 취소 |
| 잘못된 입력 | `abc`, `9` | "1부터 6까지의 숫자를 입력하세요." 안내 후 재입력 |
| 종료 | `6` | 데이터 저장 후 종료 |

퀴즈 풀기 화면 (일부):

```text
퀴즈를 시작합니다. (총 6문제, 무작위 순서)

[문제 1] 여러 값을 순서대로 저장하는 자료형은?
1. int
2. bool
3. list
4. float
정답 번호 (1-4): 3
정답입니다!

[문제 3] JSON 파일을 처리할 때 사용하는 표준 모듈은?
1. random
2. json
3. math
4. time
정답 번호 (1-4): 3
오답입니다. 정답: 2. json

결과: 6문제 중 5문제 정답 (83.3점)

[오답 노트]
- JSON 파일을 처리할 때 사용하는 표준 모듈은? → 정답: json
새로운 최고 점수입니다!
```

## 파일 구조

```text
.
├── main.py        # Quiz, QuizGame 및 프로그램 진입점
├── test_main.py   # 표준 라이브러리 unittest를 사용한 테스트
├── README.md      # 프로젝트 설명과 실행 방법
├── .gitignore     # 개인 데이터와 캐시 제외
├── results/       # 실행 결과 보관
│   ├── README.md          # 화면별 실행 결과 정리
│   ├── run_log.txt        # 전체 실행 기록
│   └── state_result.json  # 실행 후 저장된 데이터 사본
└── state.json     # 실행 후 생성되는 퀴즈와 점수 데이터 (Git 제외)
```

## 데이터 파일

`state.json`은 프로젝트 루트에 UTF-8로 저장됩니다. `quizzes`는 문제 배열이고, 각 문제는 `question`, 선택지 4개인 `choices`, 1~4 사이의 정답 번호 `answer`로 구성됩니다. `best_score`는 아직 기록이 없으면 `null`, 기록이 있으면 정답 수 `correct`와 문제 수 `total`을 가진 객체입니다.

```json
{
  "quizzes": [
    {
      "question": "Python에서 화면에 값을 출력하는 함수는?",
      "choices": ["print", "input", "open", "len"],
      "answer": 1
    }
  ],
  "best_score": {"correct": 1, "total": 1}
}
```

위 JSON은 구조 설명을 위한 예시입니다. 처음 실행하면 기본 문제 5개가 사용되고 종료하거나 변경 사항을 저장할 때 파일이 생성됩니다. 파일을 삭제하면 다음 실행에 기본 문제부터 다시 시작합니다. 개인 퀴즈와 점수는 `.gitignore`에 포함되어 GitHub에 업로드되지 않습니다.

## Git과 GitHub

저장소: https://github.com/lstldg77-gif/E1-2

기능 단위로 커밋하고, 두 기능은 별도 브랜치에서 개발한 뒤 `main`에 `--no-ff`로 병합했습니다.

| 브랜치 | 작업 | 병합 커밋 |
| --- | --- | --- |
| `feat/random-quiz` | 문제 순서 무작위 출제, 문서 보완 | `Merge: 무작위 출제 기능` |
| `feat/delete-quiz` | 퀴즈 삭제 메뉴, 문서 보완 | `Merge: 퀴즈 삭제 기능` |

`main`에서는 풀 문제 수 선택, 오답 노트, 메뉴 리팩터링, 테스트 보강, 문서 정리를 각각 커밋했습니다. 전체 이력은 다음 명령으로 확인합니다.

```powershell
git log --oneline --graph --all
```

### 원격 저장소에 올리기

```powershell
git remote add origin https://github.com/lstldg77-gif/E1-2.git
git push -u origin main
git push origin feat/random-quiz feat/delete-quiz
```

### clone과 pull 실습

별도의 디렉터리에 저장소를 복제해 변경을 push하고, 원본 디렉터리에서 pull로 받아옵니다.

```powershell
cd ..
git clone https://github.com/lstldg77-gif/E1-2.git quiz-clone
cd quiz-clone
# README.md에 실제 변경을 추가한 다음
git add README.md
git commit -m "Docs: clone 환경에서 README 보완"
git push
cd ..\E1-2
git pull
git log --oneline --graph --all
```

제출할 때는 GitHub 저장소 URL과 개발 환경, 메뉴/추가/목록/삭제/플레이/점수 화면, Git 로그 스크린샷을 함께 냅니다.