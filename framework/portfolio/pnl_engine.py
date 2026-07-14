"""
Portfolio PnL Engine

Calculates unrealized PnL from PositionBook.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List

import pandas as pd

from framework.portfolio.position_book import PositionBook, Position


@dataclass
class PositionPnL:
    trade_id: int
    strategy: str
    quantity: int
    entry_price: float
    current_price: float
    unrealized_pnl: float
    unrealized_return: float
    market_value: float
    status: str


@dataclass
class PortfolioPnL:
    positions: int
    total_market_value: float
    total_unrealized_pnl: float
    average_return: float


def compute_position_pnl(position: Position) -> PositionPnL:
    pnl = (position.current_price - position.entry_price) * position.quantity

    if position.entry_price == 0:
        ret = 0.0
    else:
        ret = pnl / (abs(position.entry_price) * abs(position.quantity))

    return PositionPnL(
        trade_id=position.trade_id,
        strategy=position.strategy,
        quantity=position.quantity,
        entry_price=position.entry_price,
        current_price=position.current_price,
        unrealized_pnl=pnl,
        unrealized_return=ret,
        market_value=position.market_value,
        status=position.status,
    )


class PnLEngine:

    @staticmethod
    def position_pnl_table(book: PositionBook) -> pd.DataFrame:
        rows: List[dict] = []

        for position in book.positions():
            rows.append(asdict(compute_position_pnl(position)))

        return pd.DataFrame(rows)

    @staticmethod
    def portfolio_pnl(book: PositionBook) -> PortfolioPnL:
        table = PnLEngine.position_pnl_table(book)

        if table.empty:
            return PortfolioPnL(
                positions=0,
                total_market_value=0.0,
                total_unrealized_pnl=0.0,
                average_return=0.0,
            )

        return PortfolioPnL(
            positions=len(table),
            total_market_value=float(table["market_value"].sum()),
            total_unrealized_pnl=float(table["unrealized_pnl"].sum()),
            average_return=float(table["unrealized_return"].mean()),
        )