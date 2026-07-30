import numpy as np

from scipy.optimize import brentq

from framework.pricing.black76 import (
    black76_price,
)


def implied_volatility(
    market_price,
    F,
    K,
    T,
    r,
    option_type="C",
):
    """
    Solve Black-76 implied volatility.

    Returns
    -------
    float
        Implied volatility.

    Notes
    -----
    Invalid or unsolvable cases return np.nan.
    This behavior is suitable for batch pipelines.
    """


    # -----------------------------
    # Validation
    # -----------------------------

    if market_price <= 0:
        raise ValueError(
            "Market price must be positive."
        )


    if F <= 0 or K <= 0:
        raise ValueError(
            "F and K must be positive."
        )


    if T <= 0:
        raise ValueError(
            "Time to maturity must be positive."
        )


    if option_type not in [
        "C",
        "P",
    ]:
        raise ValueError(
            "option_type must be C or P."
        )


    # -----------------------------
    # Root function
    # -----------------------------

    def objective(sigma):

        return (
            black76_price(
                F,
                K,
                T,
                r,
                sigma,
                option_type,
            )
            -
            market_price
        )


    # -----------------------------
    # Solve
    # -----------------------------

    try:

        iv = brentq(
            objective,
            1e-6,
            5.0,
            maxiter=100,
        )

    except ValueError:

        return np.nan


    return iv