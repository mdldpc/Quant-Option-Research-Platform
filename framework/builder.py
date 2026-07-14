"""
=========================================================
Strategy Builder Interface
=========================================================

All strategy builders should return the same structure.

This file defines the standard output format.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class BuilderResult:

    strategy_name: str

    dataset_path: Path

    report_path: Path

    rows: int

    status: str

    message: str = ""


class StrategyBuilder:

    """
    Base class.

    Every future strategy builder should inherit this class.
    """

    strategy_name = "unknown"

    def build(self):

        raise NotImplementedError