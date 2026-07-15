"""
Unit tests for PerformanceMetrics.

Tests:
- Total return
- Annualized return
- Volatility
- Sharpe ratio
- Maximum drawdown
- Win rate
- Profit factor
"""


import numpy as np

from analysis.performance_metrics import PerformanceMetrics


def test_total_return():
    """
    Test cumulative return calculation.
    """

    returns = [
        0.10,
        -0.05,
    ]

    metrics = PerformanceMetrics(
        returns
    )

    expected = (
        1.10 * 0.95
        - 1
    )

    assert np.isclose(
        metrics.total_return(),
        expected
    )


def test_max_drawdown():
    """
    Test maximum drawdown.
    """

    returns = [
        0.10,
        -0.20,
        0.05,
    ]

    metrics = PerformanceMetrics(
        returns
    )

    drawdown = (
        metrics.max_drawdown()
    )

    assert drawdown < 0


def test_win_rate():
    """
    Test percentage of positive returns.
    """

    returns = [
        0.01,
        -0.01,
        0.02,
        0.03,
    ]

    metrics = PerformanceMetrics(
        returns
    )

    assert np.isclose(
        metrics.win_rate(),
        0.75
    )


def test_profit_factor():
    """
    Test profit factor.
    """

    returns = [
        0.10,
        0.05,
        -0.05,
    ]

    metrics = PerformanceMetrics(
        returns
    )

    expected = (
        0.15 /
        0.05
    )

    assert np.isclose(
        metrics.profit_factor(),
        expected
    )


def test_summary_output():
    """
    Ensure summary contains
    all required metrics.
    """

    returns = [
        0.01,
        0.02,
        -0.01,
    ]

    metrics = PerformanceMetrics(
        returns
    )

    result = metrics.summary()


    required_keys = [
        "total_return",
        "annualized_return",
        "annualized_volatility",
        "sharpe_ratio",
        "sortino_ratio",
        "max_drawdown",
        "win_rate",
        "profit_factor",
    ]


    for key in required_keys:

        assert key in result