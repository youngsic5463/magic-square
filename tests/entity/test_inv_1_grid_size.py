"""INV-1: 마방진의 크기는 4×4이다."""

import pytest

from src.square import GRID_SIZE, validate_grid

pytestmark = pytest.mark.entity


def test_inv_1_01_grid_size_constant_is_four():
    """INV-1: GRID_SIZE 상수는 4이다."""
    assert GRID_SIZE == 4


def test_inv_1_02_validate_grid_accepts_four_by_four():
    """INV-1: 4×4 격자는 validate_grid를 통과한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 0, 12],
        [4, 14, 15, 0],
    ]

    validate_grid(grid)


def test_inv_1_03_validate_grid_rejects_non_four_by_four():
    """INV-1: 4×4가 아닌 격자는 validate_grid가 거부한다."""
    grid = [[1, 2, 3], [4, 5, 6]]

    with pytest.raises(ValueError):
        validate_grid(grid)
