"""
Unit tests for volatility metrics.

Tests:
- Historical volatility
- Rolling volatility
- IV Rank
- IV Percentile
"""


import numpy as np

from analysis.volatility_metrics import (
    historical_volatility,
    iv_rank,
    iv_percentile,
)



def test_historical_volatility():

    prices = [
        100,
        101,
        102,
        103,
        104,
    ]

    hv = historical_volatility(
        prices
    )

    assert hv > 0



def test_historical_volatility_constant_price():

    prices = [
        100,
        100,
        100,
        100,
    ]

    hv = historical_volatility(
        prices
    )

    assert np.isclose(
        hv,
        0
    )



def test_iv_rank():

    iv = [
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
    ]

    rank = iv_rank(
        iv
    )

    assert np.isclose(
        rank,
        1.0
    )



def test_iv_rank_middle_value():

    iv = [
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
    ]

    rank = iv_rank(
        iv,
        current_iv=0.30
    )

    expected = (
        0.30 - 0.20
    ) / (
        0.40 - 0.20
    )

    assert np.isclose(
        rank,
        expected
    )



def test_iv_percentile():

    iv = [
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
    ]

    percentile = iv_percentile(
        iv
    )

    assert np.isclose(
        percentile,
        0.8
    )



def test_iv_percentile_current_value():

    iv = [
        0.20,
        0.25,
        0.30,
        0.35,
        0.40,
    ]

    percentile = iv_percentile(
        iv,
        current_iv=0.30
    )


    # Values below 0.30:
    #
    # 0.20
    # 0.25
    #
    # 2 / 5 = 0.4

    assert np.isclose(
        percentile,
        0.4
    )