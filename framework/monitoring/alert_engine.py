"""
Alert Engine

Converts PortfolioStatus into alert events.

AlertEngine does not compute Greeks or risk.
It only evaluates monitoring status and records alerts.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

import pandas as pd

from framework.monitoring.portfolio_monitor import PortfolioStatus


@dataclass
class AlertEvent:

    timestamp: str

    level: str

    title: str

    message: str


class AlertEngine:

    def __init__(self):

        self._history: List[AlertEvent] = []

    def update(
        self,
        status: PortfolioStatus,
    ) -> AlertEvent | None:

        if status.overall_status == "normal":
            return None

        if status.overall_status == "warning":
            level = "WARNING"
        elif status.overall_status == "critical":
            level = "CRITICAL"
        else:
            level = "INFO"

        message = (
            f"{status.critical_risks} critical risk(s), "
            f"{status.warning_risks} warning risk(s)."
        )

        event = AlertEvent(
            timestamp=datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            level=level,
            title="Portfolio Risk Alert",
            message=message,
        )

        self._history.append(event)

        return event

    def latest(self):

        if not self._history:
            return None

        return self._history[-1]

    def history(self) -> pd.DataFrame:

        if not self._history:
            return pd.DataFrame()

        return pd.DataFrame(
            [asdict(x) for x in self._history]
        )

    def clear(self):

        self._history.clear()

    def size(self):

        return len(self._history)