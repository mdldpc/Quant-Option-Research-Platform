from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class BacktestResult:
    """
    Standard output of a strategy backtest.

    Every strategy backtester should return one BacktestResult.
    """

    strategy_name: str

    total_trades: int

    completed_trades: int

    skipped_trades: int

    win_rate: float

    final_equity: float

    max_drawdown: float

    average_return: float

    report_path: Optional[Path] = None

    trades_path: Optional[Path] = None

    equity_path: Optional[Path] = None

    status: str = "success"

    message: str = ""