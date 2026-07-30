import pandas as pd


from analysis.trade_performance_adapter import (
    TradePerformanceAdapter,
)



def test_strangle_return():


    df = pd.DataFrame(

        {

            "strategy":
            [
                "long_atm_strangle"
            ],


            "entry_strangle_price":
            [
                100
            ],


            "exit_strangle_price":
            [
                120
            ],


            "holding_days":
            [
                5
            ]

        }

    )


    result = (
        TradePerformanceAdapter
        .adapt(df)
    )


    assert (
        result["return"].iloc[0]
        ==
        0.2
    )