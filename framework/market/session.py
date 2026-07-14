"""
Market session utilities.

All session classification should go through MarketSession.
Do not hard-code trading hours elsewhere.
"""

from framework.market.market_config import (
    CALL_AUCTION,
    CONTINUOUS_AM,
    CONTINUOUS_PM,
    LUNCH_BREAK,
    PRE_OPEN,
    AFTER_CLOSE,
)


class MarketSession:

    @staticmethod
    def normalize_time(time_value) -> int:
        """
        Convert time value to integer HHMMSS.

        Supported:
            104553
            "104553"
            "10:45:53"
            "10:45:53.500"
        """
        if time_value is None:
            return -1

        s = str(time_value).strip()

        if not s:
            return -1

        if ":" in s:
            main = s.split(".")[0]
            parts = main.split(":")

            if len(parts) >= 3:
                h = int(parts[0])
                m = int(parts[1])
                sec = int(parts[2])
                return h * 10000 + m * 100 + sec

        return int(float(s))

    @staticmethod
    def _in_session(time_value, session) -> bool:
        """
        Inclusive start, exclusive end.
        """
        t = MarketSession.normalize_time(time_value)
        return session.start <= t < session.end

    @classmethod
    def session_name(cls, time_value) -> str:
        if cls._in_session(time_value, PRE_OPEN):
            return PRE_OPEN.name

        if cls._in_session(time_value, CALL_AUCTION):
            return CALL_AUCTION.name

        if cls._in_session(time_value, CONTINUOUS_AM):
            return CONTINUOUS_AM.name

        if cls._in_session(time_value, LUNCH_BREAK):
            return LUNCH_BREAK.name

        if cls._in_session(time_value, CONTINUOUS_PM):
            return CONTINUOUS_PM.name

        if cls._in_session(time_value, AFTER_CLOSE):
            return AFTER_CLOSE.name

        return "unknown"

    @classmethod
    def is_call_auction(cls, time_value) -> bool:
        return cls.session_name(time_value) == CALL_AUCTION.name

    @classmethod
    def is_pre_open(cls, time_value) -> bool:
        return cls.session_name(time_value) == PRE_OPEN.name

    @classmethod
    def is_lunch_break(cls, time_value) -> bool:
        return cls.session_name(time_value) == LUNCH_BREAK.name

    @classmethod
    def is_after_close(cls, time_value) -> bool:
        return cls.session_name(time_value) == AFTER_CLOSE.name

    @classmethod
    def is_continuous(cls, time_value) -> bool:
        return cls.session_name(time_value) in (
            CONTINUOUS_AM.name,
            CONTINUOUS_PM.name,
        )

    @classmethod
    def is_tradable(cls, time_value) -> bool:
        return cls.is_continuous(time_value)

    @classmethod
    def is_market_open(cls, time_value) -> bool:
        return cls.session_name(time_value) in (
            CALL_AUCTION.name,
            CONTINUOUS_AM.name,
            CONTINUOUS_PM.name,
        )

    @classmethod
    def is_valid_snapshot_time(cls, time_value) -> bool:
        return cls.is_continuous(time_value)