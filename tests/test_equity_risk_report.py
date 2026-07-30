import pandas as pd

from analysis.equity_risk_report import (
    EquityRiskReport
)



def test_equity_risk_report():


    df=pd.DataFrame(

        {

        "equity":
        [
            1,
            1.1,
            1.0
        ],


        "daily_return":
        [
            0,
            0.1,
            -0.09
        ]

        }

    )


    path="test_equity.csv"

    df.to_csv(
        path,
        index=False
    )


    report=EquityRiskReport(

        {
            "test":
            path
        }

    )


    result=report.generate()


    assert (
        result.shape[0]
        ==
        1
    )