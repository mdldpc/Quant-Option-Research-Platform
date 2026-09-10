import math

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.scenario_schemas import ScenarioPosition
from api.scenarios import theta_and_rho
from api.valuation import black_scholes_price

BASE = dict(spot=100, strike=100, maturity=1, rate=0.05,
            volatility=0.2, option_type="call", quantity=2, position_id="call")


@pytest.fixture
def client():
    with TestClient(app) as session:
        yield session


def request(client, positions=None, **shock):
    return client.post("/risk/scenarios", json={
        "positions": [BASE] if positions is None else positions,
        "scenarios": [{"name": "test", **shock}],
    })


def test_no_shock(client):
    response = request(client)
    assert response.status_code == 200
    result = response.json()["scenarios"][0]
    assert result["base_value"] == pytest.approx(2 * 10.450583572185565)
    assert result["full_revaluation_pnl"] == 0
    assert result["approximation_pnl"] == 0
    assert result["approximation_error"] == 0


def test_aggregation_and_revaluation(client):
    positions = [BASE, {**BASE, "position_id": "put", "option_type": "put", "quantity": -3}]
    response = request(client, positions, spot_return=-0.10,
                       volatility_shift=0.05, rate_shift=0.01, days_elapsed=7)
    assert response.status_code == 200
    result = response.json()["scenarios"][0]
    for row, position in zip(result["positions"], positions):
        params = {k: v for k, v in position.items() if k not in ("quantity", "position_id")}
        expected = black_scholes_price(**{**params, "spot": 90, "volatility": 0.25,
                                          "rate": 0.06, "maturity": 1 - 7 / 365})
        assert row["stressed_price"] == pytest.approx(expected)
        assert row["stressed_value"] == pytest.approx(position["quantity"] * expected)
        assert row["approximation_pnl"] == pytest.approx(sum(row["components"].values()))
    for key in ("base_value", "stressed_value", "full_revaluation_pnl", "approximation_pnl", "approximation_error"):
        assert result[key] == pytest.approx(math.fsum(p[key] for p in result["positions"]))
    assert result["full_revaluation_pnl"] == pytest.approx(result["stressed_value"] - result["base_value"])
    assert result["approximation_error"] == pytest.approx(result["full_revaluation_pnl"] - result["approximation_pnl"])


def test_put_call_parity_scenario(client):
    # Long call and short put replicate S - K*exp(-rT), independent of volatility.
    positions = [{**BASE, "quantity": 1}, {**BASE, "position_id": "put", "option_type": "put", "quantity": -1}]
    result = request(client, positions, spot_return=-0.1, volatility_shift=0.05,
                     rate_shift=0.01, days_elapsed=7).json()["scenarios"][0]
    expected = (90 - 100 * math.exp(-0.06 * (1 - 7 / 365))) - (100 - 100 * math.exp(-0.05))
    assert result["full_revaluation_pnl"] == pytest.approx(expected, abs=1e-10)


@pytest.mark.parametrize("kind", ["call", "put"])
def test_theta_rho_against_price_differences(kind):
    parameters = {k: v for k, v in BASE.items() if k not in ("quantity", "position_id")}
    parameters["option_type"] = kind
    theta, rho = theta_and_rho(ScenarioPosition(**{**BASE, "option_type": kind}))
    h = 1e-5
    def shifted(field, difference):
        return black_scholes_price(**{**parameters, field: parameters[field] + difference})
    assert theta == pytest.approx((shifted("maturity", -h) - shifted("maturity", h)) / (2 * h), abs=1e-7)
    assert rho == pytest.approx((shifted("rate", h) - shifted("rate", -h)) / (2 * h), abs=1e-6)


@pytest.mark.parametrize("shock,component", [
    ({"spot_return": 1e-4}, "delta"), ({"volatility_shift": 1e-5}, "vega"),
    ({"rate_shift": 1e-5}, "rho"), ({"days_elapsed": 0.001}, "theta"),
])
def test_small_shock_approximation(client, shock, component):
    result = request(client, **shock).json()["scenarios"][0]
    assert abs(result["approximation_error"]) < 1e-6
    assert result["components"][component] != 0


@pytest.mark.parametrize("positions", [[], [{**BASE, "quantity": 0}],
    [BASE, {**BASE, "position_id": "offset", "quantity": -2}]])
def test_empty_zero_and_offsetting(client, positions):
    response = request(client, positions, spot_return=-0.1, volatility_shift=0.05, days_elapsed=7)
    assert response.status_code == 200
    result = response.json()["scenarios"][0]
    for key in ("base_value", "stressed_value", "full_revaluation_pnl", "approximation_pnl", "approximation_error"):
        assert result[key] == 0


@pytest.mark.parametrize("shock", [
    {"spot_return": -1}, {"volatility_shift": -0.2}, {"days_elapsed": -1},
    {"days_elapsed": 365}, {"days_elapsed": 366}, {"spot_return": "-0.1"},
    {"rate_shift": True}, {"volatility_shift": "NaN"}, {"days_elapsed": None},
])
def test_invalid_scenario(client, shock):
    assert request(client, **shock).status_code == 422


def test_shortest_maturity_controls_horizon(client):
    assert request(client, [BASE, {**BASE, "position_id": "short", "maturity": 1 / 365}], days_elapsed=2).status_code == 422


def test_negative_rate_is_allowed(client):
    assert request(client, rate_shift=-0.1).status_code == 200


def test_numerical_overflow_is_rejected(client):
    assert request(client, volatility_shift=1e308).status_code == 422


def test_duplicate_ids_and_names(client):
    assert request(client, [BASE, BASE]).status_code == 422
    payload = {"positions": [BASE], "scenarios": [{"name": "same"}, {"name": "same"}]}
    assert client.post("/risk/scenarios", json=payload).status_code == 422


def test_request_size_bounds(client):
    for positions, scenarios in [
        ([{**BASE, "position_id": str(i)} for i in range(1001)], [{"name": "one"}]),
        ([BASE], [{"name": str(i)} for i in range(101)]),
        ([{**BASE, "position_id": str(i)} for i in range(101)], [{"name": str(i)} for i in range(100)]),
        ([BASE], []),
    ]:
        assert client.post("/risk/scenarios", json={"positions": positions, "scenarios": scenarios}).status_code == 422
