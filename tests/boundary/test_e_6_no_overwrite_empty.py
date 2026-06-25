"""E-6: 빈 칸이 아닌 칸에 빈 값으로 덮어쓰기 할 수 없다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.boundary


def test_e_6_01_validate_grid_rejects_cleared_filled_cell():
    """E-6: 기존 숫자 칸을 0으로 덮어쓴 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 0, 0, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)
