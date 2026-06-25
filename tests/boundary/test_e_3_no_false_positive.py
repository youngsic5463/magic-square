"""E-3: 마방진 조건을 만족하지 않는 상태를 정답으로 표시하지 않는다."""

import pytest

from src.square import is_magic_square

pytestmark = pytest.mark.boundary


def test_e_3_01_is_magic_square_does_not_accept_invalid_grid():
    """E-3: 마방진 조건을 만족하지 않는 격자는 is_magic_square가 False이다."""
    grid = [
        [16, 2, 3, 13],
        [5, 11, 10, 8],
        [9, 7, 1, 12],
        [4, 14, 15, 6],
    ]

    assert is_magic_square(grid) is False
