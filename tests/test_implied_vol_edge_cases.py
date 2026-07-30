import pytest


from framework.pricing.black76 import (
    black76_price,
)


from framework.pricing.implied_vol import (
    implied_volatility,
)



def test_iv_itm_call():

    F = 4000
    K = 3500
    T = 60 / 365
    r = 0.017

    sigma_true = 0.25


    price = black76_price(
        F,
        K,
        T,
        r,
        sigma_true,
        "C",
    )


    iv = implied_volatility(
        price,
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



def test_iv_otm_call():

    F = 4000
    K = 4500
    T = 60 / 365
    r = 0.017

    sigma_true = 0.30


    price = black76_price(
        F,
        K,
        T,
        r,
        sigma_true,
        "C",
    )


    iv = implied_volatility(
        price,
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



def test_invalid_market_price():

    F = 4000
    K = 4000
    T = 30 / 365
    r = 0.017


    with pytest.raises(
        ValueError
    ):

        implied_volatility(
            -1,
            F,
            K,
            T,
            r,
            "C",
        )

def test_invalid_option_type():

    with pytest.raises(ValueError):

        implied_volatility(
            100,
            4000,
            4000,
            30/365,
            0.017,
            "X",
        )

def test_zero_maturity():

    with pytest.raises(ValueError):

        implied_volatility(
            100,
            4000,
            4000,
            0,
            0.017,
            "C",
        )