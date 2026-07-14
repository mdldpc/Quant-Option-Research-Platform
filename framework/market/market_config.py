"""
Market configuration.

All market session definitions should live here.
Business logic should never hard-code session times.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TradingSession:

    name: str

    start: int

    end: int


CALL_AUCTION = TradingSession(
    "call_auction",
    91500,
    92500,
)

CONTINUOUS_AM = TradingSession(
    "continuous_am",
    93000,
    113000,
)

LUNCH_BREAK = TradingSession(
    "lunch_break",
    113000,
    130000,
)

CONTINUOUS_PM = TradingSession(
    "continuous_pm",
    130000,
    150000,
)

AFTER_CLOSE = TradingSession(
    "after_close",
    150000,
    235959,
)

PRE_OPEN = TradingSession(
    "pre_open",
    0,
    91500,
)


REMOVE_CALL_AUCTION = True
REMOVE_AFTER_CLOSE = True
REMOVE_PRE_OPEN = True
REMOVE_LUNCH_BREAK = True

REMOVE_ZERO_VOLUME = True
REMOVE_NEGATIVE_PRICE = True
REMOVE_NEGATIVE_IV = True
REMOVE_INVALID_GREEKS = True
REMOVE_CROSSED_QUOTES = True