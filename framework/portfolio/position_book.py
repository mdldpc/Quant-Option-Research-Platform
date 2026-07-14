"""
Portfolio Position Book

Maintains the current portfolio positions.

This module does not calculate PnL.
It only stores and manages positions.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict

import pandas as pd


@dataclass
class Position:

    trade_id: int

    strategy: str

    quantity: int

    entry_date: int

    entry_price: float

    current_price: float

    market_value: float

    status: str = "open"


class PositionBook:

    def __init__(self):

        self._positions: Dict[int, Position] = {}

    def add(
        self,
        position: Position,
    ):

        self._positions[position.trade_id] = position

    def remove(
        self,
        trade_id: int,
    ):

        self._positions.pop(trade_id, None)

    def exists(
        self,
        trade_id: int,
    ) -> bool:

        return trade_id in self._positions

    def update_price(
        self,
        trade_id: int,
        current_price: float,
    ):

        if trade_id not in self._positions:
            raise KeyError(f"Unknown trade_id: {trade_id}")

        p = self._positions[trade_id]

        p.current_price = float(current_price)
        p.market_value = p.quantity * p.current_price

    def get(
        self,
        trade_id: int,
    ) -> Position | None:

        return self._positions.get(trade_id)

    def positions(self):

        return list(self._positions.values())

    def size(self) -> int:

        return len(self._positions)

    def market_value(self) -> float:

        return sum(
            p.market_value
            for p in self._positions.values()
        )

    def summary(self) -> pd.DataFrame:

        if not self._positions:
            return pd.DataFrame()

        rows = [
            asdict(x)
            for x in self._positions.values()
        ]

        return pd.DataFrame(rows)

    def clear(self):

        self._positions.clear()