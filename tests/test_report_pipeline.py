from pathlib import Path

import pandas as pd

from framework.runner import (
    run_strategy_report,
)



def test_run_strategy_report(tmp_path):


    trades = pd.DataFrame(
        {

            "trade_id":[1],

            "status":[
                "constructed"
            ],

            "entry_butterfly_price":[
                10
            ],

            "exit_butterfly_price":[
                12
            ],

        }
    )


    report_path = (
        tmp_path
        /
        "report.docx"
    )


    trades_path = (
        tmp_path
        /
        "trades.csv"
    )


    result = run_strategy_report(

        strategy_name=
        "long_call_butterfly",

        trades=trades,

        report_path=
        report_path,

        trades_path=
        trades_path,

    )


    assert (
        result.strategy_name
        ==
        "long_call_butterfly"
    )


    assert report_path.exists()