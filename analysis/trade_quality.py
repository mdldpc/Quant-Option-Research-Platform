"""
Trade Quality Analysis

Check whether backtest trades
can be used for performance evaluation.
"""


import pandas as pd



class TradeQualityAnalyzer:



    PRICE_COLUMNS = {


        "long_atm_strangle":
        (
            "entry_strangle_price",
            "exit_strangle_price",
        ),


        "long_call_butterfly":
        (
            "entry_butterfly_price",
            "exit_butterfly_price",
        ),


        "calendar_spread":
        (
            "entry_calendar_price",
            "exit_calendar_price",
        ),

    }



    @classmethod
    def analyze(
        cls,
        trades: pd.DataFrame,
    ):


        strategy = (
            trades["strategy"]
            .iloc[0]
        )


        entry_col, exit_col = (
            cls.PRICE_COLUMNS[
                strategy
            ]
        )


        total = len(trades)


        valid = trades.dropna(
            subset=[
                entry_col,
                exit_col,
            ]
        )


        completed = len(valid)


        invalid = (
            total
            -
            completed
        )


        result = {


            "strategy":
                strategy,


            "generated_trades":
                total,


            "completed_trades":
                completed,


            "invalid_trades":
                invalid,


            "invalid_ratio":
                (
                    invalid / total
                    if total > 0
                    else 0
                ),

        }


        if invalid > 0:


            invalid_rows = trades[
                trades[
                    exit_col
                ].isna()
            ]


            result[
                "invalid_reason"
            ] = (
                "missing_exit_price"
            )


        else:

            result[
                "invalid_reason"
            ] = None



        return result