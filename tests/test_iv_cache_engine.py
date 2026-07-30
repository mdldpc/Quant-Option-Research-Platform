import pandas as pd
import pytest

from datetime import datetime

from scripts.iv_cache_engine import (
    add_iv_cache,
)

from framework.pricing.black76 import (
    black76_price,
)



def test_add_iv_cache():

    F = 4000
    K = 4000

    trade_date = datetime(
        2025,
        12,
        15,
    )

    expiry_code = "2601"

    T = (
        datetime(2026,1,16)
        -
        trade_date
    ).days / 365


    sigma_true = 0.25

    r = 0.017


    option_price = black76_price(
        F,
        K,
        T,
        r,
        sigma_true,
        "C",
    )


    df = pd.DataFrame(
        {
            "expiry_code":[expiry_code],

            "option_type":["C"],

            "strike":[K],

            "option_price":[option_price],

            "future_price":[F],
        }
    )


    result = add_iv_cache(
        df,
        trade_date,
    )


    assert (
        "T"
        in result.columns
    )


    assert (
        "implied_vol"
        in result.columns
    )


    assert result["implied_vol"].iloc[0] == pytest.approx(
        sigma_true,
        rel=1e-5,
    )