"""INV-6: 마방진 조건 충족 여부를 검증할 수 있어야 한다."""

import pytest

from src.square import is_magic_square

pytestmark = pytest.mark.entity


def test_inv_6_01_is_magic_square_validates_complete_grid(complete_magic):
    """INV-6: is_magic_square는 완성 마방진을 True로 검증한다."""
    assert is_magic_square(complete_magic) is True


def test_inv_6_02_is_magic_square_rejects_incomplete_grid(partial_puzzle):
    """INV-6: is_magic_square는 미완성 격자를 False로 검증한다."""
    assert is_magic_square(partial_puzzle) is False
