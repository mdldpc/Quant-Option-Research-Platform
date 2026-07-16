from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class ReportData:
    """
    Standardized data model
    for research report generation.

    This layer converts internal
    backtest outputs into report-ready data.
    """


    # -------------------------
    # Strategy Information
    # -------------------------

    strategy_name: str

    display_name: str = ""

    description: str = ""



    # -------------------------
    # Performance Metrics
    # -------------------------

    performance_metrics: Dict[str, Any] = field(
        default_factory=dict
    )


    # -------------------------
    # Trade Statistics
    # -------------------------

    trade_statistics: Dict[str, Any] = field(
        default_factory=dict
    )


    # -------------------------
    # Risk Information
    # -------------------------

    risk_metrics: Dict[str, Any] = field(
        default_factory=dict
    )


    # -------------------------
    # Generated Files
    # -------------------------

    charts: Dict[str, Path] = field(
        default_factory=dict
    )


    report_path: Optional[Path] = None



    # -------------------------
    # Metadata
    # -------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )