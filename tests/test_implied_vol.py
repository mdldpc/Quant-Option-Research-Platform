import pytest

from framework.pricing.black76 import (
    black76_price,
)

from framework.pricing.implied_vol import (
    implied_volatility,
)



def test_implied_volatility_call():

    F = 4000

    K = 4000

    T = 30 / 365

    r = 0.017


    sigma_true = 0.20


    market_price = black76_price(
        F,
        K,
        T,
        r,
        sigma_true,
        "C",
    )


    iv = implied_volatility(
        market_price,
        F,
        K,
        T,
        r,
        "C",
    )


    assert iv == pytest.approx(
        sigma_true,
        rel=1e-5,
    )



def test_implied_volatility_put():

    F = 4000

    K = 4100

    T = 60 / 365

    r = 0.017


    sigma_true = 0.35


    market_price = black76_price(
        F,
        K,
        T,
        r,
        sigma_true,
        "P",
    )


    iv = implied_volatility(
        market_price,
        F,
        K,
        T,
        r,
        "P",
    )


    assert iv == pytest.approx(
        sigma_true,
        rel=1e-5,
    )