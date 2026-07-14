from pathlib import Path

from framework.strategy.trade_constructor import (
    StrangleTradeConstructor,
    ButterflyTradeConstructor,
    CalendarTradeConstructor,
)

from framework.strategy.backtesters.strangle import StrangleBacktester
from framework.strategy.backtesters.butterfly import ButterflyBacktester
from framework.strategy.backtesters.calendar import CalendarBacktester


STRATEGIES = {
    "long_atm_strangle": {
        "constructor": StrangleTradeConstructor,
        "backtester": StrangleBacktester,
        "snapshot": Path("research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet"),
        "trade_output": Path("research/exports/option_strategy_backtest_strangle_v1_1.csv"),
        "backtest_output": Path("research/exports/strangle_strategy_backtest_v1_1.csv"),
        "backtest_report": Path("research/reports/strangle_strategy_backtest_v1_1_report.txt"),
    },
    "long_call_butterfly": {
        "constructor": ButterflyTradeConstructor,
        "backtester": ButterflyBacktester,
        "snapshot": Path("research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet"),
        "trade_output": Path("research/exports/option_strategy_backtest_butterfly_v1_1.csv"),
        "backtest_output": Path("research/exports/butterfly_strategy_backtest_v1_1.csv"),
        "backtest_report": Path("research/reports/butterfly_strategy_backtest_v1_1_report.txt"),
    },
    "calendar_spread": {
        "constructor": CalendarTradeConstructor,
        "backtester": CalendarBacktester,
        "snapshot": Path("research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet"),
        "trade_output": Path("research/exports/option_strategy_backtest_calendar_v1_1.csv"),
        "backtest_output": Path("research/exports/calendar_strategy_backtest_v1_1.csv"),
        "backtest_report": Path("research/reports/calendar_strategy_backtest_v1_1_report.txt"),
    },
}


def list_strategies():
    return list(STRATEGIES.keys())


def get_strategy(strategy_name: str):
    if strategy_name not in STRATEGIES:
        raise KeyError(f"Unknown strategy: {strategy_name}")
    return STRATEGIES[strategy_name]