from contextlib import chdir
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from level import XpRepository


def set_up_database(test_case: TestCase) -> None:
    temporary_directory = test_case.enterContext(
        TemporaryDirectory(prefix="yuruneko-tests-")
    )
    test_case.enterContext(chdir(temporary_directory))
    Path("database").mkdir()
    XpRepository.create()
