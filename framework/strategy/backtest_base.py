from pathlib import Path
from abc import ABC, abstractmethod

import pandas as pd

from framework.strategy.contracts import BacktestResult

from framework.strategy.backtest_engine import (
    compute_equity_curve,
    write_backtest_report,
)


from analysis.backtest_analysis import (
    BacktestAnalyzer,
)

class BaseBacktester(ABC):
    """
    Base class for all strategy backtesters.

    Workflow:

    run()
        |
        v
    trade dataframe
        |
        v
    finalize()
        |
        v
    BacktestResult

    """

    strategy_name = "base_strategy"

    display_name = "Base Strategy"


    def __init__(
        self,
        trades: pd.DataFrame,
    ):
        self.trades = trades.copy()



    @abstractmethod
    def run(self) -> pd.DataFrame:
        """
        Execute strategy-specific backtest logic.

        Returns
        -------
        pd.DataFrame
            Trade-level backtest results.
        """

        raise NotImplementedError



    def backtest(
        self,
        report_path: Path,
        trades_path: Path,
    ) -> BacktestResult:
        """
        Unified backtest entry point.

        Executes:

        run()
          |
          v
        finalize()

        Returns
        -------
        BacktestResult
        """

        out = self.run()


        return self.finalize(
            out=out,
            report_path=report_path,
            trades_path=trades_path,
        )



    def finalize(
        self,
        out: pd.DataFrame,
        report_path: Path,
        trades_path: Path,
    ) -> BacktestResult:
        """
        Convert trade dataframe into
        standardized BacktestResult.
        """


        out = compute_equity_curve(
            out
        )


        trades_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )



        out.to_csv(
            trades_path,
            index=False,
            encoding="utf-8-sig",
        )



        write_backtest_report(
            strategy_name=self.display_name,
            trades=out,
            report_path=report_path,
        )



        analyzer = BacktestAnalyzer(
            out
        )


        summary = analyzer.summary()


        performance = (
            summary["performance"]
        )


        trade_statistics = (
            summary["trade_statistics"]
        )


        return BacktestResult(

            strategy_name=self.strategy_name,


            total_trades=(
                trade_statistics["total_trades"]
            ),


            completed_trades=(
                trade_statistics["completed_trades"]
            ),


            skipped_trades=(
                trade_statistics["skipped_trades"]
            ),
            

            win_rate=(
                trade_statistics["win_rate"]
            ),


            final_equity=(
                performance["final_equity"]
            ),


            max_drawdown=(
                performance["max_drawdown"]
            ),


            average_return=(
                performance["average_return"]
            ),


            report_path=
                report_path,


            trades_path=
                trades_path,


            status="success",


            message=
                f"{self.display_name} backtest completed.",

        )