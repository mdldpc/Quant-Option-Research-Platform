"""
=========================================================
Strategy Dataset Builder v2
=========================================================

This module defines the common structure for building
strategy-level datasets directly from complete option-level
Greeks data.

All future strategy datasets should be generated from
all_greeks_2026H1.parquet or its session-clean v1.1 version,
not from research summary datasets such as smile or surface data.
"""

from pathlib import Path

from framework.builder import StrategyBuilder, BuilderResult


class StrategyDatasetBuilder(StrategyBuilder):
    """
    Base class for all strategy dataset builders.

    A strategy dataset builder should:

    1. Read complete option-level Greeks data.
    2. Select strategy legs.
    3. Construct strategy-level prices and Greeks.
    4. Save parquet dataset.
    5. Save preview CSV.
    6. Save summary report.
    7. Return BuilderResult.
    """

    source_file: Path | None = None
    output_dataset: Path | None = None
    output_report: Path | None = None

    def validate_inputs(self):
        if self.source_file is None:
            raise ValueError("source_file is not defined.")

        if not Path(self.source_file).exists():
            raise FileNotFoundError(self.source_file)

    def build(self) -> BuilderResult:
        raise NotImplementedError