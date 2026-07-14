"""
Performance Report Builder

Builds summary statistics from portfolio NAV timeseries.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class PerformanceSummary:
    start_date: int
    end_date: int
    observations: int

    initial_nav: float
    final_nav: float
    total_return: float

    max_drawdown: float
    best_day_pnl: float
    worst_day_pnl: float

    average_pnl: float
    positive_days: int
    negative_days: int
    win_rate: float

    critical_days: int
    warning_days: int
    normal_days: int


class PerformanceReportBuilder:

    @staticmethod
    def summarize(nav_df: pd.DataFrame) -> PerformanceSummary:
        if nav_df.empty:
            return PerformanceSummary(
                start_date=0,
                end_date=0,
                observations=0,
                initial_nav=0.0,
                final_nav=0.0,
                total_return=0.0,
                max_drawdown=0.0,
                best_day_pnl=0.0,
                worst_day_pnl=0.0,
                average_pnl=0.0,
                positive_days=0,
                negative_days=0,
                win_rate=0.0,
                critical_days=0,
                warning_days=0,
                normal_days=0,
            )

        df = nav_df.copy()
        df = df.sort_values("trade_date").reset_index(drop=True)

        initial_nav = float(df["current_nav"].iloc[0])
        final_nav = float(df["current_nav"].iloc[-1])

        if initial_nav == 0:
            total_return = 0.0
        else:
            total_return = (final_nav - initial_nav) / initial_nav

        pnl = df["unrealized_pnl"].fillna(0)

        positive_days = int((pnl > 0).sum())
        negative_days = int((pnl < 0).sum())

        denom = positive_days + negative_days
        win_rate = positive_days / denom if denom > 0 else 0.0

        return PerformanceSummary(
            start_date=int(df["trade_date"].iloc[0]),
            end_date=int(df["trade_date"].iloc[-1]),
            observations=len(df),
            initial_nav=initial_nav,
            final_nav=final_nav,
            total_return=total_return,
            max_drawdown=float(df["drawdown"].min()),
            best_day_pnl=float(pnl.max()),
            worst_day_pnl=float(pnl.min()),
            average_pnl=float(pnl.mean()),
            positive_days=positive_days,
            negative_days=negative_days,
            win_rate=win_rate,
            critical_days=int((df["risk_status"] == "critical").sum()),
            warning_days=int((df["risk_status"] == "warning").sum()),
            normal_days=int((df["risk_status"] == "normal").sum()),
        )

    @staticmethod
    def build_text_report(
        summary: PerformanceSummary,
        nav_df: pd.DataFrame,
    ) -> str:
        lines = []

        lines.append("Performance Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Start Date     : {summary.start_date}")
        lines.append(f"End Date       : {summary.end_date}")
        lines.append(f"Observations   : {summary.observations}")
        lines.append("")

        lines.append("NAV Summary")
        lines.append("-" * 80)
        lines.append(f"Initial NAV    : {summary.initial_nav:,.2f}")
        lines.append(f"Final NAV      : {summary.final_nav:,.2f}")
        lines.append(f"Total Return   : {summary.total_return:.6%}")
        lines.append(f"Max Drawdown   : {summary.max_drawdown:.6%}")
        lines.append("")

        lines.append("PnL Summary")
        lines.append("-" * 80)
        lines.append(f"Best Day PnL   : {summary.best_day_pnl:,.2f}")
        lines.append(f"Worst Day PnL  : {summary.worst_day_pnl:,.2f}")
        lines.append(f"Average PnL    : {summary.average_pnl:,.2f}")
        lines.append(f"Positive Days  : {summary.positive_days}")
        lines.append(f"Negative Days  : {summary.negative_days}")
        lines.append(f"Win Rate       : {summary.win_rate:.6%}")
        lines.append("")

        lines.append("Risk Status Summary")
        lines.append("-" * 80)
        lines.append(f"Normal Days    : {summary.normal_days}")
        lines.append(f"Warning Days   : {summary.warning_days}")
        lines.append(f"Critical Days  : {summary.critical_days}")
        lines.append("")

        lines.append("NAV Timeseries")
        lines.append("-" * 80)

        if nav_df.empty:
            lines.append("No NAV timeseries available.")
        else:
            lines.append(nav_df.to_string(index=False))

        return "\n".join(lines)

    @staticmethod
    def write_text_report(
        report_text: str,
        path: Path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report_text, encoding="utf-8")