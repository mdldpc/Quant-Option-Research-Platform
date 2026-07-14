"""
Portfolio NAV Engine

Maintains portfolio NAV statistics.

NAV = Initial Capital + Unrealized PnL
"""

from __future__ import annotations

from dataclasses import dataclass

from framework.portfolio.position_book import PositionBook
from framework.portfolio.pnl_engine import PnLEngine


@dataclass
class PortfolioNAV:

    initial_capital: float

    current_nav: float

    total_market_value: float

    unrealized_pnl: float

    cumulative_return: float

    drawdown: float


class NAVEngine:

    def __init__(
        self,
        initial_capital: float,
    ):

        self.initial_capital = float(initial_capital)

        self.high_water_mark = float(initial_capital)

    def update(
        self,
        book: PositionBook,
    ) -> PortfolioNAV:

        pnl = PnLEngine.portfolio_pnl(book)

        current_nav = (
            self.initial_capital
            + pnl.total_unrealized_pnl
        )

        if current_nav > self.high_water_mark:
            self.high_water_mark = current_nav

        if self.initial_capital == 0:
            cumulative_return = 0.0
        else:
            cumulative_return = (
                current_nav
                - self.initial_capital
            ) / self.initial_capital

        if self.high_water_mark == 0:
            drawdown = 0.0
        else:
            drawdown = (
                current_nav
                - self.high_water_mark
            ) / self.high_water_mark

        return PortfolioNAV(
            initial_capital=self.initial_capital,
            current_nav=current_nav,
            total_market_value=pnl.total_market_value,
            unrealized_pnl=pnl.total_unrealized_pnl,
            cumulative_return=cumulative_return,
            drawdown=drawdown,
        )