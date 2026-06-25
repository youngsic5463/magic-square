"""Boundary — Flask 마방진 폼 (Discovery 4.1).

계약:
- UC-1: GET / → 200, 본문에 4×4 마방진을 그려주고 2개의 입력란 표시
- UC-2: POST /calc → 본문에 정답 여부를 결과 표시
- UE-1: 입력 값이 숫자가 아니거나 1에서 16 사이가 아니면 400 + 에러 메시지

ECB 역할:
- Boundary: HTTP 입력·검증·응답만 담당한다.
- Entity: ``src.square`` (Flask import 금지) — 마방진 계산을 재사용한다.
"""

import random

from flask import Flask, request, session

from src.square import EMPTY, MAGIC_CONSTANT, is_magic_square, unused_numbers

app = Flask(__name__)
app.secret_key = "magic-square-session"

# 테스트·폴백용 고정 퍼즐
DEFAULT_PUZZLE = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]
DEFAULT_INPUT_CELLS = [(3, 3), (4, 4)]

COMPLETE_MAGIC = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def _random_magic(base: list[list[int]]) -> list[list[int]]:
    grid = [row[:] for row in base]
    for _ in range(random.randint(0, 3)):
        grid = [list(row) for row in zip(*grid[::-1])]
    if random.random() < 0.5:
        grid = grid[::-1]
    return grid


def _create_puzzle() -> tuple[list[list[int]], list[tuple[int, int]]]:
    if app.config.get("TESTING"):
        return [row[:] for row in DEFAULT_PUZZLE], list(DEFAULT_INPUT_CELLS)

    magic = _random_magic(COMPLETE_MAGIC)
    positions = random.sample(range(16), 2)
    puzzle = [row[:] for row in magic]
    input_cells: list[tuple[int, int]] = []
    for position in positions:
        row_index, col_index = divmod(position, 4)
        puzzle[row_index][col_index] = EMPTY  # INV-2
        input_cells.append((row_index + 1, col_index + 1))
    return puzzle, input_cells


def _puzzle_state() -> tuple[list[list[int]], list[tuple[int, int]]]:
    puzzle = session.get("puzzle")
    input_cells = session.get("input_cells")
    if puzzle is not None and input_cells is not None:
        return puzzle, input_cells
    return [row[:] for row in DEFAULT_PUZZLE], list(DEFAULT_INPUT_CELLS)


def _parse_cell_value(field_name: str) -> int:
    raw = request.form.get(field_name, "")
    if not raw.isdigit():  # UE-1
        raise ValueError(f"{field_name} must be a number")
    value = int(raw)
    if value < 1 or value > 16:  # UE-1
        raise ValueError(f"{field_name} must be between 1 and 16")
    return value


def _build_grid() -> list[list[int]]:
    puzzle, input_cells = _puzzle_state()
    grid = [row[:] for row in puzzle]
    for row_index, col_index in input_cells:
        grid[row_index - 1][col_index - 1] = _parse_cell_value(
            f"r{row_index}c{col_index}"
        )  # UE-1
    return grid


def _render_cell(
    row_index: int, col_index: int, value: int, input_cells: list[tuple[int, int]]
) -> str:
    if (row_index, col_index) in input_cells:
        return (
            f'<input class="cell-input" name="r{row_index}c{col_index}" '
            f'type="number" min="1" max="16" value="{value}">'  # INV-2: 빈 칸은 0 표시
        )
    return f'<span class="cell-value">{value}</span>'


def _render_grid(puzzle: list[list[int]], input_cells: list[tuple[int, int]]) -> str:
    cells = []
    for row_index, row in enumerate(puzzle, start=1):
        for col_index, cell in enumerate(row, start=1):
            cells.append(
                f'<div class="cell">{_render_cell(row_index, col_index, cell, input_cells)}</div>'
            )
    return "".join(cells)


def _render_unused_numbers(puzzle: list[list[int]]) -> str:
    numbers = unused_numbers(puzzle)  # INV-2, E-2
    items = "".join(f'<div class="unused-number">{number}</div>' for number in numbers)
    return f"""<aside class="unused-panel">
      <h2>채울 숫자</h2>
      <p class="unused-hint">아래 2개를 빈 칸에 넣으세요.</p>
      {items}
    </aside>"""


@app.get("/")
def index():
    puzzle, input_cells = _create_puzzle()
    session["puzzle"] = puzzle
    session["input_cells"] = input_cells

    # UC-1: GET / → 200, 본문에 4×4 마방진을 그려주고 2개의 입력란 표시
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>4×4 마방진</title>
  <style>
    body {{ font-family: sans-serif; margin: 2rem; }}
    h1 {{ margin-bottom: 0.25rem; }}
    p {{ color: #444; margin-top: 0; }}
    .puzzle-layout {{
      display: flex;
      align-items: flex-start;
      gap: 1.5rem;
      margin-top: 1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, 4rem);
      grid-template-rows: repeat(4, 4rem);
      gap: 4px;
      margin-top: 1rem;
    }}
    .unused-panel {{
      min-width: 6rem;
      padding: 0.75rem 1rem;
      border: 2px solid #333;
      border-radius: 8px;
      background: #f5f5f5;
    }}
    .unused-panel h2 {{
      font-size: 1rem;
      margin: 0 0 0.25rem;
    }}
    .unused-hint {{
      font-size: 0.85rem;
      margin: 0 0 0.75rem;
      color: #555;
    }}
    .unused-number {{
      width: 3rem;
      height: 3rem;
      margin-bottom: 0.5rem;
      border: 2px solid #333;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      font-weight: 600;
      background: #fff;
    }}
    .cell {{
      width: 4rem;
      height: 4rem;
      border: 2px solid #333;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #fafafa;
      box-sizing: border-box;
    }}
    .cell-value {{
      font-size: 1.25rem;
      font-weight: 600;
    }}
    .cell-input {{
      width: 3rem;
      height: 3rem;
      text-align: center;
      font-size: 1.25rem;
      border: 1px solid #888;
      border-radius: 4px;
    }}
    button {{
      margin-top: 1rem;
      padding: 0.5rem 1.25rem;
      font-size: 1rem;
    }}
  </style>
</head>
<body>
  <h1>4×4 마방진</h1>
  <p>1~16 숫자를 한 번씩 배치하고, 가로·세로·대각선의 합이 모두 {MAGIC_CONSTANT}이 되도록 빈 칸을 채우세요.</p>
  <form action="/calc" method="post">
    <div class="puzzle-layout">
      <div class="grid">
        {_render_grid(puzzle, input_cells)}
      </div>
      {_render_unused_numbers(puzzle)}
    </div>
    <button type="submit">확인</button>
  </form>
</body>
</html>"""


@app.post("/calc")
def calc():
    try:
        grid = _build_grid()
    except ValueError as error:
        return str(error), 400  # UE-1

    if is_magic_square(grid):  # UC-2, INV-5, INV-8
        return "정답"
    return "오답"  # UC-2
