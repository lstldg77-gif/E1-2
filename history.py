"""보너스 과제: 점수 기록 히스토리.

게임을 한 번 마칠 때마다 날짜/시간, 푼 문제 수, 맞힌 문제 수, 점수를 기록한다.
"""
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class GameRecord:
    def __init__(self, played_at, correct, total):
        if not isinstance(played_at, str):
            raise ValueError("기록 시간의 형식이 올바르지 않습니다.")
        datetime.strptime(played_at, TIME_FORMAT)
        if type(correct) is not int or type(total) is not int or total <= 0 or not 0 <= correct <= total:
            raise ValueError("게임 기록의 점수 형식이 올바르지 않습니다.")
        self.played_at = played_at
        self.correct = correct
        self.total = total

    @classmethod
    def create(cls, correct, total):
        return cls(datetime.now().strftime(TIME_FORMAT), correct, total)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("게임 기록의 형식이 올바르지 않습니다.")
        return cls(data["played_at"], data["correct"], data["total"])

    @property
    def score(self):
        return round(self.correct / self.total * 100, 1)

    def to_dict(self):
        return {"played_at": self.played_at, "total": self.total,
                "correct": self.correct, "score": self.score}

    def summary(self):
        return f"{self.played_at} | {self.total}문제 중 {self.correct}문제 정답 | {self.score:.1f}점"
