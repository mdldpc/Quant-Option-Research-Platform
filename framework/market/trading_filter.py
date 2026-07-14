"""
Market data cleaning.

All snapshot builders should pass raw market data
through TradingFilter before any Greeks calculation.
"""

from __future__ import annotations

import pandas as pd

from framework.market.market_config import (
    REMOVE_AFTER_CLOSE,
    REMOVE_CALL_AUCTION,
    REMOVE_CROSSED_QUOTES,
    REMOVE_INVALID_GREEKS,
    REMOVE_LUNCH_BREAK,
    REMOVE_NEGATIVE_IV,
    REMOVE_NEGATIVE_PRICE,
    REMOVE_PRE_OPEN,
    REMOVE_ZERO_VOLUME,
)

from framework.market.session import MarketSession


class TradingFilter:

    @staticmethod
    def remove_invalid_session(
        df: pd.DataFrame,
        time_column: str = "updateTime",
    ) -> pd.DataFrame:

        if time_column not in df.columns:
            return df.copy()

        session = df[time_column].apply(
            MarketSession.session_name
        )

        keep = pd.Series(True, index=df.index)

        if REMOVE_PRE_OPEN:
            keep &= session != "pre_open"

        if REMOVE_CALL_AUCTION:
            keep &= session != "call_auction"

        if REMOVE_LUNCH_BREAK:
            keep &= session != "lunch_break"

        if REMOVE_AFTER_CLOSE:
            keep &= session != "after_close"

        return df.loc[keep].copy()

    @staticmethod
    def remove_zero_volume(
        df: pd.DataFrame,
        volume_column: str = "volume",
    ) -> pd.DataFrame:

        if not REMOVE_ZERO_VOLUME:
            return df.copy()

        if volume_column not in df.columns:
            return df.copy()

        return df[df[volume_column] > 0].copy()

    @staticmethod
    def remove_negative_price(
        df: pd.DataFrame,
        price_columns=None,
    ) -> pd.DataFrame:

        if not REMOVE_NEGATIVE_PRICE:
            return df.copy()

        if price_columns is None:
            price_columns = [
                "lastPrice",
                "BP1",
                "AP1",
            ]

        keep = pd.Series(True, index=df.index)

        for col in price_columns:
            if col not in df.columns:
                continue

            keep &= df[col] >= 0

        return df.loc[keep].copy()

    @staticmethod
    def remove_crossed_quotes(
        df: pd.DataFrame,
        bid_column="BP1",
        ask_column="AP1",
    ) -> pd.DataFrame:

        if not REMOVE_CROSSED_QUOTES:
            return df.copy()

        if bid_column not in df.columns:
            return df.copy()

        if ask_column not in df.columns:
            return df.copy()

        return df[df[bid_column] <= df[ask_column]].copy()

    @staticmethod
    def remove_invalid_iv(
        df: pd.DataFrame,
        iv_column="iv",
    ) -> pd.DataFrame:

        if not REMOVE_NEGATIVE_IV:
            return df.copy()

        if iv_column not in df.columns:
            return df.copy()

        return df[df[iv_column] >= 0].copy()

    @staticmethod
    def remove_invalid_greeks(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if not REMOVE_INVALID_GREEKS:
            return df.copy()

        greek_columns = [
            "delta",
            "gamma",
            "vega",
            "theta",
        ]

        keep = pd.Series(True, index=df.index)

        for col in greek_columns:
            if col not in df.columns:
                continue

            keep &= df[col].notna()

        return df.loc[keep].copy()

    @classmethod
    def clean(
        cls,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        x = df.copy()

        x = cls.remove_invalid_session(x)
        x = cls.remove_zero_volume(x)
        x = cls.remove_negative_price(x)
        x = cls.remove_crossed_quotes(x)
        x = cls.remove_invalid_iv(x)
        x = cls.remove_invalid_greeks(x)

        return x.reset_index(drop=True)