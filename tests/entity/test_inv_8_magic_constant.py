"""INV-8: 모든 직선·대각선의 목표 합은 34이다."""

import pytest

from src.square import MAGIC_CONSTANT, line_sums

pytestmark = pytest.mark.entity


def test_inv_8_01_magic_constant_is_thirty_four():
    """INV-8: MAGIC_CONSTANT 상수는 34이다."""
    assert MAGIC_CONSTANT == 34


def test_inv_8_02_all_line_sums_equal_magic_constant(complete_magic):
    """INV-8: 완성 마방진의 모든 직선·대각선 합은 MAGIC_CONSTANT와 같다."""
    sums = line_sums(complete_magic)
    all_sums = sums["rows"] + sums["cols"] + sums["diagonals"]

    assert all(value == MAGIC_CONSTANT for value in all_sums)
