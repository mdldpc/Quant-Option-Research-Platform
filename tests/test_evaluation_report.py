import pandas as pd


from analysis.evaluation_report import (
    EvaluationReport,
)



def test_unified_report():


    trades = pd.DataFrame(

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
            90,
        ],


        "holding_days":
        [
            5,
            5,
        ]

        }

    )


    result = (
        EvaluationReport
        .generate(
            trades
        )
    )


    assert (
        result["strategy"]
        ==
        "long_atm_strangle"
    )


    assert (
        result["generated_trades"]
        ==
        2
    )


    assert (
        result["total_trades"]
        ==
        2
    )


    assert (
        "sharpe_ratio"
        in result
    )