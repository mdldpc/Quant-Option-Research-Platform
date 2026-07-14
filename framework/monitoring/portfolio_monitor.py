"""
Portfolio Monitor

High-level monitoring built on top of
Exposure Engine and Risk Engine.

PortfolioMonitor never computes Greeks itself.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

import pandas as pd

from framework.risk.exposure import compute_exposure
from framework.risk.hedge_rules import (
    HedgeRuleConfig,
    generate_hedge_recommendations,
)


@dataclass
class PortfolioStatus:

    timestamp: str

    position_count: int

    overall_status: str

    critical_risks: int

    warning_risks: int

    recommendations: list


class PortfolioMonitor:

    def __init__(
        self,
        config: HedgeRuleConfig | None = None,
    ):

        self.config = config or HedgeRuleConfig()

        self._history: List[PortfolioStatus] = []

    def update(
        self,
        positions: pd.DataFrame,
        timestamp: str | None = None,
    ) -> PortfolioStatus:

        if timestamp is None:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        exposure = compute_exposure(positions)

        recommendations = generate_hedge_recommendations(
            exposure,
            self.config,
        )

        critical = sum(
            r.risk_level == "critical"
            for r in recommendations
        )

        warning = sum(
            r.risk_level == "warning"
            for r in recommendations
        )

        if critical > 0:
            overall = "critical"
        elif warning > 0:
            overall = "warning"
        else:
            overall = "normal"

        snapshot = PortfolioStatus(
            timestamp=timestamp,
            position_count=exposure.positions,
            overall_status=overall,
            critical_risks=critical,
            warning_risks=warning,
            recommendations=recommendations,
        )

        self._history.append(snapshot)

        return snapshot

    def latest(self):

        if not self._history:
            return None

        return self._history[-1]

    def history(self) -> pd.DataFrame:

        if not self._history:
            return pd.DataFrame()

        rows = []

        for x in self._history:

            d = asdict(x)

            d["recommendations"] = len(
                d["recommendations"]
            )

            rows.append(d)

        return pd.DataFrame(rows)

    def clear(self):

        self._history.clear()

    def size(self):

        return len(self._history)