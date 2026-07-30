"""
Trade Performance Adapter v1.1

Convert strategy backtest output
into standardized trade performance dataframe.

Responsibilities:
    - Standardize trade return calculation
    - Preserve expired trades
    - Provide realized_return field

Does NOT handle:
    - expiration payoff valuation
    - option pricing
    - settlement calculation
"""


import pandas as pd

from analysis.expired_trade_valuation import (
    ExpiredTradeValuator
)

class TradePerformanceAdapter:



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

    @staticmethod
    def _calculate_expired_return(
        trade,
        valuator,
    ):

        strategy = trade["strategy"]


        if strategy == "long_atm_strangle":

            result = valuator.value_strangle(
                trade
            )


        elif strategy == "long_call_butterfly":

            result = valuator.value_butterfly(
                trade
            )


        elif strategy == "calendar_spread":

            result = valuator.value_calendar(
                trade
            )


        else:

            raise ValueError(
                f"Unsupported expired strategy: {strategy}"
            )


        return result["realized_return"]

    EXPIRED_STATUS = [

        "contract_expired",

        "calendar_pair_expired",

    ]



    @classmethod
    def adapt(
        cls,
        trades: pd.DataFrame,
        data_path = None,
    ):


        df = trades.copy()
        valuator = None


        if data_path is not None:

            valuator = ExpiredTradeValuator(
                data_path
            )


        if df.empty:

            return df



        strategy = (

            df["strategy"]

            .iloc[0]

        )



        if strategy not in cls.PRICE_COLUMNS:

            raise ValueError(

                f"Unsupported strategy: {strategy}"

            )



        entry_col, exit_col = (

            cls.PRICE_COLUMNS[strategy]

        )



        # ==================================================
        # Normal realized return calculation
        # ==================================================

        df["realized_return"] = (

            df[exit_col]

            -

            df[entry_col]

        ) / df[entry_col]

        # backward compatibility
        df["return"] = df["realized_return"]

        # ==================================================
        # Identify expired trades
        # ==================================================

        if "status" in df.columns:

            expired_mask = (

                df["status"]

                .isin(
                    cls.EXPIRED_STATUS
                )

            )

        else:

            expired_mask = pd.Series(

                False,

                index=df.index

            )



        # ==================================================
        # Expired trade valuation
        # ==================================================

        if valuator is not None:


            for idx, trade in df[
                expired_mask
            ].iterrows():


                try:

                    df.loc[
                        idx,
                        "realized_return"
                    ] = cls._calculate_expired_return(
                        trade,
                        valuator,
                    )


                except Exception:


                    df.loc[
                        idx,
                        "realized_return"
                    ] = None



        # ==================================================
        # Clean invalid numerical values
        # ==================================================

        df = df.replace(

            [

                float("inf"),

                -float("inf"),

            ],

            None,

        )



        return df