import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from main import Quiz, QuizGame, read_number, read_text


class QuizGameTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.state_file = Path(self.directory.name) / "state.json"
        shuffle_patch = patch("main.random.shuffle")
        self.shuffle = shuffle_patch.start()
        self.addCleanup(shuffle_patch.stop)
        with redirect_stdout(io.StringIO()):
            self.game = QuizGame(self.state_file)

    def test_default_quizzes(self):
        self.assertGreaterEqual(len(self.game.quizzes), 5)
        self.assertTrue(all(isinstance(quiz, Quiz) for quiz in self.game.quizzes))

    def test_quiz_rejects_invalid_data(self):
        invalid_cases = [
            ("", ["a", "b", "c", "d"], 1),
            ("문제", ["a", "b", "c"], 1),
            ("문제", ["a", "b", " ", "d"], 1),
            ("문제", ["a", "b", "c", "d"], 5),
            ("문제", ["a", "b", "c", "d"], True),
            ("문제", ["a", "b", "c", "d"], "1"),
        ]
        for question, choices, answer in invalid_cases:
            with self.subTest(question=question, choices=choices, answer=answer):
                with self.assertRaises(ValueError):
                    Quiz(question, choices, answer)

    def test_quiz_round_trip_and_answer_check(self):
        quiz = Quiz("문제", ["a", "b", "c", "d"], 3)
        restored = Quiz(**quiz.to_dict())
        self.assertEqual(restored.to_dict(), quiz.to_dict())
        self.assertTrue(restored.is_correct(3))
        self.assertFalse(restored.is_correct(1))

    def test_menu_exit_saves_state(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["7", "6"]), redirect_stdout(output):
            self.game.run()
        self.assertIn("게임을 종료합니다", output.getvalue())
        self.assertTrue(self.state_file.exists())

    def test_input_retries_invalid_values(self):
        with patch("builtins.input", side_effect=["", "abc", "0", "9", " 2 "]), redirect_stdout(io.StringIO()):
            self.assertEqual(read_number("선택: ", 1, 5), 2)
        with patch("builtins.input", side_effect=["  ", " 문제 "]), redirect_stdout(io.StringIO()):
            self.assertEqual(read_text("문제: "), "문제")

    def test_added_quiz_and_score_survive_restart(self):
        answers = ["새 문제", "하나", "둘", "셋", "넷", "2"]
        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            self.game.add_quiz()
            with patch("builtins.input", side_effect=["6"] + [str(quiz.answer) for quiz in self.game.quizzes]):
                self.game.play()
            restarted = QuizGame(self.state_file)
        self.assertEqual(len(restarted.quizzes), 6)
        self.assertEqual(restarted.quizzes[-1].question, "새 문제")
        self.assertEqual(restarted.best_score, {"correct": 6, "total": 6})

    def test_best_score_compares_percentages(self):
        self.game.best_score = {"correct": 4, "total": 5}
        with patch("builtins.input", side_effect=["5", "1", "2", "1", "1", "1"]), redirect_stdout(io.StringIO()):
            self.game.play()
        self.assertEqual(self.game.best_score, {"correct": 4, "total": 5})

    def test_play_shuffles_copy_of_quizzes(self):
        original = list(self.game.quizzes)
        self.shuffle.side_effect = lambda items: items.reverse()
        answers = ["5"] + [str(quiz.answer) for quiz in reversed(original)]
        with patch("builtins.input", side_effect=answers), redirect_stdout(io.StringIO()):
            self.game.play()
        self.shuffle.assert_called_once()
        self.assertEqual(self.game.quizzes, original)
        self.assertEqual(self.game.best_score, {"correct": 5, "total": 5})

    def test_play_selected_number_of_quizzes(self):
        first, second = self.game.quizzes[:2]
        answers = ["0", "6", "2", str(first.answer), str(second.answer % 4 + 1)]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            self.game.play()
        self.assertEqual(self.game.best_score, {"correct": 1, "total": 2})
        review = output.getvalue().split("[오답 노트]")[1]
        self.assertIn(second.question, review)
        self.assertNotIn(first.question, review)

    def test_no_review_when_all_correct(self):
        answers = ["5"] + [str(quiz.answer) for quiz in self.game.quizzes]
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            self.game.play()
        self.assertNotIn("[오답 노트]", output.getvalue())

    def test_corrupt_json_and_invalid_schema_use_defaults(self):
        for contents in ("{broken", json.dumps({"quizzes": [], "best_score": {"correct": 2, "total": 0}})):
            self.state_file.write_text(contents, encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                game = QuizGame(self.state_file)
            self.assertEqual(len(game.quizzes), 5)
            self.assertIsNone(game.best_score)

    def test_delete_quiz_saves_and_cancel_keeps(self):
        first_question = self.game.quizzes[0].question
        with patch("builtins.input", side_effect=["0"]), redirect_stdout(io.StringIO()):
            self.game.delete_quiz()
        self.assertEqual(len(self.game.quizzes), 5)
        with patch("builtins.input", side_effect=["9", "1"]), redirect_stdout(io.StringIO()):
            self.game.delete_quiz()
            restarted = QuizGame(self.state_file)
        self.assertEqual(len(restarted.quizzes), 4)
        self.assertNotIn(first_question, [quiz.question for quiz in restarted.quizzes])

    def test_menu_runs_delete_and_exits(self):
        with patch("builtins.input", side_effect=["4", "1", "6"]), redirect_stdout(io.StringIO()):
            self.game.run()
        saved = json.loads(self.state_file.read_text(encoding="utf-8"))
        self.assertEqual(len(saved["quizzes"]), 4)

    def test_empty_quiz_list(self):
        self.game.quizzes = []
        output = io.StringIO()
        with redirect_stdout(output):
            self.game.play()
            self.game.list_quizzes()
            self.game.delete_quiz()
            self.game.show_score()
        self.assertIn("등록된 퀴즈가 없습니다", output.getvalue())
        self.assertIn("삭제할 퀴즈가 없습니다", output.getvalue())
        self.assertIn("아직 퀴즈를 푼 기록이 없습니다", output.getvalue())

    def test_interrupt_and_eof_save_and_exit(self):
        for exception in (KeyboardInterrupt, EOFError):
            with patch("builtins.input", side_effect=exception), redirect_stdout(io.StringIO()):
                self.game.run()
            self.assertTrue(self.state_file.exists())
            self.assertEqual(len(json.loads(self.state_file.read_text(encoding="utf-8"))["quizzes"]), 5)

    def test_write_error_is_reported(self):
        self.game.state_file = self.state_file / "missing" / "state.json"
        output = io.StringIO()
        with redirect_stdout(output):
            saved = self.game.save_state()
        self.assertFalse(saved)
        self.assertIn("저장하지 못했습니다", output.getvalue())

    def test_read_error_prevents_overwrite(self):
        with patch.object(Path, "open", side_effect=PermissionError("접근 거부")), redirect_stdout(io.StringIO()):
            game = QuizGame(self.state_file)
        self.assertFalse(game.save_allowed)
        with redirect_stdout(io.StringIO()):
            self.assertFalse(game.save_state())
        self.assertFalse(self.state_file.exists())


if __name__ == "__main__":
    unittest.main()