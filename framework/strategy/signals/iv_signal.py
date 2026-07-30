import pandas as pd

from framework.strategy.signals.base import (
    BaseSignalGenerator,
)


class IVSignalGenerator(BaseSignalGenerator):

    signal_name = "iv_signal_v1_2"



    def __init__(
        self,
        max_holding_days=10,
        entry_threshold=None,
        exit_score_threshold=40,
    ):

        """
        Parameters
        ----------
        max_holding_days:
            Maximum holding period.


        entry_threshold:
            Unified sensitivity parameter.

            Example:

                60
                70
                80
                90


            Entry condition:

                signal_score >= entry_threshold


        exit_score_threshold:
            Exit when signal score falls below this value.
        """


        self.max_holding_days = (
            max_holding_days
        )


        if entry_threshold is None:

            # Original strategy behavior
            self.entry_threshold = 80

        else:

            self.entry_threshold = (
                entry_threshold
            )


        self.exit_score_threshold = (
            exit_score_threshold
        )



    def generate(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:


        df = df.copy()



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



        trades = []


        in_position = False

        entry_idx = None



        for i,row in df.iterrows():



            # =================================
            # Entry
            # =================================

            if not in_position:


                if (

                    row["signal_score"]

                    >=

                    self.entry_threshold

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

                i
                -
                entry_idx

            )


            exit_reason = None



            # signal deterioration

            if (

                row["signal_score"]

                <=

                self.exit_score_threshold

            ):

                exit_reason = (
                    "score_exit"
                )



            # max holding

            if (

                holding_days

                >=

                self.max_holding_days

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
                            entry[
                                "trade_date"
                            ],


                        "exit_date":
                            row[
                                "trade_date"
                            ],



                        "holding_days":
                            holding_days,



                        "entry_signal_score":
                            entry[
                                "signal_score"
                            ],



                        "exit_signal_score":
                            row[
                                "signal_score"
                            ],



                        "entry_near_iv":
                            entry[
                                "near_iv"
                            ],



                        "exit_near_iv":
                            row[
                                "near_iv"
                            ],



                        "entry_term_slope":
                            entry[
                                "term_slope_next_near"
                            ],



                        "exit_term_slope":
                            row[
                                "term_slope_next_near"
                            ],



                        "entry_iv_zscore":
                            entry[
                                "near_iv_zscore"
                            ],



                        "exit_iv_zscore":
                            row[
                                "near_iv_zscore"
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