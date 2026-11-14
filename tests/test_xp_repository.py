import unittest

from level import XpRepository
from tests._database import set_up_database

class XpRepositoryTests(unittest.TestCase):
    USER_ID = 123456789012345678

    def setUp(self) -> None:
        super().setUp()
        set_up_database(self)

    def test_unknown_user_has_zero_xp(self) -> None:
        self.assertEqual(XpRepository.get_user_xp(self.USER_ID), 0)

    def test_awards_accumulate_and_survive_table_initialization(self) -> None:
        self.assertEqual(XpRepository.add_xp(self.USER_ID, 10), 10)
        self.assertEqual(XpRepository.add_xp(self.USER_ID, 10), 20)

        XpRepository.create()

        self.assertEqual(XpRepository.get_user_xp(self.USER_ID), 20)

    def test_users_have_independent_xp(self) -> None:
        other_user_id = self.USER_ID + 1
        XpRepository.add_xp(self.USER_ID, 10)
        XpRepository.add_xp(other_user_id, 70)
        XpRepository.add_xp(self.USER_ID, 20)

        self.assertEqual(XpRepository.get_user_xp(self.USER_ID), 30)
        self.assertEqual(XpRepository.get_user_xp(other_user_id), 70)
