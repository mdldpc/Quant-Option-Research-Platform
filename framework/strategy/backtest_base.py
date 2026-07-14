from pathlib import Path
from abc import ABC, abstractmethod
import pandas as pd

from framework.strategy.contracts import BacktestResult
from framework.strategy.backtest_engine import (
    compute_equity_curve,
    summarize_backtest,
    write_backtest_report,
)


class BaseBacktester(ABC):
    strategy_name = "base_strategy"
    display_name = "Base Strategy"

    def __init__(self, trades: pd.DataFrame):
        self.trades = trades.copy()

    @abstractmethod
    def run(self) -> pd.DataFrame:
        raise NotImplementedError

    def finalize(
        self,
        out: pd.DataFrame,
        report_path: Path,
        trades_path: Path,
    ) -> BacktestResult:
        out = compute_equity_curve(out)

        trades_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.parent.mkdir(parents=True, exist_ok=True)

        out.to_csv(trades_path, index=False, encoding="utf-8-sig")

        write_backtest_report(
            strategy_name=self.display_name,
            trades=out,
            report_path=report_path,
        )

        stats = summarize_backtest(out)

        return BacktestResult(
            strategy_name=self.strategy_name,
            total_trades=stats["total_trades"],
            completed_trades=stats["completed_trades"],
            skipped_trades=stats["skipped_trades"],
            win_rate=stats["win_rate"],
            final_equity=stats["final_equity"],
            max_drawdown=stats["max_drawdown"],
            average_return=stats["average_return"],
            report_path=report_path,
            trades_path=trades_path,
            status="success",
            message=f"{self.display_name} backtest completed.",
        )