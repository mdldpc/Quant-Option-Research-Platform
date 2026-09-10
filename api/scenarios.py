"""Deterministic mark-to-model shocks; no trading, funding or FX cash flows."""

import math

from api.routes.risk import calculate_greeks
from api.scenario_schemas import (
    PnLComponents, PositionScenarioResult, ScenarioRequest, ScenarioResponse, ScenarioResult,
)
from api.valuation import black_scholes_price


def theta_and_rho(position):
    """Calendar-time theta per year and rho per 1.0 rate change, q=0."""
    s, k, t, r, v = (
        position.spot, position.strike, position.maturity, position.rate, position.volatility,
    )
    root_t = math.sqrt(t)
    d1 = (math.log(s) - math.log(k) + (r + v * v / 2) * t) / (v * root_t)
    d2 = d1 - v * root_t
    pdf = math.exp(-d1 * d1 / 2) / math.sqrt(2 * math.pi)
    discounted_strike = k * math.exp(-r * t)
    diffusion = -s * pdf * v / (2 * root_t)
    if position.option_type == "call":
        probability = math.erfc(-d2 / math.sqrt(2)) / 2
        return diffusion - r * discounted_strike * probability, t * discounted_strike * probability
    probability = math.erfc(d2 / math.sqrt(2)) / 2
    return diffusion + r * discounted_strike * probability, -t * discounted_strike * probability


def run_scenarios(request: ScenarioRequest) -> ScenarioResponse:
    """Approximation uses base Greeks: delta*dS + gamma*dS²/2 + vega*dv
    + calendar_theta*elapsed_years + rho*dr. Cross and higher orders are omitted.
    """
    baseline = []
    for position in request.positions:
        parameters = position.model_dump(exclude={"quantity", "position_id"})
        price = black_scholes_price(**parameters)
        greeks = calculate_greeks(position)
        theta, rho = theta_and_rho(position)
        baseline.append((position, parameters, price, greeks, theta, rho))
    results = []
    for scenario in request.scenarios:
        positions = []
        for position, parameters, base_price, greeks, theta, rho in baseline:
            elapsed = scenario.days_elapsed / 365
            stressed = {
                **parameters,
                "spot": position.spot * (1 + scenario.spot_return),
                "volatility": position.volatility + scenario.volatility_shift,
                "rate": position.rate + scenario.rate_shift,
                "maturity": position.maturity - elapsed,
            }
            stressed_price = black_scholes_price(**stressed)
            ds = stressed["spot"] - position.spot
            quantity = position.quantity
            components = PnLComponents(
                delta=quantity * greeks.delta * ds,
                gamma=quantity * greeks.gamma * ds * ds / 2,
                vega=quantity * greeks.vega * scenario.volatility_shift,
                theta=quantity * theta * elapsed,
                rho=quantity * rho * scenario.rate_shift,
            )
            approximation = math.fsum(components.model_dump().values())
            base_value = quantity * base_price
            stressed_value = quantity * stressed_price
            pnl = stressed_value - base_value
            positions.append(PositionScenarioResult(
                position_id=position.position_id, base_price=base_price,
                stressed_price=stressed_price, base_value=base_value,
                stressed_value=stressed_value, full_revaluation_pnl=pnl,
                approximation_pnl=approximation, approximation_error=pnl - approximation,
                components=components,
            ))
        components = PnLComponents(**{
            key: math.fsum(getattr(p.components, key) for p in positions)
            for key in PnLComponents.model_fields
        })
        totals = {
            key: math.fsum(getattr(p, key) for p in positions)
            for key in ("base_value", "stressed_value", "full_revaluation_pnl",
                        "approximation_pnl", "approximation_error")
        }
        results.append(ScenarioResult(
            name=scenario.name, **totals, components=components, positions=positions,
        ))
    return ScenarioResponse(base_value=results[0].base_value, scenarios=results)
