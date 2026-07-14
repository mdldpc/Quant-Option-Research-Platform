"""
==========================================================
Rebuild Pipeline Common Utilities
==========================================================

Shared utilities for all v1.1 rebuild scripts.

Pipeline

cleaned_sessions
        ↓
IV
        ↓
Greeks
        ↓
Research Dataset
        ↓
Strategy Dataset
"""

from pathlib import Path
from typing import Iterable

from config.data_version import (
    CLEANED_SESSION_DIR,
    REBUILD_DIR,
    DATA_VERSION,
)


# ==========================================================
# File Discovery
# ==========================================================

def iter_cleaned_sessions() -> Iterable[Path]:
    """
    Iterate over all cleaned session parquet files.
    """

    files = sorted(
        CLEANED_SESSION_DIR.glob("*.session_clean.parquet")
    )

    return files


def cleaned_session_count() -> int:
    """
    Number of cleaned session files.
    """

    return len(list(iter_cleaned_sessions()))


# ==========================================================
# Output Directory
# ==========================================================

def ensure_rebuild_directory() -> None:
    """
    Create rebuild output directory.
    """

    REBUILD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Version
# ==========================================================

def version_tag() -> str:
    """
    Current rebuild version.
    """

    return DATA_VERSION


# ==========================================================
# Progress
# ==========================================================

def print_rebuild_header(title: str) -> None:

    print("=" * 72)
    print(title)
    print("=" * 72)

    print(f"Version          : {DATA_VERSION}")
    print(f"Input Directory  : {CLEANED_SESSION_DIR}")
    print(f"Output Directory : {REBUILD_DIR}")
    print()


def print_progress(
    current: int,
    total: int,
    every: int = 10,
) -> None:

    if current == 1:

        print(f"Processing {total} session files...")

    if (
        current % every == 0
        or current == total
    ):

        print(
            f"Processed "
            f"{current}/{total}"
        )


# ==========================================================
# Validation
# ==========================================================

def validate_cleaned_sessions() -> None:
    """
    Basic validation.
    """

    files = list(iter_cleaned_sessions())

    if len(files) == 0:

        raise FileNotFoundError(
            f"No cleaned session files found:\n"
            f"{CLEANED_SESSION_DIR}"
        )


# ==========================================================
# Summary
# ==========================================================

def show_rebuild_environment() -> None:

    print_rebuild_header(
        "Rebuild Environment"
    )

    print(
        f"Detected session files : "
        f"{cleaned_session_count()}"
    )

    print(
        f"Version tag            : "
        f"{version_tag()}"
    )

    print()

    files = list(iter_cleaned_sessions())

    if files:

        print(
            f"First file             : "
            f"{files[0].name}"
        )

        print(
            f"Last file              : "
            f"{files[-1].name}"
        )



# ==========================================================
# Script Test
# ==========================================================

if __name__ == "__main__":

    show_rebuild_environment()