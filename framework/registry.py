"""
=========================================================
Strategy Registry
=========================================================

Central registry for all trading strategies.

Responsibilities

1. Register available strategies.

2. Query strategy information.

3. Provide builder / runner lookup.

Future strategy builders should register themselves here.
"""

from config.strategy_config import STRATEGY_REGISTRY

from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)

from framework.strategy.backtesters.calendar import (
    CalendarBacktester,
)

from framework.strategy.backtesters.strangle import (
    StrangleBacktester,
)

STRATEGY_CLASS_REGISTRY = {

    "long_call_butterfly":
        ButterflyBacktester,


    "calendar_spread":
        CalendarBacktester,


    "long_atm_strangle":
        StrangleBacktester,

}

def list_all_strategies():
    """
    Return all registered strategy names.
    """
    return list(STRATEGY_REGISTRY.keys())


def enabled_strategies():
    """
    Return enabled strategies only.
    """
    return [
        name
        for name, cfg in STRATEGY_REGISTRY.items()
        if cfg["enabled"]
    ]


def strategy_status(strategy_name):
    """
    Return strategy status.
    """

    if strategy_name not in STRATEGY_REGISTRY:
        raise KeyError(strategy_name)

    return STRATEGY_REGISTRY[strategy_name]["status"]


def is_enabled(strategy_name):

    if strategy_name not in STRATEGY_REGISTRY:
        raise KeyError(strategy_name)

    return STRATEGY_REGISTRY[strategy_name]["enabled"]


def get_strategy(strategy_name):

    if strategy_name not in STRATEGY_REGISTRY:
        raise KeyError(strategy_name)

    return STRATEGY_REGISTRY[strategy_name]

def get_backtester(strategy_name):

    if strategy_name not in STRATEGY_CLASS_REGISTRY:
        raise KeyError(
            f"No backtester registered for {strategy_name}"
        )


    return STRATEGY_CLASS_REGISTRY[strategy_name]