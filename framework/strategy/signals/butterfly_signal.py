import pandas as pd

from framework.strategy.signals.base import (
    BaseSignalGenerator,
)


class ButterflySignalGenerator(BaseSignalGenerator):

    signal_name = "butterfly_iv_signal_v1_2"


    def __init__(
        self,
        max_holding_days=10,
        entry_zscore=None,
        entry_threshold=None,
        exit_zscore=0.0,
    ):

        """
        Parameters
        ----------
        max_holding_days:
            Maximum holding period

        entry_zscore:
            Original parameter.
            Kept for backward compatibility.

        entry_threshold:
            Unified sensitivity parameter.

            Example:
                -2.0
                -1.5
                -1.0

            Entry condition:
                butterfly_zscore <= entry_threshold

        exit_zscore:
            Exit condition.
        """


        self.max_holding_days = (
            max_holding_days
        )


        # ----------------------------------
        # Unified threshold handling
        # ----------------------------------

        if entry_threshold is not None:

            self.entry_zscore = (
                entry_threshold
            )

        elif entry_zscore is not None:

            self.entry_zscore = (
                entry_zscore
            )

        else:

            self.entry_zscore = -1.0



        self.exit_zscore = exit_zscore



    def generate(
        self,
        dataset: pd.DataFrame,
    ) -> pd.DataFrame:


        df = dataset.copy()



        # =====================================
        # Convert intraday snapshots
        # into daily butterfly feature
        # =====================================

        df = (
            df.groupby(
                "trade_date",
                as_index=False,
            )
            .agg(
                butterfly_price=(
                    "butterfly_price",
                    "mean",
                ),
            )
        )



        df["trade_date_dt"] = pd.to_datetime(
            df["trade_date"].astype(str)
        )


        df = (
            df
            .sort_values(
                "trade_date_dt"
            )
            .reset_index(drop=True)
        )



        # =====================================
        # Rolling z-score
        # =====================================

        df["butterfly_mean"] = (
            df["butterfly_price"]
            .rolling(20)
            .mean()
        )


        df["butterfly_std"] = (
            df["butterfly_price"]
            .rolling(20)
            .std()
        )


        df["butterfly_zscore"] = (

            (
                df["butterfly_price"]
                -
                df["butterfly_mean"]
            )

            /

            df["butterfly_std"]

        )



        trades = []


        in_position = False

        entry_idx = None



        for i,row in df.iterrows():



            # =================================
            # Entry
            # =================================

            if not in_position:


                if (
                    row["butterfly_zscore"]
                    <= self.entry_zscore
                ):

                    in_position = True

                    entry_idx = i


                continue



            # =================================
            # Holding
            # =================================

            entry = df.iloc[
                entry_idx
            ]


            holding_days = (
                i - entry_idx
            )


            exit_reason = None



            # zscore recovery

            if (
                row["butterfly_zscore"]
                >= self.exit_zscore
            ):

                exit_reason = (
                    "zscore_exit"
                )



            # max holding

            if (
                holding_days
                >= self.max_holding_days
            ):

                exit_reason = (
                    "max_holding"
                )



            # last observation

            if (
                i == len(df)-1
            ):

                exit_reason = (
                    "end_of_data"
                )



            if exit_reason is not None:


                trades.append(

                    {

                        "entry_date":
                            entry["trade_date"],


                        "exit_date":
                            row["trade_date"],


                        "holding_days":
                            holding_days,


                        "entry_signal_score":
                            entry[
                                "butterfly_zscore"
                            ],


                        "exit_signal_score":
                            row[
                                "butterfly_zscore"
                            ],


                        "entry_butterfly_zscore":
                            entry[
                                "butterfly_zscore"
                            ],


                        "exit_butterfly_zscore":
                            row[
                                "butterfly_zscore"
                            ],


                        "exit_reason":
                            exit_reason,

                    }

                )


                in_position = False

                entry_idx = None



        return pd.DataFrame(
            trades
        )