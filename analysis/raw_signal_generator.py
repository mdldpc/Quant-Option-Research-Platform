"""
Raw Signal Generator

Generate raw entry opportunities.

Important:
    This module DOES NOT handle:
        - position state
        - holding period
        - exits
        - overlap restriction

It only answers:

"On which dates would the strategy want to enter?"
"""


import pandas as pd



class RawSignalGenerator:



    def __init__(
        self,
        strategy_name,
    ):

        self.strategy_name = strategy_name



    # ==================================================
    # Main interface
    # ==================================================

    def generate(
        self,
        df: pd.DataFrame,
    ):


        if self.strategy_name == "long_atm_strangle":

            return self._strangle(df)



        elif self.strategy_name == "long_call_butterfly":

            return self._butterfly(df)



        elif self.strategy_name == "calendar_spread":

            return self._calendar(df)



        else:

            raise ValueError(
                f"Unknown strategy: {self.strategy_name}"
            )



    # ==================================================
    # Long ATM Strangle
    # ==================================================

    def _strangle(
        self,
        df,
    ):


        out = df.copy()


        out = (
            out
            .reset_index(drop=True)
        )

        # ==================================================
        # Ensure required signal columns exist
        # ==================================================

        required_defaults = {

            "signal_score":
                out["long_signal"].astype(float),

            "trade_date":
                range(len(out)),

            "near_iv":
                None,

            "term_slope_next_near":
                None,

            "near_iv_zscore":
                None,
        }


        for col, default_value in required_defaults.items():

            if col not in out.columns:
                out[col] = default_value

        trades = []


        entry_candidates = out[
            out["long_signal"] == 1
        ]


        for entry_idx in entry_candidates.index:


            exit_idx = None


            for i in range(
                entry_idx + 1,
                len(out)
            ):


                holding_days = (
                    i - entry_idx
                )


                # same exit logic as IVSignalGenerator
                if (
                    out.loc[i, "signal_score"]
                    <= 40
                ):

                    exit_idx = i
                    break



                if holding_days >= 10:

                    exit_idx = i
                    break



            if exit_idx is None:

                exit_idx = len(out)-1



            entry = out.loc[
                entry_idx
            ]


            exit_ = out.loc[
                exit_idx
            ]



            trades.append(
                {


                    "trade_date":
                        entry["trade_date"],


                    "exit_date":
                        exit_["trade_date"],


                    "entry_idx":
                        entry_idx,


                    "exit_idx":
                        exit_idx,


                    "signal_score":
                        entry["signal_score"],


                    "near_iv":
                        entry["near_iv"],


                    "term_slope_next_near":
                        entry["term_slope_next_near"],


                    "near_iv_zscore":
                        entry["near_iv_zscore"],


                }
            )


        return pd.DataFrame(trades)


    # ==================================================
    # Long Call Butterfly
    # ==================================================

    def _butterfly(
        self,
        df,
    ):


        daily = (

            df

            .groupby(
                "trade_date",
                as_index=False,
            )

            .agg(
                butterfly_price=
                (
                    "butterfly_price",
                    "mean",
                )
            )

        )



        daily = daily.sort_values(
            "trade_date"
        ).reset_index(
            drop=True
        )



        daily["mean"] = (

            daily["butterfly_price"]

            .rolling(20)
            .mean()

        )


        daily["std"] = (

            daily["butterfly_price"]

            .rolling(20)
            .std()

        )



        daily["butterfly_zscore"] = (

            (
                daily["butterfly_price"]
                -
                daily["mean"]
            )

            /

            daily["std"]

        )



        signals = daily[
            daily["butterfly_zscore"]
            <= -1
        ].copy()



        signals["entry_idx"] = (
            signals.index
        )


        trades = []


        for entry_idx in signals["entry_idx"]:


            exit_idx = None


            for i in range(
                entry_idx + 1,
                len(daily)
            ):

                holding_days = (
                    i - entry_idx
                )


                # exit rule
                # butterfly mean reversion
                if (
                    daily.loc[i, "butterfly_zscore"]
                    >= 0
                ):

                    exit_idx = i
                    break


                if holding_days >= 10:

                    exit_idx = i
                    break



            if exit_idx is None:

                exit_idx = len(daily)-1



            trades.append(
                {

                    "trade_date":
                        daily.loc[
                            entry_idx,
                            "trade_date"
                        ],


                    "exit_date":
                        daily.loc[
                            exit_idx,
                            "trade_date"
                        ],


                    "entry_idx":
                        entry_idx,


                    "exit_idx":
                        exit_idx,


                    # keep signal information
                    "butterfly_price":
                        daily.loc[
                            entry_idx,
                            "butterfly_price"
                        ],


                    "butterfly_zscore":
                        daily.loc[
                            entry_idx,
                            "butterfly_zscore"
                        ],


                    "mean":
                        daily.loc[
                            entry_idx,
                            "mean"
                        ],


                    "std":
                        daily.loc[
                            entry_idx,
                            "std"
                        ],

                }
            )


        return pd.DataFrame(trades)



    # ==================================================
    # Calendar Spread
    # ==================================================

    def _calendar(
        self,
        df,
    ):


        daily = (

            df

            .groupby(
                "trade_date",
                as_index=False,
            )

            .agg(
                iv_spread=
                (
                    "iv_spread",
                    "mean",
                )
            )

        )



        daily = daily.sort_values(
            "trade_date"
        ).reset_index(
            drop=True
        )



        daily["mean"] = (

            daily["iv_spread"]

            .rolling(20)
            .mean()

        )


        daily["std"] = (

            daily["iv_spread"]

            .rolling(20)
            .std()

        )



        daily["iv_spread_zscore"] = (

            (
                daily["iv_spread"]
                -
                daily["mean"]
            )

            /

            daily["std"]

        )



        signals = daily[
            daily["iv_spread_zscore"]
            <= -1
        ].copy()



        signals["entry_idx"] = (
            signals.index
        )


        trades = []


        for entry_idx in signals["entry_idx"]:


            exit_idx = None


            for i in range(
                entry_idx + 1,
                len(daily)
            ):


                holding_days = (
                    i - entry_idx
                )


                # IV spread mean reversion
                if (
                    daily.loc[i, "iv_spread_zscore"]
                    >= 0
                ):

                    exit_idx = i
                    break



                if holding_days >= 10:

                    exit_idx = i
                    break



            if exit_idx is None:

                exit_idx = len(daily)-1



            trades.append(
                {

                    "trade_date":
                        daily.loc[
                            entry_idx,
                            "trade_date"
                        ],

                    "exit_date":
                        daily.loc[
                            exit_idx,
                            "trade_date"
                        ],

                    "entry_idx":
                        entry_idx,

                    "exit_idx":
                        exit_idx,

                    "iv_spread":
                        daily.loc[
                            entry_idx,
                            "iv_spread"
                        ],

                    "iv_spread_zscore":
                        daily.loc[
                            entry_idx,
                            "iv_spread_zscore"
                        ],


                    "mean":
                        daily.loc[
                            entry_idx,
                            "mean"
                        ],


                    "std":
                        daily.loc[
                            entry_idx,
                            "std"
                        ],
                        
                }
            )


        return pd.DataFrame(trades)