"""
Unit tests for BacktestAnalyzer.

Tests:
- Performance metrics integration
- Trade statistics
- Summary output
"""


import numpy as np
import pandas as pd

from analysis.backtest_analysis import (
    BacktestAnalyzer,
)



def test_trade_statistics():

    trades = pd.DataFrame(
        {
            "net_return":
            [
                0.10,
                -0.05,
                0.20,
                0.03,
            ]
        }
    )


    analyzer = BacktestAnalyzer(
        trades
    )


    stats = analyzer.trade_statistics()


    assert stats["num_trades"] == 4

    assert stats["winning_trades"] == 3

    assert stats["losing_trades"] == 1

    assert np.isclose(
        stats["win_rate"],
        0.75
    )



def test_performance_integration():

    trades = pd.DataFrame(
        {
            "net_return":
            [
                0.10,
                -0.05,
                0.20,
                0.03,
            ]
        }
    )


    analyzer = BacktestAnalyzer(
        trades
    )


    performance = (
        analyzer.performance()
    )


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

        assert key in performance



def test_summary_structure():

    trades = pd.DataFrame(
        {
            "net_return":
            [
                0.01,
                0.02,
                -0.01,
            ]
        }
    )


    analyzer = BacktestAnalyzer(
        trades
    )


    summary = analyzer.summary()


    assert "performance" in summary

    assert "trade_statistics" in summary



def test_missing_return_column():

    trades = pd.DataFrame(
        {
            "return":
            [
                0.1,
                0.2,
            ]
        }
    )


    try:

        BacktestAnalyzer(
            trades
        )

    except ValueError:

        assert True

    else:

        assert False