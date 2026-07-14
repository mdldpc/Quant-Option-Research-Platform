from dataclasses import dataclass
from pathlib import Path


@dataclass
class ResearchDatasetResult:
    dataset_name: str
    dataset_path: Path
    preview_path: Path
    report_path: Path
    rows: int
    status: str
    message: str = ""