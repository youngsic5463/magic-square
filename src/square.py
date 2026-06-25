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
    empty_cells: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if is_empty(cell):  # INV-2
                empty_cells.append((row_index, col_index))

    candidates = unused_numbers(grid)  # INV-2, E-2
    r1, c1 = empty_cells[0]
    r2, c2 = empty_cells[1]
    return [r1 + 1, c1 + 1, candidates[0], r2 + 1, c2 + 1, candidates[1]]  # INV-6


def validate_grid(grid: list[list[int]]) -> None:
    """도메인 진입 시 격자 입력을 검증한다."""
    if len(grid) != GRID_SIZE:  # INV-1
        raise ValueError("grid must be 4x4")

    seen: set[int] = set()
    empty_count = 0

    for row_index, row in enumerate(grid):
        if len(row) != GRID_SIZE:  # INV-1
            raise ValueError(f"row {row_index + 1} must have length {GRID_SIZE}")
        for col_index, cell in enumerate(row):
            if not isinstance(cell, int):  # E-4
                raise TypeError(f"non-numeric cell at ({row_index + 1},{col_index + 1})")
            if is_empty(cell):  # INV-2
                empty_count += 1
                if empty_count > 2:  # E-6
                    raise ValueError(f"empty value at ({row_index + 1},{col_index + 1})")
            elif cell < 1 or cell > 16:  # INV-7, E-5
                raise ValueError(f"out of range at ({row_index + 1},{col_index + 1})")
            elif cell in seen:  # INV-4, E-1
                raise ValueError(f"duplicate {cell} at ({row_index + 1},{col_index + 1})")
            else:
                seen.add(cell)


def is_empty(value: int) -> bool:
    """INV-2: 빈 칸(0)과 배치된 숫자를 구분한다."""
    return value == EMPTY  # INV-2


def unused_numbers(grid: list[list[int]]) -> list[int]:
    """INV-2, E-2: 격자에 없는 사용 가능 숫자(1~16) 목록."""
    placed: set[int] = set()
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if not is_empty(cell):  # INV-2, E-2
                if cell in placed:  # E-2
                    raise ValueError(
                        f"already placed {cell} at ({row_index + 1},{col_index + 1})"
                    )
                placed.add(cell)
    return [number for number in range(1, 17) if number not in placed]  # INV-2, E-2


def line_sums(grid: list[list[int]]) -> dict[str, list[int]]:
    """INV-3: 가로·세로·대각선 각각의 합을 산출한다."""
    rows = [sum(row) for row in grid]  # INV-3
    cols = [sum(grid[row_index][col_index] for row_index in range(GRID_SIZE)) for col_index in range(GRID_SIZE)]  # INV-3
    diagonals = [
        sum(grid[index][index] for index in range(GRID_SIZE)),  # INV-3
        sum(grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)),  # INV-3
    ]
    return {"rows": rows, "cols": cols, "diagonals": diagonals}  # INV-3


def is_magic_square(grid: list[list[int]]) -> bool:
    """INV-5, INV-6, E-3: 완성 상태에서 직선·대각선 합 동일 및 마방진 조건 충족 여부."""
    for row in grid:
        for cell in row:
            if is_empty(cell):  # INV-6
                return False

    sums = line_sums(grid)  # INV-5, INV-8
    all_sums = sums["rows"] + sums["cols"] + sums["diagonals"]  # INV-5
    return all(value == MAGIC_CONSTANT for value in all_sums)  # INV-5, INV-8, E-3
