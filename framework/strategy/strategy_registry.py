from pathlib import Path


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

from framework.strategy.signals.calendar_signal import (
    CalendarSignalGenerator,
)

from framework.strategy.signals.iv_signal import (
    IVSignalGenerator,
)


from framework.strategy.signals.butterfly_signal import (
    ButterflySignalGenerator,
)

STRATEGIES = {
    "long_atm_strangle": {

        "signal_generator": IVSignalGenerator,

        "signal_score_column":
            "entry_signal_score",

        "signal_direction":
            "positive",

        "signal_input": Path(
            "research/signals/daily_signal_features.parquet"
        ),

        "constructor": StrangleTradeConstructor,

        "backtester": StrangleBacktester,

        "capacity":
            1,

        "snapshot": Path(
            "research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet"
        ),

        "trade_output": Path(
            "research/exports/option_strategy_backtest_strangle_v1_1.csv"
        ),

        "backtest_output": Path(
            "research/exports/strangle_strategy_backtest_v1_1.csv"
        ),

        "backtest_report": Path(
            "research/reports/strangle_strategy_backtest_v1_1_report.txt"
        ),
    },
    "long_call_butterfly": {

        "signal_generator": ButterflySignalGenerator,

        "signal_score_column":
            "entry_butterfly_zscore",

        "signal_direction":
            "negative",

        "signal_input": Path(
            "research/datasets/butterfly_dataset_2026H1_v1_1.parquet"
        ),

        "constructor": ButterflyTradeConstructor,

        "backtester": ButterflyBacktester,

        "capacity":
            1,

        "snapshot": Path(
            "research/datasets/butterfly_daily_snapshot_2026H1_v1_1.parquet"
        ),

        "trade_output": Path(
            "research/exports/option_strategy_backtest_butterfly_v1_1.csv"
        ),

        "backtest_output": Path(
            "research/exports/butterfly_strategy_backtest_v1_1.csv"
        ),

        "backtest_report": Path(
            "research/reports/butterfly_strategy_backtest_v1_1_report.txt"
        ),
    },
    "calendar_spread": {

        "signal_generator": CalendarSignalGenerator,

        "signal_score_column":
            "entry_iv_spread_zscore",

        "signal_direction":
            "negative",

        "signal_input": Path(
            "research/datasets/calendar_spread_dataset_2026H1_v1_1.parquet"
        ),

        "constructor": CalendarTradeConstructor,

        "backtester": CalendarBacktester,

        "capacity":
            1,

        "snapshot": Path(
            "research/datasets/calendar_daily_snapshot_2026H1_v1_1.parquet"
        ),

        "trade_output": Path(
            "research/exports/option_strategy_backtest_calendar_v1_1.csv"
        ),

        "backtest_output": Path(
            "research/exports/calendar_strategy_backtest_v1_1.csv"
        ),

        "backtest_report": Path(
            "research/reports/calendar_strategy_backtest_v1_1_report.txt"
        ),
    },
}


def list_strategies():
    return list(STRATEGIES.keys())


def get_strategy(strategy_name: str):
    if strategy_name not in STRATEGIES:
        raise KeyError(f"Unknown strategy: {strategy_name}")
    return STRATEGIES[strategy_name]