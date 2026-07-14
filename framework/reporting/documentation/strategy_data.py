"""
Central strategy registry.

All strategy documentation records are imported from individual
strategy definition files.

This file should not contain detailed strategy descriptions.
"""

from framework.reporting.documentation.strategy_database import (
    LONG_ATM_STRANGLE,
    LONG_CALL_BUTTERFLY,
    CALENDAR_SPREAD,
)


STRATEGIES = {

    "long_atm_strangle":
        LONG_ATM_STRANGLE,

    "long_call_butterfly":
        LONG_CALL_BUTTERFLY,

    "calendar_spread":
        CALENDAR_SPREAD,

}


def get_strategy(strategy_key: str):

    return STRATEGIES[strategy_key]


def get_all_strategies():

    return list(STRATEGIES.values())