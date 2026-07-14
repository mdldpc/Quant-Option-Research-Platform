"""
Greek Monitor

Maintains a history of portfolio Greek exposure snapshots.

The monitor does not compute Greeks itself.
It delegates all calculations to framework.risk.exposure.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

import pandas as pd

from framework.risk.exposure import compute_exposure


@dataclass
class GreekSnapshot:

    timestamp: str

    position_count: int

    net_delta: float
    net_gamma: float
    net_vega: float
    net_theta: float

    gross_delta: float
    gross_vega: float


class GreekMonitor:

    def __init__(self):

        self._history: List[GreekSnapshot] = []

    def update(
        self,
        positions: pd.DataFrame,
        timestamp: str | None = None,
    ) -> GreekSnapshot:
        """
        Compute current portfolio exposure and
        append one monitoring snapshot.
        """

        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        exposure = compute_exposure(positions)

        snapshot = GreekSnapshot(

            timestamp=timestamp,

            position_count=exposure.positions,

            net_delta=exposure.net_delta,
            net_gamma=exposure.net_gamma,
            net_vega=exposure.net_vega,
            net_theta=exposure.net_theta,

            gross_delta=exposure.gross_delta,
            gross_vega=exposure.gross_vega,
        )

        self._history.append(snapshot)

        return snapshot

    def latest(self) -> GreekSnapshot | None:

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

    def size(self) -> int:

        return len(self._history)