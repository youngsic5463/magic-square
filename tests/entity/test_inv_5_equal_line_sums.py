"""INV-5: 완성 상태에서 모든 직선·대각선의 합이 동일해야 한다."""

import pytest

from src.square import is_magic_square

pytestmark = pytest.mark.entity


def test_inv_5_01_complete_magic_square_has_equal_line_sums(complete_magic):
    """INV-5: 완성 마방진은 is_magic_square가 True이다."""
    assert is_magic_square(complete_magic) is True


def test_inv_5_02_non_magic_grid_has_unequal_line_sums():
    """INV-5: 완성되었으나 합이 다른 격자는 is_magic_square가 False이다."""
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    assert is_magic_square(grid) is False
