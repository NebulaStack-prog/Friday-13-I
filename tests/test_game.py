import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

spec = importlib.util.spec_from_file_location("game", Path(__file__).resolve().parents[1] / "Friday13-I-New.py")
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class GameTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        original = game.SAVE_FILE
        self.addCleanup(setattr, game, "SAVE_FILE", original)
        game.SAVE_FILE = Path(self.temp.name) / "records.json"

    def test_records_roundtrip(self):
        records = game.load_records()
        records["1"]["best"] = 12
        self.assertTrue(game.save_records(records))
        self.assertEqual(game.load_records()["1"]["best"], 12)

    def test_corrupt_records(self):
        game.SAVE_FILE.write_text("invalid")
        self.assertEqual(game.load_records()["1"]["best"], 0)

    def test_levels(self):
        g = game.Game.__new__(game.Game)
        for key, size in [("1", 8), ("2", 12), ("3", 16)]:
            g.start_game(key)
            self.assertEqual(g.grid_size, size)
            self.assertEqual(g.maximum_score, size ** 2 - 1)
            self.assertNotIn(g.food, g.occupied)

    def test_full_board(self):
        g = game.Game.__new__(game.Game)
        g.grid_size = 2
        g.occupied = {(0, 0), (0, 1), (1, 0), (1, 1)}
        self.assertIsNone(g.spawn_food())

    def test_growth(self):
        g = game.Game.__new__(game.Game)
        g.start_game("1")
        x, y = g.snake[0]
        g.food = (x + 1, y)
        g.next_direction = (1, 0)
        g.move()
        self.assertEqual(g.score, 1)
        self.assertEqual(len(g.snake), 2)
        self.assertEqual(set(g.snake), g.occupied)
