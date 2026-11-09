# 실행 결과 보관

과제 요구사항을 확인할 수 있는 실제 실행 기록을 모아 둔 폴더입니다. 전체 설명은 [프로젝트 README](../README.md)에 있습니다.

| 파일 | 내용 | 확인할 수 있는 요구사항 |
| --- | --- | --- |
| [run_1_first.txt](run_1_first.txt) | 데이터 파일이 없는 상태에서 모든 메뉴를 사용한 화면 기록 | 메뉴별 화면, 풀기/추가/목록/점수 동작 |
| [run_2_restart.txt](run_2_restart.txt) | 종료 후 다시 실행한 화면 기록 | 추가한 퀴즈와 최고 점수 유지 |
| [run_3_bonus_history.txt](run_3_bonus_history.txt) | 이어서 한 판 더 하고 게임 기록을 확인한 화면 기록 | 보너스: 점수 기록 히스토리 |
| [state_result.json](state_result.json) | 세 번의 실행을 마친 뒤 저장된 데이터 사본 | `state.json` 저장 형식 (UTF-8) |
| [git_history.txt](git_history.txt) | 커밋 그래프, 브랜치, checkout/merge/clone/pull 기록 | GitHub 커밋·브랜치·clone·pull |
| [screenshots/](screenshots/) | 실행 장면 이미지 11장 | 아래 표 참고 |

## 1. 첫 실행 (run_1_first.txt)

| 단계 | 입력 | 결과 |
| --- | --- | --- |
| 시작 | - | "저장된 데이터가 없어 기본 퀴즈를 사용합니다." |
| 퀴즈 목록 | `3` | 기본 퀴즈 5개 |
| 퀴즈 추가 | `2` → "리스트의 길이를 구하는 함수는?" / len, size, count, length / 정답 `1` | "퀴즈가 추가되고 저장되었습니다." |
| 퀴즈 목록 | `3` | 퀴즈 6개 |
| 퀴즈 풀기 | `1` → 풀 문제 수 `6` | 6문제 중 5문제 정답 (83.3점), 새로운 최고 점수 |
| 점수 확인 | `5` | 최고 점수 83.3점, 게임 기록 1회 |
| 퀴즈 삭제 | `4` → `0` | "삭제를 취소했습니다." |
| 잘못된 입력 | `abc`, `9` | "1부터 6까지의 숫자를 입력하세요." |
| 종료 | `6` | "게임을 종료합니다." |

오답 노트에는 틀린 문제 1개가 표시되었습니다.

```text
[오답 노트]
- Python에서 화면에 값을 출력하는 함수는? → 정답: print
```

## 2. 재실행 (run_2_restart.txt)

| 단계 | 입력 | 결과 |
| --- | --- | --- |
| 시작 | - | "저장된 데이터를 불러왔습니다. (퀴즈 6개)" |
| 퀴즈 목록 | `3` | 추가한 6번 문제가 그대로 있음 |
| 점수 확인 | `5` | 최고 점수 83.3점과 게임 기록 1회가 그대로 있음 |
| 종료 | `6` | "게임을 종료합니다." |

## 3. 보너스: 점수 기록 히스토리 (run_3_bonus_history.txt)

| 단계 | 입력 | 결과 |
| --- | --- | --- |
| 시작 | - | "저장된 데이터를 불러왔습니다. (퀴즈 6개)" |
| 퀴즈 풀기 | `1` → 풀 문제 수 `3` | 3문제 중 3문제 정답 (100.0점), 새로운 최고 점수 |
| 점수 확인 | `5` | 최고 점수 100.0점, 게임 기록 2회 |
| 종료 | `6` | "게임을 종료합니다." |

```text
[게임 기록] (총 2회)
1. 2026-11-09 18:26:37 | 6문제 중 5문제 정답 | 83.3점
2. 2026-11-09 18:26:38 | 3문제 중 3문제 정답 | 100.0점
```

## 4. 저장된 데이터 (state_result.json)

세 번의 실행을 마친 뒤의 상태입니다. 퀴즈 6개(기본 5개와 추가 1개), 최고 점수 `{"correct": 3, "total": 3}`, 게임 기록 2개가 UTF-8로 저장되어 있습니다.

실제 게임은 프로젝트 루트의 `state.json`을 사용합니다. 이 파일은 개인 데이터라 `.gitignore`로 GitHub 업로드에서 제외했고, 이 폴더의 `state_result.json`은 결과 확인용 사본입니다.

## 5. 실행 장면 이미지 (screenshots/)

| 파일 | 장면 |
| --- | --- |
| [01_menu_and_list.png](screenshots/01_menu_and_list.png) | 프로그램 시작, 메뉴, 퀴즈 목록 (기본 5개) |
| [02_add_quiz.png](screenshots/02_add_quiz.png) | 퀴즈 추가 후 목록에서 6개 확인 |
| [03_play_quiz.png](screenshots/03_play_quiz.png) | 퀴즈 풀기 6문제, 점수, 오답 노트 |
| [04_score.png](screenshots/04_score.png) | 최고 점수와 게임 기록 확인 |
| [05_delete_cancel.png](screenshots/05_delete_cancel.png) | 퀴즈 삭제 메뉴 (취소) |
| [06_invalid_input_and_exit.png](screenshots/06_invalid_input_and_exit.png) | 잘못된 입력 안내와 종료 |
| [07_restart_data_kept.png](screenshots/07_restart_data_kept.png) | 다시 실행했을 때 퀴즈 6개, 최고 점수, 게임 기록 유지 |
| [08_dev_env_and_tests.png](screenshots/08_dev_env_and_tests.png) | Python·Git 버전, 테스트 21개 통과 |
| [09_git_log_graph.png](screenshots/09_git_log_graph.png) | 커밋 그래프와 브랜치 목록 |
| [10_git_branch_clone_pull.png](screenshots/10_git_branch_clone_pull.png) | checkout, merge, clone, pull 기록과 원격 저장소 |
| [11_bonus_score_history.png](screenshots/11_bonus_score_history.png) | 보너스: 한 판 더 풀고 게임 기록 2회 확인 |

게임 장면(01~07, 11)은 실행 기록 `run_*.txt`의 출력을 터미널 화면 모양으로 그린 것입니다. 08~10은 이미지를 만들 때 해당 명령을 실제로 실행한 출력입니다. 입력값은 노란색, 정답은 초록색, 오답과 오류 안내는 빨간색으로 표시했습니다.
