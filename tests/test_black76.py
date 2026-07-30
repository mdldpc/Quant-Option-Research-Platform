import pytest


from framework.pricing.black76 import (
    black76_price,
)



def test_call_put_parity():


    F = 4000

    K = 4000

    T = 30 / 365

    r = 0.017

    sigma = 0.20



    call = black76_price(
        F,
        K,
        T,
        r,
        sigma,
        "C",
    )


    put = black76_price(
        F,
        K,
        T,
        r,
        sigma,
        "P",
    )


    lhs = call - put


    rhs = (
        (F - K)
        *
        __import__("math")
        .exp(
            -r * T
        )
    )


    assert abs(
        lhs - rhs
    ) < 1e-8




def test_atm_call_positive():


    price = black76_price(

        F=4000,

        K=4000,

        T=30/365,

        r=0.017,

        sigma=0.20,

        option_type="C",

    )


    assert price > 0



def test_invalid_time():

    with pytest.raises(
        ValueError
    ):

        black76_price(

            F=4000,

            K=4000,

            T=0,

            r=0.017,

            sigma=0.2,

            option_type="C",

        )



def test_invalid_volatility():

    with pytest.raises(
        ValueError
    ):

        black76_price(

            F=4000,

            K=4000,

            T=30/365,

            r=0.017,

            sigma=0,

            option_type="C",

        )