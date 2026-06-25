"""Entity — 4×4 마방진 순수 도메인 로직 (RED).

Flask 등 Boundary 계층을 import하지 않는다.
계약 ID는 README.md의 INV-*, E-* 와 tests를 잇는 추적의 못이다.
"""

from __future__ import annotations

# INV-1: 마방진 크기 4×4
GRID_SIZE = 4

# INV-8: 모든 직선·대각선 목표 합
MAGIC_CONSTANT = 34

# INV-2: 빈 칸 표식
EMPTY = 0


def solve(grid: list[list[int]]) -> list[int]:
    """2개 빈칸을 채워 4×4 마방진을 완성한다.

    입력: 4×4 int[][] — 0=빈칸(정확히 2개), 값은 0 또는 1~16, 중복 금지
    출력: [r1, c1, n1, r2, c2, n2] — 좌표 1-index

    예: [[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]] → [3,3,1,4,4,6]
    """
    # TODO INV-6: 완성 격자가 마방진 조건을 만족하는지 검증 가능해야 한다
    raise NotImplementedError


def validate_grid(grid: list[list[int]]) -> None:
    """도메인 진입 시 격자 입력을 검증한다."""
    # TODO INV-1: 4×4 크기 확인
    # TODO INV-4 / E-1: 같은 숫자 중복 배치 금지
    # TODO INV-7 / E-5: 1~16 범위, 각 숫자 1회만
    # TODO E-6: 빈 칸이 아닌 칸에 빈 값(0)으로 덮어쓰기 금지
    raise NotImplementedError


def is_empty(value: int) -> bool:
    """INV-2: 빈 칸(0)과 배치된 숫자를 구분한다."""
    raise NotImplementedError


def unused_numbers(grid: list[list[int]]) -> list[int]:
    """INV-2, E-2: 격자에 없는 사용 가능 숫자(1~16) 목록."""
    raise NotImplementedError


def line_sums(grid: list[list[int]]) -> dict[str, list[int]]:
    """INV-3: 가로·세로·대각선 각각의 합을 산출한다."""
    raise NotImplementedError


def is_magic_square(grid: list[list[int]]) -> bool:
    """INV-5, INV-6, E-3: 완성 상태에서 직선·대각선 합 동일 및 마방진 조건 충족 여부."""
    raise NotImplementedError
