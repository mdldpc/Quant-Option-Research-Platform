"""Independent zero-dividend European option pricing; no research data required."""

import math

import numpy as np


def black_scholes_price(spot, strike, maturity, rate, volatility, option_type):
    """Price a validated European call or put using the closed-form model."""
    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot) - math.log(strike) + (rate + volatility**2 / 2) * maturity) / (volatility * sqrt_t)
    d2 = d1 - volatility * sqrt_t
    discount = math.exp(-rate * maturity)
    if not all(math.isfinite(x) for x in (d1, d2, discount)):
        raise ValueError("Parameters exceed the supported numerical range.")
    cdf = lambda x: math.erfc(-x / math.sqrt(2)) / 2
    if option_type == "call":
        price = spot * cdf(d1) - strike * discount * cdf(d2)
    else:
        price = strike * discount * cdf(-d2) - spot * cdf(-d1)
    if not math.isfinite(price):
        raise ValueError("Price exceeds the supported numerical range.")
    return max(0.0, price)


def crr_price(spot, strike, maturity, rate, volatility, option_type, steps):
    """CRR backward induction, O(steps**2) time and O(steps) memory.

    Inputs are validated by the API schema. Only terminal exercise is allowed.
    A coarse tree with invalid risk-neutral probability is rejected, not clipped.
    """
    dt = maturity / steps
    move = volatility * math.sqrt(dt)
    spread = math.expm1(2 * move)
    probability = math.expm1(rate * dt + move) / spread
    discount = math.exp(-rate * dt)
    if not (math.isfinite(probability) and 0 <= probability <= 1):
        raise ValueError("Invalid CRR probability: increase steps or review rate and volatility.")
    with np.errstate(over="raise", invalid="raise", divide="raise"):
        prices = np.exp(math.log(spot) + (2 * np.arange(steps + 1) - steps) * move)
        values = np.maximum(prices - strike if option_type == "call" else strike - prices, 0)
        for remaining in range(steps, 0, -1):
            values = discount * ((1 - probability) * values[:remaining] + probability * values[1:remaining + 1])
    price = float(values[0])
    if not math.isfinite(price):
        raise ValueError("Price exceeds the supported numerical range.")
    return price
