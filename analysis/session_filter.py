import pandas as pd


def filter_regular_trading_session(
    df: pd.DataFrame,
    time_col: str = "updateTime",
) -> pd.DataFrame:
    """
    Keep only regular continuous trading sessions.

    For Chinese index options/futures day session, this filter keeps:
    - Morning:   09:31:00 to 11:30:00
    - Afternoon: 13:01:00 to 14:56:00

    It excludes opening auction, closing auction, lunch break,
    and after-market abnormal records.
    """

    if time_col not in df.columns:
        raise ValueError(f"Missing time column: {time_col}")

    t = pd.to_datetime(df[time_col].astype(str), format="%H:%M:%S", errors="coerce").dt.time

    morning = (
        (t >= pd.to_datetime("09:31:00").time())
        & (t <= pd.to_datetime("11:30:00").time())
    )

    afternoon = (
        (t >= pd.to_datetime("13:01:00").time())
        & (t <= pd.to_datetime("14:56:00").time())
    )

    mask = morning | afternoon

    return df.loc[mask].copy()