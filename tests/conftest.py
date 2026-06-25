"""공통 테스트 픽스처."""

import pytest

COMPLETE_MAGIC = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

PARTIAL_PUZZLE = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]


@pytest.fixture
def complete_magic():
    return [row[:] for row in COMPLETE_MAGIC]


@pytest.fixture
def partial_puzzle():
    return [row[:] for row in PARTIAL_PUZZLE]
