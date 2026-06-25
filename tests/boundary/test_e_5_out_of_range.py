"""E-5: 1~16 범위 밖의 숫자는 입력할 수 없다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.boundary


def test_e_5_01_validate_grid_rejects_negative_number():
    """E-5: 1~16 범위 밖(음수) 숫자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, -1, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)


def test_e_5_02_validate_grid_rejects_number_above_sixteen():
    """E-5: 16보다 큰 숫자가 있는 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 20, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)
