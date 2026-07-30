import pandas as pd


from analysis.strategy_return_series import (
    StrategyReturnBuilder,
)



def test_strategy_return_series():


    trades = pd.DataFrame(

        {

        "strategy":
        [
            "long_atm_strangle"
        ],

        "trade_id":
        [
            1
        ],

        "entry_date":
        [
            20260119
        ],

        "exit_date":
        [
            20260121
        ],

        "entry_strangle_price":
        [
            100
        ]

        }

    )


    snapshot = pd.DataFrame(

        {

        "trade_date":
        [
            "20260119",
            "20260120",
            "20260121",
        ],

        "strangle_price":
        [
            100,
            110,
            120,
        ]

        }

    )


    result = (
        StrategyReturnBuilder(
            trades,
            snapshot,
        )
        .build()
    )


    assert len(result)==3


    assert (
        result["nav"].iloc[-1]
        ==
        1.2
    )