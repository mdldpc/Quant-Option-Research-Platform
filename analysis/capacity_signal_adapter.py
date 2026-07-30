import pandas as pd



class CapacitySignalAdapter:


    @staticmethod
    def adapt(
        signals: pd.DataFrame,
        strategy_name: str,
    ) -> pd.DataFrame:


        df = signals.copy()


        # ==================================================
        # Long ATM Strangle
        # ==================================================

        if strategy_name == "long_atm_strangle":


            out = pd.DataFrame()


            out["entry_date"] = (
                df["trade_date"]
            )


            out["exit_date"] = (
                df["exit_date"]
            )


            out["holding_days"] = (

                pd.to_datetime(
                    out["exit_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

                -

                pd.to_datetime(
                    out["entry_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

            ).dt.days



            out["entry_signal_score"] = (
                df["signal_score"]
            )


            # capacity stage has no future information
            # use placeholder until exit simulation

            out["exit_signal_score"] = 0



            out["entry_near_iv"] = (
                df["near_iv"]
            )


            out["exit_near_iv"] = (
                df["near_iv"]
            )


            out["entry_term_slope"] = (
                df["term_slope_next_near"]
            )


            out["exit_term_slope"] = (
                df["term_slope_next_near"]
            )


            out["entry_iv_zscore"] = (
                df["near_iv_zscore"]
            )


            out["exit_iv_zscore"] = (
                df["near_iv_zscore"]
            )


            out["exit_reason"] = (
                "capacity_exit"
            )


            return out



        # ==================================================
        # Butterfly
        # ==================================================

        elif strategy_name == "long_call_butterfly":


            out = pd.DataFrame()


            out["entry_date"] = (
                df["trade_date"]
            )


            out["exit_date"] = (
                df["exit_date"]
            )


            out["holding_days"] = (

                pd.to_datetime(
                    out["exit_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

                -

                pd.to_datetime(
                    out["entry_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

            ).dt.days


            out["entry_signal_score"] = (
                df["butterfly_zscore"]
            )


            out["exit_signal_score"] = 0


            out["entry_butterfly_zscore"] = (
                df["butterfly_zscore"]
            )


            out["exit_butterfly_zscore"] = (
                df["butterfly_zscore"]
            )


            out["exit_reason"] = (
                "capacity_exit"
            )


            return out



        # ==================================================
        # Calendar
        # ==================================================

        elif strategy_name == "calendar_spread":


            out = pd.DataFrame()


            out["entry_date"] = (
                df["trade_date"]
            )


            out["exit_date"] = (
                df["exit_date"]
            )


            out["holding_days"] = (

                pd.to_datetime(
                    out["exit_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

                -

                pd.to_datetime(
                    out["entry_date"]
                    .astype(int)
                    .astype(str),
                    format="%Y%m%d"
                )

            ).dt.days



            out["entry_signal_score"] = (
                df["iv_spread_zscore"]
            )


            out["exit_signal_score"] = 0


            out["entry_iv_spread"] = (
                df["iv_spread"]
            )


            out["exit_iv_spread"] = (
                df["iv_spread"]
            )


            out["entry_iv_spread_zscore"] = (
                df["iv_spread_zscore"]
            )


            out["exit_iv_spread_zscore"] = (
                df["iv_spread_zscore"]
            )


            out["exit_reason"] = (
                "capacity_exit"
            )


            return out



        else:

            raise ValueError(
                f"Unknown strategy: {strategy_name}"
            )