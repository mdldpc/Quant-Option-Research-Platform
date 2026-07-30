import pandas as pd

from analysis.portfolio_valuation import (
    StrategyValuator,
)



def test_trade_valuation():


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



    trade = {

        "strategy":
        "long_atm_strangle",

        "trade_id":
        1,

        "entry_date":
        20260119,

        "exit_date":
        20260121,

        "entry_strangle_price":
        100,

    }



    valuator = StrategyValuator(
        snapshot
    )


    result = valuator.value_trade(
        trade
    )


    assert len(result)==3


    assert (
        result["nav"].iloc[-1]
        ==
        1.2
    )