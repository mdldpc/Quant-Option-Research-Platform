import pandas as pd

from pathlib import Path

from framework.runner import (
    run_strategy,
)

from framework.strategy.contracts import (
    BacktestResult,
)



def test_run_strategy():

    trades = pd.DataFrame(
        {

            "trade_id":
            [
                1
            ],


            "status":
            [
                "constructed"
            ],


            "entry_butterfly_price":
            [
                10
            ],


            "exit_butterfly_price":
            [
                12
            ],

        }
    )


    result = run_strategy(
        strategy_name="long_call_butterfly",

        trades=trades,

        report_path=Path(
            "tests/test_report.txt"
        ),

        trades_path=Path(
            "tests/test_trades.csv"
        ),
    )


    assert isinstance(
        result,
        BacktestResult,
    )


    assert (
        result.strategy_name
        ==
        "long_call_butterfly"
    )