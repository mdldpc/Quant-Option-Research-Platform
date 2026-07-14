"""
Portfolio Report Builder

Presentation layer for portfolio status.

This module does not calculate pricing, PnL, NAV, risk, or hedge logic.
It only formats already-computed results into report-ready structures.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class PortfolioReportData:
    trade_date: int
    initial_capital: float
    current_nav: float
    unrealized_pnl: float
    cumulative_return: float
    drawdown: float
    positions: int
    market_value: float
    net_delta: float
    net_gamma: float
    net_vega: float
    net_theta: float
    risk_status: str


class PortfolioReportBuilder:

    @staticmethod
    def build_text_report(
        data: PortfolioReportData,
        pnl_table: pd.DataFrame,
        hedge_plan: pd.DataFrame,
    ) -> str:
        lines = []

        lines.append("Portfolio Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Trade Date      : {data.trade_date}")
        lines.append(f"Initial Capital : {data.initial_capital:,.2f}")
        lines.append("")

        lines.append("NAV Summary")
        lines.append("-" * 80)
        lines.append(f"Current NAV     : {data.current_nav:,.2f}")
        lines.append(f"Unrealized PnL  : {data.unrealized_pnl:,.2f}")
        lines.append(f"Cumulative Ret  : {data.cumulative_return:.6%}")
        lines.append(f"Drawdown        : {data.drawdown:.6%}")
        lines.append("")

        lines.append("Position Summary")
        lines.append("-" * 80)
        lines.append(f"Positions       : {data.positions}")
        lines.append(f"Market Value    : {data.market_value:,.2f}")
        lines.append("")

        lines.append("Risk Summary")
        lines.append("-" * 80)
        lines.append(f"Risk Status     : {data.risk_status}")
        lines.append(f"Net Delta       : {data.net_delta:.6f}")
        lines.append(f"Net Gamma       : {data.net_gamma:.6f}")
        lines.append(f"Net Vega        : {data.net_vega:.6f}")
        lines.append(f"Net Theta       : {data.net_theta:.6f}")
        lines.append("")

        lines.append("Position PnL")
        lines.append("-" * 80)

        if pnl_table.empty:
            lines.append("No position PnL available.")
        else:
            lines.append(pnl_table.to_string(index=False))

        lines.append("")
        lines.append("Hedge Plan")
        lines.append("-" * 80)

        if hedge_plan.empty:
            lines.append("No hedge plan available.")
        else:
            lines.append(hedge_plan.to_string(index=False))

        return "\n".join(lines)

    @staticmethod
    def write_text_report(
        report_text: str,
        path: Path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report_text, encoding="utf-8")