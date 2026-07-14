import pandas as pd


def build_daily_execution_snapshot(
    df: pd.DataFrame,
    group_cols: list[str],
    time_col: str = "time_bucket",
    price_col: str = "strangle_price",
    target_time_bucket: int | None = None,
) -> pd.DataFrame:
    """
    Build one execution snapshot per day / expiry / strategy group.

    Rule:
    1. Keep rows with valid positive price.
    2. If target_time_bucket is provided, choose the row closest to it.
    3. Otherwise choose the latest available time_bucket.

    This function is strategy-agnostic and can be reused by straddle,
    strangle, calendar spread, and future option strategies.
    """

    required_cols = set(group_cols + [time_col, price_col])
    missing = required_cols - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    work = df.copy()

    work = work.dropna(subset=[price_col])
    work = work[work[price_col] > 0]

    if work.empty:
        return work

    work[time_col] = work[time_col].astype(int)

    if target_time_bucket is not None:
        work["_time_distance"] = (work[time_col] - int(target_time_bucket)).abs()

        snapshot = (
            work.sort_values(group_cols + ["_time_distance", time_col])
            .groupby(group_cols, as_index=False)
            .head(1)
            .drop(columns=["_time_distance"])
            .reset_index(drop=True)
        )

    else:
        snapshot = (
            work.sort_values(group_cols + [time_col])
            .groupby(group_cols, as_index=False)
            .tail(1)
            .reset_index(drop=True)
        )

    return snapshot