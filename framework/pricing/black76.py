import numpy as np
from scipy.stats import norm


def black76_price(
    F,
    K,
    T,
    r,
    sigma,
    option_type="C",
):
    """
    Black-76 option pricing model.

    Parameters
    ----------
    F:
        Futures price

    K:
        Strike price

    T:
        Time to maturity (years)

    r:
        Risk-free rate

    sigma:
        Volatility

    option_type:
        "C" for call
        "P" for put

    Returns
    -------
    option price
    """


    if T <= 0:
        raise ValueError(
            "Time to maturity must be positive"
        )


    if sigma <= 0:
        raise ValueError(
            "Volatility must be positive"
        )


    sqrt_T = np.sqrt(T)


    d1 = (
        np.log(F / K)
        +
        0.5 * sigma ** 2 * T
    ) / (
        sigma * sqrt_T
    )


    d2 = (
        d1
        -
        sigma * sqrt_T
    )


    discount = np.exp(
        -r * T
    )


    if option_type.upper() == "C":

        price = discount * (
            F * norm.cdf(d1)
            -
            K * norm.cdf(d2)
        )


    elif option_type.upper() == "P":

        price = discount * (
            K * norm.cdf(-d2)
            -
            F * norm.cdf(-d1)
        )


    else:

        raise ValueError(
            "option_type must be C or P"
        )


    return price