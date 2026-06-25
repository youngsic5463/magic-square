"""INV-3: 가로·세로·대각선 각각의 합을 산출·표시할 수 있어야 한다."""

import pytest

from src.square import line_sums

pytestmark = pytest.mark.entity


def test_inv_3_01_line_sums_returns_row_col_and_diagonal_sums(complete_magic):
    """INV-3: line_sums는 행·열·대각선 합을 산출한다."""
    sums = line_sums(complete_magic)

    assert sums["rows"] == [34, 34, 34, 34]
    assert sums["cols"] == [34, 34, 34, 34]
    assert sums["diagonals"] == [34, 34]
