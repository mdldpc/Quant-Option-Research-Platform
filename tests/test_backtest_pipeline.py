"""
Tests for unified backtest pipeline.

Validates:

BaseBacktester.backtest()

run()
    |
    v
finalize()
    |
    v
BacktestResult
"""


from pathlib import Path

import pandas as pd

from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)

from framework.strategy.contracts import (
    BacktestResult,
)



def test_backtest_pipeline_returns_result(tmp_path):

    trades = pd.DataFrame(
        {
            "trade_id": [1, 2],

            "status": [
                "constructed",
                "constructed",
            ],

            "entry_butterfly_price": [
                10,
                20,
            ],

            "exit_butterfly_price": [
                12,
                18,
            ],
        }
    )


    backtester = ButterflyBacktester(
        trades
    )


    report_path = (
        tmp_path /
        "report.txt"
    )

    trades_path = (
        tmp_path /
        "trades.csv"
    )


    result = backtester.backtest(
        report_path=report_path,
        trades_path=trades_path,
    )


    assert isinstance(
        result,
        BacktestResult
    )


    assert result.strategy_name == (
        "long_call_butterfly"
    )


    assert result.total_trades == 2


    assert result.completed_trades == 2


    assert result.status == "success"



def test_backtest_pipeline_outputs_files(tmp_path):

    trades = pd.DataFrame(
        {
            "trade_id": [1],

            "status": [
                "constructed"
            ],

            "entry_butterfly_price": [
                10
            ],

            "exit_butterfly_price": [
                11
            ],
        }
    )


    backtester = ButterflyBacktester(
        trades
    )


    report_path = (
        tmp_path /
        "report.txt"
    )

    trades_path = (
        tmp_path /
        "trades.csv"
    )


    backtester.backtest(
        report_path=report_path,
        trades_path=trades_path,
    )


    assert report_path.exists()

    assert trades_path.exists()