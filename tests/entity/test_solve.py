"""solve: 2개 빈칸을 채워 마방진을 완성한다."""

import pytest

from src.square import solve

pytestmark = pytest.mark.entity


def test_solve_01_partial_puzzle_returns_one_indexed_coordinates(partial_puzzle):
    """INV-6: solve는 2개 빈칸 좌표와 숫자를 1-index로 반환한다."""
    assert solve(partial_puzzle) == [3, 3, 1, 4, 4, 6]
