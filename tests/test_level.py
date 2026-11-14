import unittest

from level import Level

class LevelTests(unittest.TestCase):
    def test_initial_level_and_main_boundaries(self) -> None:
        for xp, expected in (
            (0, 1),
            (99, 1),
            (100, 2),
            (2_999, 4),
            (3_000, 5),
            (14_999, 9),
            (15_000, 10),
        ):
            with self.subTest(xp=xp, expected_level=expected):
                self.assertEqual(Level.calculate_level(xp), expected)
