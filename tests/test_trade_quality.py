import pandas as pd


from analysis.trade_quality import (
    TradeQualityAnalyzer,
)



def test_invalid_trade_detection():


    df = pd.DataFrame(

        {

        "strategy":
        [
            "long_atm_strangle",
            "long_atm_strangle",
        ],


        "entry_strangle_price":
        [
            100,
            100,
        ],


        "exit_strangle_price":
        [
            120,
            None,
        ]

        }

    )


    result = (
        TradeQualityAnalyzer
        .analyze(df)
    )


    assert (
        result["generated_trades"]
        ==
        2
    )


    assert (
        result["completed_trades"]
        ==
        1
    )


    assert (
        result["invalid_trades"]
        ==
        1
    )