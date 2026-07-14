"""
===========================================================
Data Version Configuration
===========================================================

Centralized data version control for rebuild pipelines.
"""

from pathlib import Path


DATA_VERSION = "v1_1"

USE_CLEAN_SESSION = True


# =========================================================
# Input Directories
# =========================================================

CLEANED_SESSION_DIR = Path("data/cleaned_sessions")

RAW_GREEKS_DIR = Path("data_parquet/batch_2026")


# =========================================================
# Core Rebuild Outputs
# =========================================================

REBUILD_DIR = Path("data_parquet/batch_2026")

ALL_IV_FILE = REBUILD_DIR / f"all_iv_2026H1_{DATA_VERSION}.parquet"

ALL_GREEKS_FILE = REBUILD_DIR / f"all_greeks_2026H1_{DATA_VERSION}.parquet"


# =========================================================
# Research Dataset Outputs
# =========================================================

RESEARCH_DATASET_DIR = Path("research/datasets")

ATM_IV_DATASET = RESEARCH_DATASET_DIR / f"atm_iv_dataset_2026H1_{DATA_VERSION}.parquet"

SMILE_DATASET = RESEARCH_DATASET_DIR / f"smile_dataset_near_2026H1_{DATA_VERSION}.parquet"

SURFACE_DATASET = RESEARCH_DATASET_DIR / f"surface_dataset_near_2026H1_{DATA_VERSION}.parquet"

TERM_STRUCTURE_DATASET = RESEARCH_DATASET_DIR / f"term_structure_wide_{DATA_VERSION}.parquet"


# =========================================================
# Strategy Dataset Outputs
# =========================================================

STRANGLE_DATASET = RESEARCH_DATASET_DIR / f"option_strangle_dataset_2026H1_{DATA_VERSION}.parquet"

BUTTERFLY_DATASET = RESEARCH_DATASET_DIR / f"butterfly_dataset_2026H1_{DATA_VERSION}.parquet"

CALENDAR_DATASET = RESEARCH_DATASET_DIR / f"calendar_spread_dataset_2026H1_{DATA_VERSION}.parquet"


def show_data_version():
    print("=" * 70)
    print("Data Version Configuration")
    print("=" * 70)
    print(f"DATA_VERSION       : {DATA_VERSION}")
    print(f"USE_CLEAN_SESSION  : {USE_CLEAN_SESSION}")
    print(f"CLEANED_SESSION_DIR: {CLEANED_SESSION_DIR}")
    print(f"ALL_IV_FILE        : {ALL_IV_FILE}")
    print(f"ALL_GREEKS_FILE    : {ALL_GREEKS_FILE}")