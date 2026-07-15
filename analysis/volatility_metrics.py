"""
Volatility Metrics Module

Provides volatility analytics:

- Historical Volatility
- IV Rank
- IV Percentile
"""


import numpy as np
import pandas as pd


def historical_volatility(
    prices,
    window=None,
    periods_per_year=252,
):
    """
    Calculate annualized historical volatility.

    Parameters
    ----------
    prices :
        Price series.

    window :
        Rolling window.
        If None, use all observations.

    periods_per_year :
        Trading periods per year.

    Returns
    -------
    float or pandas.Series
        Annualized volatility.
    """

    prices = (
        pd.Series(prices)
        .dropna()
        .astype(float)
    )

    log_returns = np.log(
        prices /
        prices.shift(1)
    ).dropna()


    if window is not None:

        volatility = (
            log_returns
            .rolling(window)
            .std()
            *
            np.sqrt(periods_per_year)
        )

        return volatility


    return (
        log_returns.std()
        *
        np.sqrt(periods_per_year)
    )



def iv_rank(
    iv_series,
    current_iv=None,
):
    """
    Calculate IV Rank.

    Formula:

    (Current IV - Historical Low)
    /
    (Historical High - Historical Low)


    Parameters
    ----------
    iv_series :
        Historical implied volatility series.

    current_iv :
        Current IV.
        If None, use latest value.


    Returns
    -------
    float
    """

    iv = (
        pd.Series(iv_series)
        .dropna()
        .astype(float)
    )


    if current_iv is None:
        current_iv = iv.iloc[-1]


    iv_low = iv.min()
    iv_high = iv.max()


    if iv_high == iv_low:
        return np.nan


    return (
        current_iv - iv_low
    ) / (
        iv_high - iv_low
    )



def iv_percentile(
    iv_series,
    current_iv=None,
):
    """
    Calculate IV Percentile.

    Measures the percentage of
    historical IV observations below
    current IV.

    Parameters
    ----------
    iv_series :
        Historical implied volatility.

    current_iv :
        Current IV.
        If None, use latest value.


    Returns
    -------
    float
    """

    iv = (
        pd.Series(iv_series)
        .dropna()
        .astype(float)
    )


    if current_iv is None:
        current_iv = iv.iloc[-1]


    return (
        (iv < current_iv)
        .mean()
    )