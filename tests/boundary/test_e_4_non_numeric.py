"""E-4: 숫자가 아닌 값은 칸에 입력할 수 없다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.boundary


def test_e_4_01_validate_grid_rejects_non_numeric_cell():
    """E-4: 숫자가 아닌 값이 포함된 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, "x", 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises((TypeError, ValueError)):
        validate_grid(grid)
