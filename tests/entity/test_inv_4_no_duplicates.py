"""INV-4: 각 숫자는 격자 전체에서 최대 1회만 배치된다."""

import pytest

from src.square import validate_grid

pytestmark = pytest.mark.entity


def test_inv_4_01_validate_grid_rejects_duplicate_numbers():
    """INV-4: 중복 숫자가 있는 격자는 validate_grid가 거부한다."""
    grid = [
        [16, 16, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 0, 12],
        [4, 14, 15, 0],
    ]

    with pytest.raises(ValueError):
        validate_grid(grid)
