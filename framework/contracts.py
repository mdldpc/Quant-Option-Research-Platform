"""
=========================================================
Framework Contracts
=========================================================

Common data contracts shared by all strategy modules.
"""

from dataclasses import dataclass
from pathlib import Path


# =========================================================
# Strategy Dataset Contract
# =========================================================

@dataclass
class StrategyDatasetContract:
    """
    Common metadata that every strategy dataset should expose.
    """

    strategy_name: str

    dataset_path: Path

    preview_path: Path

    report_path: Path

    trade_count: int

    start_date: str

    end_date: str

    version: str = "v2"


# =========================================================
# Backtest Contract
# =========================================================

@dataclass
class BacktestContract:
    """
    Common summary returned by every strategy backtest.
    """

    strategy_name: str

    trade_count: int

    win_rate: float

    cumulative_return: float

    max_drawdown: float

    report_path: Path


# =========================================================
# Risk Contract
# =========================================================

@dataclass
class RiskContract:
    """
    Common summary produced by the risk engine.
    """

    strategy_name: str

    observation_count: int

    medium_risk_count: int

    high_risk_count: int

    report_path: Path