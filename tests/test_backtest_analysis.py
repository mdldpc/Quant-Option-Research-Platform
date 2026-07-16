"""
Unit tests for BacktestAnalyzer.

Tests:

- Performance integration
- Trade statistics
- Equity statistics
- Summary structure

"""


import numpy as np
import pandas as pd


from analysis.backtest_analysis import (
    BacktestAnalyzer,
)



def create_test_trades():

    return pd.DataFrame(
        {
            "status":
            [
                "ok",
                "ok",
                "ok",
                "failed",
            ],

            "net_return":
            [
                0.10,
                -0.05,
                0.20,
                np.nan,
            ],
        }
    )



def test_trade_statistics():


    trades = create_test_trades()


    analyzer = BacktestAnalyzer(
        trades
    )


    stats = (
        analyzer.trade_statistics()
    )


    assert (
        stats["total_trades"]
        ==
        4
    )


    assert (
        stats["completed_trades"]
        ==
        3
    )


    assert (
        stats["skipped_trades"]
        ==
        1
    )


    assert np.isclose(
        stats["win_rate"],
        2 / 3,
    )



def test_performance_metrics():


    trades = create_test_trades()


    analyzer = BacktestAnalyzer(
        trades
    )


    performance = (
        analyzer.performance()
    )


    assert (
        "total_return"
        in performance
    )


    assert (
        "max_drawdown"
        in performance
    )


    assert (
        "sharpe_ratio"
        in performance
    )



def test_equity_statistics():


    trades = create_test_trades()


    analyzer = BacktestAnalyzer(
        trades
    )


    stats = (
        analyzer.equity_statistics()
    )


    assert (
        "final_equity"
        in stats
    )


    assert (
        "average_return"
        in stats
    )


    assert stats["final_equity"] > 0



def test_summary_structure():


    trades = create_test_trades()


    analyzer = BacktestAnalyzer(
        trades
    )


    summary = (
        analyzer.summary()
    )


    assert (
        "performance"
        in summary
    )


    assert (
        "trade_statistics"
        in summary
    )


    assert (
        "final_equity"
        in summary["performance"]
    )


    assert (
        "completed_trades"
        in summary["trade_statistics"]
    )