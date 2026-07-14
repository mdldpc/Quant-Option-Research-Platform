"""
Trading day discovery utilities.

Scans project data folders and extracts available trade dates.
"""

from pathlib import Path
import re
from typing import List


DATE_PATTERN = re.compile(r"(20\d{6})")


def extract_trade_date_from_path(path: Path) -> int | None:
    """
    Extract YYYYMMDD trade date from file or folder path.
    """
    text = str(path)

    m = DATE_PATTERN.search(text)

    if not m:
        return None

    return int(m.group(1))


def find_available_trade_dates(
    root: Path | str,
    pattern: str = "*.parquet",
) -> List[int]:
    """
    Find all available trade dates under a directory.

    Parameters
    ----------
    root
        Directory to scan.

    pattern
        Glob pattern, default '*.parquet'.

    Returns
    -------
    Sorted list of unique YYYYMMDD dates.
    """
    root = Path(root)

    if not root.exists():
        raise FileNotFoundError(root)

    dates = []

    for path in root.rglob(pattern):
        d = extract_trade_date_from_path(path)

        if d is not None:
            dates.append(d)

    return sorted(set(dates))


def filter_trade_dates(
    dates: List[int],
    start_date: int | None = None,
    end_date: int | None = None,
) -> List[int]:
    """
    Filter trade dates by optional start/end date.
    """
    out = []

    for d in dates:
        if start_date is not None and d < int(start_date):
            continue

        if end_date is not None and d > int(end_date):
            continue

        out.append(d)

    return out