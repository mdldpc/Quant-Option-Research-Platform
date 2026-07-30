from pathlib import Path

import pandas as pd
import numpy as np


from framework.strategy.trade_constructor import (
    StrangleTradeConstructor,
    ButterflyTradeConstructor,
    CalendarTradeConstructor,
)


from framework.strategy.backtesters.strangle import (
    StrangleBacktester,
)

from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)

from framework.strategy.backtesters.calendar import (
    CalendarBacktester,
)



class SignalBacktestSensitivity:


    def __init__(
        self,
        config: dict,
    ):

        self.config = config



    # --------------------------------------------------
    # Generate signals under threshold
    # --------------------------------------------------

    def generate_signals(
        self,
        threshold,
    ):

        df = pd.read_parquet(
            self.config["signal_input"]
        )


        generator = self.config[
            "signal_generator"
        ](
            entry_threshold=threshold
        )


        signals = generator.generate(
            df
        )


        return signals



    # --------------------------------------------------
    # Backtest one threshold
    # --------------------------------------------------

    def run_threshold(
        self,
        threshold,
    ):


        signals = self.generate_signals(
            threshold
        )


        if signals.empty:

            return {

                "threshold": threshold,

                "trades":0,

                "win_rate":np.nan,

                "average_return":np.nan,

                "profit_factor":np.nan,

            }



        snapshot = pd.read_parquet(
            self.config["snapshot"]
        )


        constructor = self.config[
            "constructor"
        ](
            snapshot
        )


        trades = constructor.build_all(
            signals
        )


        backtester = self.config[
            "backtester"
        ](
            trades
        )


        result = backtester.backtest(
            report_path=Path(
                "research/reports/"
                f"{self.config['backtester'].strategy_name}_"
                f"sensitivity_{threshold}_report.txt"
            ),

            trades_path=Path(
                "research/reports/"
                f"{self.config['backtester'].strategy_name}_"
                f"sensitivity_{threshold}_trades.csv"
            ),
        )

        return {

            "threshold":
                threshold,


            "trades":
                result.total_trades,


            "win_rate":
                result.win_rate,


            "average_return":
                result.average_return,


            "profit_factor":
                getattr(
                    result,
                    "profit_factor",
                    np.nan
                ),


            "final_equity":
                result.final_equity,


            "max_drawdown":
                result.max_drawdown,

        }



    # --------------------------------------------------
    # Run sensitivity
    # --------------------------------------------------

    def analyze(
        self,
        thresholds,
    ):


        rows=[]


        for t in thresholds:

            print(
                "Testing threshold:",
                t
            )


            rows.append(
                self.run_threshold(t)
            )


        return pd.DataFrame(rows)