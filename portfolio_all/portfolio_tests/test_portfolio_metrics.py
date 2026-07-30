import pandas as pd

from analysis.portfolio_metrics import (
    PortfolioMetrics,
)



def test_portfolio_metrics():


    df = pd.DataFrame(

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
        ],


        "strategy_b":
        [
            0.02,
            0.01,
            -0.01,
        ]

        }

    )


    pm = PortfolioMetrics(df)


    corr = (
        pm
        .correlation_matrix()
    )


    assert corr.shape == (2,2)


    vol = (
        pm
        .volatility()
    )


    assert len(vol)==2