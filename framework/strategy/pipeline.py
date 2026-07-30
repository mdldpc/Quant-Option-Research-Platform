from pathlib import Path
import pandas as pd


from framework.strategy.trade_constructor import (
    StrangleTradeConstructor,
    ButterflyTradeConstructor,
    CalendarTradeConstructor,
)


from framework.strategy.strategy_registry import (
    get_strategy,
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



CONSTRUCTOR_MAP = {

    "long_atm_strangle":
        StrangleTradeConstructor,

    "long_call_butterfly":
        ButterflyTradeConstructor,

    "calendar_spread":
        CalendarTradeConstructor,

}



BACKTESTER_MAP = {

    "long_atm_strangle":
        StrangleBacktester,

    "long_call_butterfly":
        ButterflyBacktester,

    "calendar_spread":
        CalendarBacktester,

}



def run_strategy_pipeline(
    strategy_name,
    signals,
):

    """
    Common strategy execution pipeline.

    Input:
        strategy_name
        executable signals

    Flow:

        signals
            |
            v
        snapshot
            |
            v
        trade constructor
            |
            v
        backtester

    """



    config = get_strategy(
        strategy_name
    )


    # -----------------------------
    # Load snapshot
    # -----------------------------

    snapshot = pd.read_parquet(
        config["snapshot_input"]
    )



    # -----------------------------
    # Construct trades
    # -----------------------------


    constructor_class = (
        CONSTRUCTOR_MAP[
            strategy_name
        ]
    )


    constructor = constructor_class(
        snapshot
    )


    trades = constructor.build_all(
        signals
    )



    trades = pd.DataFrame(
        trades
    )



    # -----------------------------
    # Backtest
    # -----------------------------


    backtester_class = (
        BACKTESTER_MAP[
            strategy_name
        ]
    )


    backtester = backtester_class(
        trades
    )


    return backtester