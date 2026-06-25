"""INV-2: 격자에는 사용되지 않은 숫자와 이미 배치된 숫자가 구분 가능해야 한다."""

import pytest

from src.square import EMPTY, is_empty, unused_numbers

pytestmark = pytest.mark.entity


def test_inv_2_01_empty_constant_is_zero():
    """INV-2: 빈 칸 표식 EMPTY는 0이다."""
    assert EMPTY == 0


def test_inv_2_02_is_empty_distinguishes_zero_from_placed_number():
    """INV-2: is_empty(0)은 True, 배치된 숫자는 False이다."""
    assert is_empty(0) is True
    assert is_empty(7) is False


def test_inv_2_03_unused_numbers_lists_only_not_yet_placed(partial_puzzle):
    """INV-2: unused_numbers는 격자에 없는 1~16 숫자만 반환한다."""
    assert unused_numbers(partial_puzzle) == [1, 6]
