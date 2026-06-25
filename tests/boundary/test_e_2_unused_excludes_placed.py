"""E-2: 이미 배치된 숫자를 미사용 숫자 목록에 표시하지 않는다."""

import pytest

from src.square import unused_numbers

pytestmark = pytest.mark.boundary


def test_e_2_01_unused_numbers_excludes_already_placed_values(partial_puzzle):
    """E-2: unused_numbers는 이미 배치된 숫자를 포함하지 않는다."""
    unused = unused_numbers(partial_puzzle)
    placed = {16, 2, 3, 13, 5, 11, 10, 8, 9, 7, 12, 4, 14, 15}

    assert placed.isdisjoint(unused)
