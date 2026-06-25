"""INV-7: 사용 가능한 숫자는 1~16의 정수이며 각각 1회만 쓰인다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.entity


def test_inv_7_01_complete_magic_square_uses_one_through_sixteen_once(complete_magic):
    """INV-7: 완성 마방진은 1~16을 각각 정확히 1회 사용한다."""
    placed = sorted(cell for row in complete_magic for cell in row)

    assert placed == list(range(1, 17))


def test_inv_7_02_validate_grid_rejects_out_of_range_number():
    """INV-7: 1~16 범위 밖 숫자가 있는 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 17, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)
