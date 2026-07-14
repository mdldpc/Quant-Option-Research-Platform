"""
Unified data loading utilities.

All parquet / csv reading should go through DataLoader.
"""

from pathlib import Path
import pandas as pd


class DataLoader:

    @staticmethod
    def read_parquet(path) -> pd.DataFrame:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_parquet(path)

    @staticmethod
    def read_csv(path, **kwargs) -> pd.DataFrame:

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        return pd.read_csv(path, **kwargs)

    @staticmethod
    def exists(path) -> bool:

        return Path(path).exists()

    @staticmethod
    def validate_columns(
        df: pd.DataFrame,
        required_columns,
    ):

        missing = []

        for c in required_columns:

            if c not in df.columns:
                missing.append(c)

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        return True

    @staticmethod
    def summary(df: pd.DataFrame):

        return {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_mb": round(
                df.memory_usage(deep=True).sum() / 1024 / 1024,
                2,
            ),
        }