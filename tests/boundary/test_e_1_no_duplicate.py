"""E-1: 같은 숫자는 중복 입력·배치할 수 없다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.boundary


def test_e_1_01_validate_grid_rejects_duplicate_placement():
    """E-1: 같은 숫자를 중복 배치한 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 2, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)
