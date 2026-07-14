"""
Trading Calendar Configuration

Central place to manage abnormal trading dates.
"""

ABNORMAL_TRADING_DATES = {
    20260505,
}


def is_abnormal_trading_date(trade_date: int) -> bool:
    return int(trade_date) in ABNORMAL_TRADING_DATES