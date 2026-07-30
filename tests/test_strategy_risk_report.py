import pandas as pd

from analysis.strategy_risk_report import (
    StrategyRiskReport,
)



def test_strategy_risk_report():


    returns = pd.DataFrame(

        {

        "trade_date":
        [
            "20260101",
            "20260102",
            "20260103",
        ],


        "strategy_a":
        [
            0.01,
            -0.02,
            0.03,
        ]

        }

    )


    trade_files = {

        "strategy_a":
        "dummy.csv"

    }


    report = StrategyRiskReport(

        returns,

        trade_files

    )


    assert report is not None