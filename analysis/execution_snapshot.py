from pathlib import Path
import pandas as pd


def build_strategy_snapshot(
    df: pd.DataFrame,
    strategy_name: str,
    group_cols: list[str],
    price_col: str,
    time_col: str = "time_bucket",
    target_time_bucket: int | None = None,
    max_time_distance: int | None = None,
    fallback_to_latest: bool = True,
    allow_negative_price: bool = False,
) -> pd.DataFrame:
    """
    Universal execution snapshot engine.

    Parameters
    ----------
    allow_negative_price
        False:
            Remove rows with price <= 0.
            Used by:
                Straddle
                Strangle
                Butterfly

        True:
            Keep all prices except NaN.
            Used by:
                Calendar Spread
                Box Spread
                Other debit/credit strategies
    """

    required_cols = set(group_cols + [time_col, price_col])

    missing = required_cols - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    work = df.copy()

    # ---------------------------------------------------
    # Price filtering
    # ---------------------------------------------------

    work = work.dropna(subset=[price_col])

    if not allow_negative_price:
        work = work[work[price_col] > 0]

    if work.empty:
        return work

    work[time_col] = work[time_col].astype(int)

    # ---------------------------------------------------
    # Latest snapshot
    # ---------------------------------------------------

    if target_time_bucket is None:

        snapshot = (
            work
            .sort_values(group_cols + [time_col])
            .groupby(group_cols, as_index=False)
            .tail(1)
            .reset_index(drop=True)
        )

        snapshot["snapshot_rule"] = "latest_valid"

    # ---------------------------------------------------
    # Target snapshot
    # ---------------------------------------------------

    else:

        work["_time_distance"] = (
            work[time_col] - int(target_time_bucket)
        ).abs()

        if max_time_distance is not None:

            near_target = work[
                work["_time_distance"] <= int(max_time_distance)
            ].copy()

        else:

            near_target = work.copy()

        if len(near_target):

            target_snapshot = (
                near_target
                .sort_values(group_cols + ["_time_distance", time_col])
                .groupby(group_cols, as_index=False)
                .head(1)
                .reset_index(drop=True)
            )

        else:

            target_snapshot = pd.DataFrame(columns=work.columns)

        target_snapshot["snapshot_rule"] = "target_time"

        if fallback_to_latest:

            if len(target_snapshot):

                selected = target_snapshot[group_cols].drop_duplicates()

            else:

                selected = pd.DataFrame(columns=group_cols)

            remaining = work.merge(
                selected.assign(_selected=1),
                on=group_cols,
                how="left",
            )

            remaining = remaining[
                remaining["_selected"].isna()
            ].drop(columns="_selected")

            if len(remaining):

                fallback = (
                    remaining
                    .sort_values(group_cols + [time_col])
                    .groupby(group_cols, as_index=False)
                    .tail(1)
                    .reset_index(drop=True)
                )

            else:

                fallback = pd.DataFrame(columns=work.columns)

            fallback["snapshot_rule"] = "fallback_latest"

            snapshot = pd.concat(
                [target_snapshot, fallback],
                ignore_index=True,
            )

        else:

            snapshot = target_snapshot

        snapshot = snapshot.drop(
            columns="_time_distance",
            errors="ignore",
        )

    snapshot["strategy_name"] = strategy_name

    return snapshot


def save_strategy_snapshot(
    snapshot: pd.DataFrame,
    dataset_path: Path,
    csv_path: Path,
    report_path: Path,
    price_col: str,
) -> None:
    """
    Save snapshot dataset + report.
    """

    dataset_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot.to_parquet(dataset_path, index=False)
    snapshot.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []

    lines.append("Strategy Snapshot Report")
    lines.append("=" * 80)
    lines.append("")

    lines.append(f"Output dataset: {dataset_path}")

    lines.append(f"Rows: {len(snapshot)}")

    if len(snapshot):

        if "strategy_name" in snapshot.columns:

            lines.append(
                f"Strategy: {snapshot['strategy_name'].iloc[0]}"
            )

    if "trade_date" in snapshot.columns:

        lines.append(
            f"Trade dates: {snapshot['trade_date'].nunique()}"
        )

    if "expiry_code" in snapshot.columns:

        lines.append(
            f"Expiry codes: {snapshot['expiry_code'].nunique()}"
        )

    if "snapshot_rule" in snapshot.columns:

        lines.append("")
        lines.append("Snapshot rule counts:")
        lines.append(
            str(snapshot["snapshot_rule"].value_counts())
        )

    lines.append("")
    lines.append("Price summary:")
    lines.append(
        str(snapshot[price_col].describe())
    )

    report_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )