# 파이썬 입문 퀴즈

터미널에서 퀴즈를 풀고 직접 문제를 추가하는 Python 콘솔 게임입니다. 추가한 문제와 최고 점수는 프로그램을 종료해도 유지됩니다.

## 퀴즈 주제와 선정 이유

주제는 **Python 기초 문법**입니다. 프로그래밍을 처음 배우면서 출력, 자료형, 조건문, 함수, JSON을 퀴즈로 복습할 수 있도록 선택했습니다. 기본 문제는 5개입니다.

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

- 퀴즈 풀기: 저장된 모든 문제를 매번 무작위 순서로 풀고 문제별 정답과 최종 점수를 확인합니다. 저장된 문제 순서는 바뀌지 않습니다.
- 퀴즈 추가: 문제, 선택지 4개, 정답 번호를 입력해 저장합니다.
- 퀴즈 목록: 저장된 문제를 확인합니다.
- 퀴즈 삭제: 목록에서 번호를 골라 문제를 삭제하고 저장합니다. 0을 입력하면 취소합니다.
- 점수 확인: 최고 점수와 당시 정답 수 및 문제 수를 표시합니다.
- 종료: 데이터를 저장하고 프로그램을 종료합니다.
- 잘못된 숫자, 범위 밖 숫자, 빈 입력을 안내하고 다시 입력받습니다.
- Ctrl+C 또는 입력 종료 시 안내 후 가능한 범위에서 저장합니다. 진행 중이던 문제 등록이나 미완료 게임은 기록하지 않습니다.
- 데이터 파일이 없거나 손상되면 기본 문제를 사용합니다. 파일 읽기 오류 시 기존 데이터 보호를 위해 저장을 중지합니다.

최고 점수는 정답률로 비교합니다. 퀴즈 수가 달라져도 점수를 공정하게 비교할 수 있으며, 같은 정답률이면 기존 기록을 유지합니다.

## 파일 구조

```text
.
├── main.py        # Quiz, QuizGame 및 프로그램 진입점
├── test_main.py   # 표준 라이브러리 unittest를 사용한 테스트
├── README.md      # 프로젝트 설명과 실행 방법
├── .gitignore     # 개인 데이터와 캐시 제외
└── state.json     # 실행 후 생성되는 퀴즈와 점수 데이터
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

## Git과 GitHub 실습

Git을 설치하고 GitHub에 빈 공개 저장소를 만든 뒤, Git의 사용자 이름과 이메일을 설정하세요. 아래 주소는 실제 저장소 URL로 바꿉니다. 인증이 필요하면 GitHub의 공식 로그인 절차를 따르세요.

```powershell
git --version
git config --global user.name "GitHub 이름"
git config --global user.email "GitHub 이메일"
git init -b main
git add .gitignore README.md main.py test_main.py
git commit -m "Feat: 파이썬 퀴즈 게임 구현"
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

이 명령은 완성된 현재 파일을 첫 커밋으로 올리는 예시이며, 이것만으로는 과제의 **의미 있는 커밋 10개와 브랜치 병합** 조건을 충족하지 않습니다. 이후 직접 기능을 개선하고 각 변경을 검증하면서 기능별로 커밋하세요. 예를 들어 무작위 출제 기능을 별도 브랜치에서 구현하고 병합할 수 있습니다.

```powershell
git checkout -b feat/random-quiz
# 기능 구현 및 테스트 후
git add main.py test_main.py README.md
git commit -m "Feat: 문제 순서 무작위 출제"
git checkout main
git merge --no-ff feat/random-quiz -m "Merge: 무작위 출제 기능"
git push
git log --oneline --graph --all
```

총 10개 이상의 커밋은 실제 기능, 테스트, 문서 개선을 나눠 작성하고 `git log --oneline --graph --all`로 확인하세요. 커밋 수만 채우기 위한 내용 없는 커밋은 피합니다.

개발을 완료한 뒤 별도의 디렉터리에서 복제와 pull을 연습합니다. 아래 `<원본-프로젝트-경로>`는 이 프로젝트의 실제 경로로 바꾸세요.

```powershell
cd ..
git clone https://github.com/사용자명/저장소명.git quiz-clone
cd quiz-clone
# README.md에 실제 변경을 추가한 다음
git add README.md
git commit -m "Docs: README 설명 보완"
git push
cd <원본-프로젝트-경로>
git pull
git log --oneline --graph --all
```

GitHub 저장소 URL과 개발 환경, 메뉴/추가/목록/플레이/점수 화면, Git 로그 스크린샷은 직접 확인하고 제출하세요.