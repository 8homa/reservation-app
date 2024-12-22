import json
import pytest
from app import app, reservations

@pytest.fixture
def client():
    return app.test_client()

def test_reserve(client):
    # 事前に初期化
    client.get("/init")
    assert len(reservations) == 0

    payload = {"user_id": 1, "date": "2024-12-25", "time": "10:00"}
    res = client.post("/reserve", json=payload)
    assert res.status_code == 201

    # reservationsリストに1件追加されたか？
    assert len(reservations) == 1

def test_duplicate_reserve(client):
    # 事前に初期化
    client.get("/init")
    # 1件登録
    payload = {"user_id": 1, "date": "2024-12-25", "time": "10:00"}
    client.post("/reserve", json=payload)
    assert len(reservations) == 1

    # 重複予約 → 409エラー
    res = client.post("/reserve", json=payload)
    assert res.status_code == 409

def test_get_reservations(client):
    # 事前に初期化
    client.get("/init")

    # 2件登録してみる
    payload1 = {"user_id": 1, "date": "2024-12-25", "time": "10:00"}
    payload2 = {"user_id": 2, "date": "2024-12-26", "time": "14:00"}
    client.post("/reserve", json=payload1)
    client.post("/reserve", json=payload2)
    assert len(reservations) == 2

    # GET /reservations
    res = client.get("/reservations")
    data = json.loads(res.data)
    assert res.status_code == 200
    assert len(data) == 2
