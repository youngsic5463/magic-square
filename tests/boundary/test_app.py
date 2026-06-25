"""UC-1, UC-2, UE-1: Flask 마방진 폼 계약."""

import pytest

from src.app import app

pytestmark = pytest.mark.boundary


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_uc_1_get_root_returns_4x4_grid_with_two_inputs(client):
    """UC-1: GET / → 200, 본문에 4×4 마방진을 그려주고 2개의 입력란 표시."""
    response = client.get("/")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "16" in body
    assert "11" in body
    assert 'name="r3c3"' in body
    assert 'name="r4c4"' in body


def test_uc_2_post_calc_shows_correct_when_answer_is_right(client):
    """UC-2: POST /calc → 본문에 정답 여부를 결과 표시 (정답)."""
    response = client.post(
        "/calc",
        data={"r3c3": 6, "r4c4": 1},
    )

    assert response.status_code == 200
    assert "정답" in response.get_data(as_text=True)


def test_ue_1_non_numeric_input_returns_400(client):
    """UE-1: 입력 값이 숫자가 아니면 400 + 에러 메시지."""
    response = client.post(
        "/calc",
        data={"r3c3": "abc", "r4c4": 6},
    )

    assert response.status_code == 400
    assert response.get_data(as_text=True)


def test_ue_1_out_of_range_input_returns_400(client):
    """UE-1: 입력 값이 1~16 범위 밖이면 400 + 에러 메시지."""
    response = client.post(
        "/calc",
        data={"r3c3": 0, "r4c4": 6},
    )

    assert response.status_code == 400
    assert response.get_data(as_text=True)
