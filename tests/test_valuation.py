import math

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routes.risk import calculate_greeks
from api.schemas import GreeksRequest
from api.valuation import black_scholes_price, crr_price

BASE = dict(spot=100, strike=100, maturity=1, rate=0.05, volatility=0.2, option_type="call")


@pytest.fixture
def client():
    with TestClient(app) as session:
        yield session


@pytest.mark.parametrize("kind,expected", [("call", 10.450583572185565), ("put", 5.573526022256971)])
def test_reference_price(client, kind, expected):
    response = client.post("/valuation/price", json={**BASE, "option_type": kind})
    assert response.status_code == 200
    result = response.json()
    assert result["black_scholes_price"] == pytest.approx(expected, abs=1e-10)
    assert result["binomial_price"] == pytest.approx(expected, abs=0.005)
    assert result["absolute_error"] == pytest.approx(abs(result["binomial_price"] - expected))
    assert result["steps"] == 500


@pytest.mark.parametrize("rate", [-0.02, 0, 0.05])
@pytest.mark.parametrize("spot", [80, 100, 120])
def test_put_call_parity(rate, spot):
    parameters = {**BASE, "rate": rate, "spot": spot}
    for method, extra in [(black_scholes_price, {}), (crr_price, {"steps": 300})]:
        call = method(**parameters, **extra)
        put = method(**{**parameters, "option_type": "put"}, **extra)
        assert call - put == pytest.approx(spot - 100 * math.exp(-rate), abs=1e-9)


@pytest.mark.parametrize("kind", ["call", "put"])
@pytest.mark.parametrize("spot", [80, 100, 120])
def test_tree_convergence(kind, spot):
    parameters = {**BASE, "spot": spot, "option_type": kind}
    benchmark = black_scholes_price(**parameters)
    coarse = abs(crr_price(**parameters, steps=25) - benchmark)
    fine = abs(crr_price(**parameters, steps=1000) - benchmark)
    # CRR errors can oscillate; do not assume monotonic convergence at every step.
    assert fine < coarse
    assert fine < 0.003


@pytest.mark.parametrize("kind", ["call", "put"])
@pytest.mark.parametrize("spot", [80, 100, 120])
def test_greeks_against_finite_differences(kind, spot):
    parameters = {**BASE, "spot": spot, "option_type": kind}
    analytical = calculate_greeks(GreeksRequest(**parameters))
    h = spot * 1e-4
    up = black_scholes_price(**{**parameters, "spot": spot + h})
    down = black_scholes_price(**{**parameters, "spot": spot - h})
    center = black_scholes_price(**parameters)
    assert (up - down) / (2 * h) == pytest.approx(analytical.delta, abs=1e-7)
    assert (up - 2 * center + down) / h**2 == pytest.approx(analytical.gamma, abs=1e-7)
    v = 1e-5
    vol_up = black_scholes_price(**{**parameters, "volatility": parameters["volatility"] + v})
    vol_down = black_scholes_price(**{**parameters, "volatility": parameters["volatility"] - v})
    assert (vol_up - vol_down) / (2 * v) == pytest.approx(analytical.vega, abs=1e-6)


@pytest.mark.parametrize("steps", [0, -1, 2001, 2.5, True, "500", None])
def test_invalid_steps(client, steps):
    assert client.post("/valuation/price", json={**BASE, "steps": steps}).status_code == 422


@pytest.mark.parametrize("field,value", [("spot", 0), ("strike", -1), ("maturity", 0), ("volatility", 0), ("rate", "NaN"), ("option_type", "C")])
def test_invalid_parameters(client, field, value):
    assert client.post("/valuation/price", json={**BASE, field: value}).status_code == 422


def test_invalid_tree_probability(client):
    response = client.post("/valuation/price", json={**BASE, "rate": 0.5, "steps": 1})
    assert response.status_code == 422
    assert "probability" in response.json()["detail"]


def test_overflow(client):
    assert client.post("/valuation/price", json={**BASE, "volatility": 1e308}).status_code == 422


def test_one_step_tree():
    # Hand-worked tree: u=2, d=0.5, p=1/3, terminal call payoffs 100 and 0.
    assert crr_price(100, 100, 1, 0, math.log(2), "call", 1) == pytest.approx(100 / 3)
