# MagicSquare PRD — 제품 요구사항 문서

| 항목 | 내용 |
|------|------|
| 제품명 | MagicSquare — 4×4 마방진 솔루션 |
| 문서 버전 | 1.0 |
| 작성일 | 2026-06-25 |
| 근거 자료 | [MomTest 인터뷰](../Prompting/01.Export-Transcript.md), [Discovery 보고서](../Report/01.REPORT.md) |
| 구현 저장소 | `src/square.py` (Entity), `src/app.py` (Boundary) |

---

## 1. 제품 개요

4×4 마방진을 풀 때 발생하는 **계산 실수·중복 입력·합 검산 반복·정답 확인 생략** 등의 문제를 줄이는 웹 기반 마방진 연습 도구이다.

MomTest 인터뷰 9건에서 도출한 **불변식(INV)**, **에러 조건(E)**, **수용 조건(AC)** 을 계약 ID로 고정하고, Dual-Track TDD로 구현·검증한다.

### 1.1 계약 유형 정의

| 유형 | ID 접두사 | 의미 | 검증 위치 |
|------|-----------|------|-----------|
| **Invariant** | `INV-*` | 어떤 입력·상태에서도 깨지면 안 되는 도메인 규칙 | `tests/entity/`, `src/square.py` |
| **Error** | `E-*` | 반드시 차단·거부해야 하는 잘못된 입력·상태 | `tests/boundary/`, `validate_grid()` |
| **Acceptance Criteria** | `AC-*` | 사용자가 “이렇게 동작하면 된다”고 받아들이는 조건 | UI·HTTP·MVP 기능 |
| **Use Case** | `UC-*` | Boundary 정상 흐름 (HTTP) | `tests/boundary/test_app.py` |
| **User Error** | `UE-*` | Boundary 오류 응답 (HTTP) | `tests/boundary/test_app.py` |

> **AC**는 MVP 기능 수용 조건(`AC-1`~`AC-7`)과 Boundary 수용 조건(`UC-*`, `UE-*`)으로 구분한다.

### 1.2 Evidence Level · Product Layer

| Evidence Level | 설명 |
|----------------|------|
| **L0** | 인터뷰에서 직접 언급·반복된 사실 |
| **L1** | 관찰된 행동·실수 패턴에서 직접 추론 |
| **L2** | 도메인 지식·맥락 기반 추론 (추가 검증 권장) |

| Product Layer | 설명 |
|---------------|------|
| **Core** | 마방진 풀이의 본질 규칙 |
| **Trust** | 정답·오답·숫자 집합에 대한 신뢰 |
| **Safety** | 잘못된 입력·상태 손실 방지 |

---

## 2. 불변식 (INV)

도메인(Entity)에서 **항상** 만족해야 하는 규칙이다.

