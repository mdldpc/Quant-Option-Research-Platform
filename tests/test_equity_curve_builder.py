import pandas as pd

from analysis.equity_curve_builder import (
    EquityCurveBuilder,
)



def test_equity_curve_builder():


    trades = pd.DataFrame(

        {

        "status":
        [
            "constructed"
        ],


        "entry_date":
        [
            20260101
        ],


        "exit_date":
        [
            20260105
        ],


        "entry_price":
        [
            100
        ],


        "exit_price":
        [
            110
        ]

        }

    )


    builder = EquityCurveBuilder(
        trades
    )


    curve = builder.build()


    assert (
        len(curve) > 0
    )


    assert (
        "equity"
        in
        curve.columns
    )