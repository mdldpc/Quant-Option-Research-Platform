import pytest
from fastapi.testclient import TestClient

from api.main import app

BASE = dict(spot=100, strike=100, maturity=1, rate=0.05, volatility=0.2, option_type="call")
CALL = dict(delta=0.6368306511756191, gamma=0.018762017345846895, vega=37.52403469169379)
PUT = {**CALL, "delta": -0.3631693488243809}


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("kind, expected", [("call", CALL), ("put", PUT)])
def test_greeks_reference_values(client, kind, expected):
    response = client.post("/risk/greeks", json={**BASE, "option_type": kind})
    assert response.status_code == 200
    assert response.json() == pytest.approx(expected, rel=1e-10)


@pytest.mark.parametrize("field", ["spot", "strike", "maturity", "volatility"])
@pytest.mark.parametrize("value", [0, -1, None, "invalid", "NaN", "Infinity", True])
@pytest.mark.parametrize("endpoint", ["greeks", "portfolio"])
def test_invalid_positive_inputs(client, field, value, endpoint):
    payload = {**BASE, field: value}
    if endpoint == "portfolio":
        payload = [{**payload, "quantity": 1}]
    assert client.post(f"/risk/{endpoint}", json=payload).status_code == 422


@pytest.mark.parametrize("kind", ["CALL", "C", "invalid", None])
def test_invalid_option_type(client, kind):
    assert client.post("/risk/greeks", json={**BASE, "option_type": kind}).status_code == 422


@pytest.mark.parametrize("field", list(BASE))
def test_missing_fields(client, field):
    payload = {key: value for key, value in BASE.items() if key != field}
    assert client.post("/risk/greeks", json=payload).status_code == 422


@pytest.mark.parametrize("field", ["rate", "quantity"])
@pytest.mark.parametrize("value", ["NaN", "Infinity", None, True])
def test_invalid_portfolio_numbers(client, field, value):
    payload = [{**BASE, "quantity": 1, field: value}]
    assert client.post("/risk/portfolio", json=payload).status_code == 422


def test_portfolio_aggregation(client):
    positions = [
        {**BASE, "quantity": 2},
        {**BASE, "option_type": "put", "quantity": -3},
    ]
    response = client.post("/risk/portfolio", json=positions)
    assert response.status_code == 200
    assert response.json() == pytest.approx({key: 2 * CALL[key] - 3 * PUT[key] for key in CALL})


@pytest.mark.parametrize("quantities", [[], [0], [2, -2]])
def test_zero_portfolio(client, quantities):
    response = client.post("/risk/portfolio", json=[{**BASE, "quantity": q} for q in quantities])
    assert response.status_code == 200
    assert response.json() == dict(delta=0, gamma=0, vega=0)


def test_negative_rate(client):
    response = client.post("/risk/greeks", json={**BASE, "rate": -0.02})
    assert response.status_code == 200
    assert response.json()["delta"] == pytest.approx(0.5)


def test_numerical_overflow(client):
    response = client.post("/risk/greeks", json={**BASE, "volatility": 1e308})
    assert response.status_code == 422


def test_portfolio_requires_array(client):
    assert client.post("/risk/portfolio", json={"positions": []}).status_code == 422