| ID | 계약 | Evidence | Layer | 구현·검증 |
|----|------|----------|-------|-----------|
| **INV-1** | 마방진의 크기는 **4×4**이다 | L0 — “4×4 마방진” 반복 (#1, #9) | Core | `GRID_SIZE`, `validate_grid()` · `test_inv_1_grid_size.py` |
| **INV-2** | 격자에서 **사용되지 않은 숫자**와 **이미 배치된 숫자**·**빈 칸**을 구분할 수 있다 | L0 — “사용되지 않은 숫자가 뭔지 몰라” (#2) | Core | `EMPTY`, `is_empty()`, `unused_numbers()` · `test_inv_2_empty_and_unused.py` |
| **INV-3** | **가로·세로·대각선** 각각의 합을 산출·표시할 수 있다 | L1 — “직선, 대각선을 모두 … 계산” (#3) | Core | `line_sums()` · `test_inv_3_line_sums.py` |
| **INV-4** | 각 숫자는 격자 전체에서 **최대 1회**만 배치된다 | L1 — 중복 입력 시 오답 (#2) | Core | `validate_grid()` · `test_inv_4_no_duplicates.py` |
| **INV-5** | 완성 상태에서 **모든 직선·대각선의 합이 동일**해야 한다 | L1 — 직선·대각선 합 반복 검산 (#3) | Core | `is_magic_square()` · `test_inv_5_equal_line_sums.py` |
| **INV-6** | 마방진 조건 **충족 여부를 검증**할 수 있다 | L1 — 장시간 풀이 후 확인 생략 (#7) | Trust | `is_magic_square()`, `solve()` · `test_inv_6_magic_validation.py` |
| **INV-7** | 사용 가능한 숫자는 **1~16 정수**이며 각각 **1회**만 쓰인다 | L2 — 4×4 + 미사용/중복 맥락 | Core | `validate_grid()` · `test_inv_7_number_set.py` |
| **INV-8** | 모든 직선·대각선의 목표 합은 **34**이다 | L2 — 표준 magic constant | Core | `MAGIC_CONSTANT`, `is_magic_square()` · `test_inv_8_magic_constant.py` |

### INV 상세 설명

- **INV-1** — 격자는 항상 4행 4열이다. 행·열 길이가 다르면 유효하지 않다.
- **INV-2** — 빈 칸은 `0`(EMPTY)으로 표식한다. 미사용 숫자 목록은 1~16 중 격자에 없는 값만 포함한다.
- **INV-3** — 행 4개, 열 4개, 대각선 2개의 합을 각각 계산할 수 있어야 한다.
- **INV-4** — 동일 숫자가 두 칸 이상에 있으면 유효한 마방진 상태가 아니다.
- **INV-5** — 완성 격자에서 10개 직선(행·열·대각)의 합이 모두 같아야 한다.
- **INV-6** — 빈 칸이 남아 있거나 합이 맞지 않으면 마방진이 아니다.
- **INV-7** — 완성 시 1부터 16까지가 정확히 한 번씩 등장한다.
- **INV-8** — 4×4 마방진의 magic constant는 34이다.

---

## 3. 에러 조건 (E)

잘못된 입력·상태는 **거부**해야 한다. Entity는 `validate_grid()`로, Boundary는 HTTP 검증으로 대응한다.

| ID | 계약 | Evidence | Layer | 구현·검증 |
|----|------|----------|-------|-----------|
| **E-1** | **같은 숫자를 중복** 입력·배치할 수 없다 | L0 — “같은 숫자를 중복으로 채워넣어서 오답” (#2) | Trust | `validate_grid()` · `test_e_1_no_duplicate.py` |
| **E-2** | 이미 배치된 숫자를 **미사용 숫자 목록에 표시하지 않는다** | L1 — 미사용 숫자 혼동 (#2) | Trust | `unused_numbers()` · `test_e_2_unused_excludes_placed.py`, `app.py` 패널 |
| **E-3** | 마방진 조건을 만족하지 않는 상태를 **정답으로 표시하지 않는다** | L1 — 오답·검증 생략 (#2, #7) | Trust | `is_magic_square()` · `test_e_3_no_false_positive.py`, `POST /calc` |
| **E-4** | **숫자가 아닌 값**은 칸에 입력할 수 없다 | L2 — 계산·숫자 입력 전제 (#1, #6) | Safety | `validate_grid()` · `test_e_4_non_numeric.py` |
| **E-5** | **1~16 범위 밖** 숫자는 입력할 수 없다 | L2 — 미사용 숫자 관리 전제 (#2) | Trust | `validate_grid()` · `test_e_5_out_of_range.py` |
| **E-6** | 빈 칸이 아닌 칸에 **빈 값(0)으로 덮어쓰기** 할 수 없다 | L2 — 재시작·상태 보존 (#1) | Safety | `validate_grid()` · `test_e_6_no_overwrite_empty.py` |

### E ↔ Boundary 매핑

| E | Boundary 대응 |
|---|----------------|
| E-4, E-5 | **UE-1** — `POST /calc` 시 비숫자·범위 밖 → `400` + 메시지 |
| E-3 | **UC-2** — `is_magic_square()` 실패 시 `"오답"` |
| E-2 | **UC-1** — 오른쪽 “채울 숫자” 패널 |

---

## 4. 수용 조건 (AC)

### 4.1 MVP 수용 조건 (AC-1 ~ AC-7)

MomTest에서 L0~L1 근거로 확정된 **MVP 기능**이다. 사용자가 제품을 “쓸 만하다”고 판단하는 기준이다.

| ID | 수용 조건 | 충족 INV/E | 인터뷰 근거 | 구현 상태 |
|----|-----------|------------|-------------|-----------|
| **AC-1** | **4×4 격자 UI**로 문제를 제시한다 | INV-1 | #1, #9 | ✅ `GET /` — 4×4 그리드 |
| **AC-2** | **미사용(채울) 숫자 목록**을 실시간 표시한다 | INV-2, E-2 | #2, #4 | ✅ 격자 오른쪽 패널 |
| **AC-3** | **중복 입력을 차단**한다 | INV-4, E-1 | #2 | ✅ Entity `validate_grid()` |
| **AC-4** | **가로·세로·대각선 합**을 자동 계산·표시한다 | INV-3 | #3, #4 | ⬜ 미구현 (Entity만 존재) |
| **AC-5** | 합이 맞는 **라인을 시각 강조**한다 | INV-3 | #4 | ⬜ 미구현 |
| **AC-6** | **원클릭 정답 검증**을 제공한다 | INV-6, E-3 | #7 | ✅ `POST /calc` |
| **AC-7** | 조건 미충족 시 **오답을 명시**한다 | INV-5, E-3 | #2, #7 | ✅ `"오답"` 응답 |

### 4.2 Boundary 수용 조건 (UC / UE)

Flask 마방진 폼(Discovery 4.1)의 HTTP 계약이다. AC의 일부로 Track A에서 검증한다.

| ID | 유형 | 계약 | HTTP | 구현 상태 |
|----|------|------|------|-----------|
| **UC-1** | Use Case | `GET /` → `200`, 본문에 4×4 마방진과 **빈 칸 2개 입력란** 표시 | `GET /` | ✅ |
| **UC-2** | Use Case | `POST /calc` → 본문에 **정답 여부** 표시 (`정답` / `오답`) | `POST /calc` | ✅ `is_magic_square()` |
| **UE-1** | User Error | 입력이 숫자가 아니거나 **1~16 범위 밖**이면 `400` + 에러 메시지 | `POST /calc` | ✅ |

#### UC-1 상세

- 4×4 정사각형 셀로 숫자 배치
- 빈 칸 2곳은 초기값 **0** 표시 + 입력 가능
- 매 페이지 로드 시 숫자 배치·빈 칸 위치 **무작위** (테스트 모드 제외)
- 폼 `action="/calc"`, `method="post"`

#### UC-2 상세

- 사용자가 채운 격자에 대해 `is_magic_square()`로 판정
- 모든 행·열·대각선 합이 34이면 `"정답"`, 아니면 `"오답"`

#### UE-1 상세

- 빈 칸 필드(`r{row}c{col}`) 값 검증
- 비숫자 또는 1 미만·16 초과 → HTTP `400`, 본문에 오류 메시지

---

## 5. 계약 추적 매트릭스

| 계약 ID | Entity (`square.py`) | Boundary (`app.py`) | 테스트 |
|---------|----------------------|---------------------|--------|
| INV-1 | `GRID_SIZE`, `validate_grid` | 4×4 렌더 | `test_inv_1_*` |
| INV-2 | `EMPTY`, `is_empty`, `unused_numbers` | 빈 칸 0, 채울 숫자 패널 | `test_inv_2_*` |
| INV-3 | `line_sums` | — | `test_inv_3_*` |
| INV-4 | `validate_grid` | — | `test_inv_4_*` |
| INV-5 | `is_magic_square` | — | `test_inv_5_*` |
| INV-6 | `is_magic_square`, `solve` | `POST /calc` | `test_inv_6_*`, `test_solve` |
| INV-7 | `validate_grid` | `min`/`max`, UE-1 | `test_inv_7_*` |
| INV-8 | `MAGIC_CONSTANT`, `is_magic_square` | 안내 문구 “합 34” | `test_inv_8_*` |
| E-1 | `validate_grid` | — | `test_e_1_*` |
| E-2 | `unused_numbers` | `_render_unused_numbers` | `test_e_2_*` |
| E-3 | `is_magic_square` | `calc()` | `test_e_3_*`, `test_uc_2_*` |
| E-4 | `validate_grid` | UE-1 | `test_e_4_*` |
| E-5 | `validate_grid` | UE-1 | `test_e_5_*` |
| E-6 | `validate_grid` | — | `test_e_6_*` |
| UC-1 | — | `index()` | `test_uc_1_*` |
| UC-2 | `is_magic_square` | `calc()` | `test_uc_2_*` |
| UE-1 | — | `_parse_cell_value` | `test_ue_1_*` |

---

## 6. 범위 외 (보류 기능)

아래는 MomTest에서 **L2·가설**이거나 행동 증거가 부족해 **AC에 포함하지 않는다**.

| 기능 | 보류 사유 |
|------|-----------|
| 완전 자동 풀이 | #8 미래 가설, 과거 행동 아님 |
| 결제·인센티브 | 가설 기반 |
| 스트레스·웰니스 트래킹 | #9 결과 서술만 |
| 일일 챌린지·게이미피케이션 | 습관 ≠ 제품 요구 |
| 소셜·친구 초대 | 연동 니즈 미확인 |
| 엑셀 연동 | 사용은 있으나 연동 요구 없음 |
| 내장 계산기 | INV-3 자동 합산으로 대체 가능 |
| 힌트·단계 가이드 | 직접 요청 없음 |
| 5×5 이상 | 인터뷰 4×4 한정 |
| 풀이 이력·세션 복원 | L2 추론 |
| 목표 합 34 고정 UI | INV-8 L2 (현재는 안내 문구만) |

---

## 7. 아키텍처 (ECB)

```text
┌─────────────────────────────────────┐
│  Boundary — src/app.py (Flask)      │
│  UC-*, UE-*, E-4/E-5 HTTP 검증      │
│  AC-1, AC-2, AC-6, AC-7 UI          │
└──────────────┬──────────────────────┘
               │ import (단방향)
┌──────────────▼──────────────────────┐
│  Entity — src/square.py             │
│  INV-*, E-* 도메인 로직             │
│  Flask import 금지                  │
└─────────────────────────────────────┘
```

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2026-06-25 | MomTest Discovery 기반 INV/E/AC 초안 정리 |

---

*본 문서는 `README.md`, `Report/01.REPORT.md`, `Prompting/01.Export-Transcript.md` 및 현재 코드베이스를 기준으로 작성되었다.*
