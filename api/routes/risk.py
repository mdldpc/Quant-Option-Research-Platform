import math

import pandas as pd
from fastapi import APIRouter, HTTPException

from api.schemas import GreeksRequest, GreeksResponse, PortfolioRequest
from framework.risk.exposure import compute_exposure

router = APIRouter(prefix="/risk", tags=["risk"])


def calculate_greeks(option: GreeksRequest) -> GreeksResponse:
    """Black-Scholes Greeks for a European option with zero dividend yield."""
    try:
        sqrt_t = math.sqrt(option.maturity)
        sigma_sqrt_t = option.volatility * sqrt_t
        d1 = (
            math.log(option.spot) - math.log(option.strike)
            + (option.rate + 0.5 * option.volatility**2) * option.maturity
        ) / sigma_sqrt_t
        pdf = math.exp(-0.5 * d1 * d1) / math.sqrt(2.0 * math.pi)
        delta = (
            0.5 * math.erfc(-d1 / math.sqrt(2.0))
            if option.option_type == "call"
            else -0.5 * math.erfc(d1 / math.sqrt(2.0))
        )
        gamma = pdf / option.spot / sigma_sqrt_t
        vega = option.spot * pdf * sqrt_t
        if not all(math.isfinite(value) for value in (d1, delta, gamma, vega)):
            raise ValueError("Non-finite calculation")
    except (OverflowError, ZeroDivisionError, ValueError) as exc:
        raise HTTPException(422, "Parameters exceed the supported numerical range.") from exc
    return GreeksResponse(delta=delta, gamma=gamma, vega=vega)


@router.post("/greeks", response_model=GreeksResponse)
def greeks(option: GreeksRequest) -> GreeksResponse:
    return calculate_greeks(option)


@router.post("/portfolio", response_model=GreeksResponse)
def portfolio(request: PortfolioRequest) -> GreeksResponse:
    rows = []
    for position in request.root:
        values = calculate_greeks(position)
        row = {
            "net_delta": position.quantity * values.delta,
            "net_gamma": position.quantity * values.gamma,
            "net_vega": position.quantity * values.vega,
        }
        if not all(math.isfinite(value) for value in row.values()):
            raise HTTPException(422, "Position exposure exceeds the supported numerical range.")
        rows.append(row)
    exposure = compute_exposure(pd.DataFrame(rows))
    values = (exposure.net_delta, exposure.net_gamma, exposure.net_vega)
    if not all(math.isfinite(value) for value in values):
        raise HTTPException(422, "Portfolio exposure exceeds the supported numerical range.")
    return GreeksResponse(delta=values[0], gamma=values[1], vega=values[2])
