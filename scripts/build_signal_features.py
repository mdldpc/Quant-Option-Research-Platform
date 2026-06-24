from pathlib import Path
import numpy as np
import pandas as pd

TERM_FILE = Path(
    r"D:\Quant_Option_Project\research\summaries\daily_atm_term_structure_2026H1.parquet"
)

OUT_FILE = Path(
    r"D:\Quant_Option_Project\research\signals\daily_signal_features.parquet"
)

OUT_CSV = Path(
    r"D:\Quant_Option_Project\research\exports\daily_signal_features.csv"
)

REPORT_FILE = Path(
    r"D:\Quant_Option_Project\research\reports\daily_signal_features_report.txt"
)

ROLLING_WINDOW = 20
MIN_PERIODS = 10


def iv_score_from_z(z):
    """
    Long-only volatility idea:
    lower IV relative to recent history = higher score.
    """
    if pd.isna(z):
        return 0

    if z <= -2.0:
        return 60
    elif z <= -1.5:
        return 50
    elif z <= -1.0:
        return 40
    elif z <= -0.5:
        return 25
    else:
        return 0


def slope_score_from_slope(slope):
    """
    Prefer normal contango:
    next IV > near IV.
    """
    if pd.isna(slope):
        return 0

    if slope > 0.015:
        return 40
    elif slope > 0.010:
        return 35
    elif slope > 0.005:
        return 25
    elif slope > 0:
        return 15
    else:
        return 0


def main():
    print("Reading daily ATM term structure...")
    df = pd.read_parquet(TERM_FILE)

    print("Source shape:")
    print(df.shape)

    print("Pivoting term ranks...")
    wide_iv = (
        df.pivot(
            index="trade_date",
            columns="term_rank",
            values="atm_iv_mean",
        )
        .reset_index()
        .sort_values("trade_date")
    )

    wide_days = (
        df.pivot(
            index="trade_date",
            columns="term_rank",
            values="days_to_expiry_mean",
        )
        .reset_index()
        .sort_values("trade_date")
    )

    rename_iv = {
        1: "near_iv",
        2: "next_iv",
        3: "third_iv",
        4: "fourth_iv",
    }

    rename_days = {
        1: "near_days",
        2: "next_days",
        3: "third_days",
        4: "fourth_days",
    }

    wide_iv = wide_iv.rename(columns=rename_iv)
    wide_days = wide_days.rename(columns=rename_days)

    features = wide_iv.merge(
        wide_days,
        on="trade_date",
        how="left",
    )

    features["trade_date_dt"] = pd.to_datetime(
        features["trade_date"].astype(str)
    )

    print("Feature base shape:")
    print(features.shape)

    print("Calculating term structure features...")
    features["term_slope_next_near"] = (
        features["next_iv"] - features["near_iv"]
    )

    features["term_slope_third_near"] = (
        features["third_iv"] - features["near_iv"]
    )

    features["term_slope_fourth_near"] = (
        features["fourth_iv"] - features["near_iv"]
    )

    features["is_contango_next_near"] = (
        features["term_slope_next_near"] > 0
    ).astype(int)

    print("Calculating rolling IV features...")

    features = features.sort_values("trade_date").copy()

    features["near_iv_roll_mean"] = (
        features["near_iv"]
        .rolling(
            window=ROLLING_WINDOW,
            min_periods=MIN_PERIODS,
        )
        .mean()
    )

    features["near_iv_roll_std"] = (
        features["near_iv"]
        .rolling(
            window=ROLLING_WINDOW,
            min_periods=MIN_PERIODS,
        )
        .std()
    )

    features["near_iv_zscore"] = (
        (features["near_iv"] - features["near_iv_roll_mean"])
        / features["near_iv_roll_std"]
    )

    features["near_iv_percentile_20d"] = (
        features["near_iv"]
        .rolling(
            window=ROLLING_WINDOW,
            min_periods=MIN_PERIODS,
        )
        .apply(
            lambda x: pd.Series(x).rank(pct=True).iloc[-1],
            raw=False,
        )
    )

    print("Calculating signal scores...")

    features["iv_score"] = features["near_iv_zscore"].apply(iv_score_from_z)

    features["slope_score"] = features["term_slope_next_near"].apply(
        slope_score_from_slope
    )

    features["signal_score"] = (
        features["iv_score"] + features["slope_score"]
    )

    features["long_signal"] = (
        features["signal_score"] >= 80
    ).astype(int)

    features["signal_strength"] = pd.cut(
        features["signal_score"],
        bins=[-1, 0, 40, 60, 80, 100],
        labels=[
            "none",
            "weak",
            "medium",
            "strong",
            "very_strong",
        ],
    )

    ordered_cols = [
        "trade_date",
        "trade_date_dt",
        "near_iv",
        "next_iv",
        "third_iv",
        "fourth_iv",
        "near_days",
        "next_days",
        "third_days",
        "fourth_days",
        "term_slope_next_near",
        "term_slope_third_near",
        "term_slope_fourth_near",
        "is_contango_next_near",
        "near_iv_roll_mean",
        "near_iv_roll_std",
        "near_iv_zscore",
        "near_iv_percentile_20d",
        "iv_score",
        "slope_score",
        "signal_score",
        "signal_strength",
        "long_signal",
    ]

    existing_cols = [
        c for c in ordered_cols
        if c in features.columns
    ]

    features = features[existing_cols].sort_values("trade_date")

    print("\nFinal feature shape:")
    print(features.shape)

    print("\nSignal score summary:")
    print(features["signal_score"].describe())

    print("\nSignal counts:")
    print(features["long_signal"].value_counts())

    print("\nSignal strength counts:")
    print(features["signal_strength"].value_counts(dropna=False))

    print("\nTop signal days:")
    print(
        features.sort_values("signal_score", ascending=False)
        .head(20)
        [
            [
                "trade_date",
                "near_iv",
                "next_iv",
                "term_slope_next_near",
                "near_iv_zscore",
                "iv_score",
                "slope_score",
                "signal_score",
                "long_signal",
            ]
        ]
    )

    print("Saving outputs...")
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    features.to_parquet(OUT_FILE, index=False)

    features.to_csv(
        OUT_CSV,
        index=False,
        encoding="utf-8-sig",
    )

    lines = []
    lines.append("====================================")
    lines.append("Daily Signal Features Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Source file: {TERM_FILE}")
    lines.append(f"Output parquet: {OUT_FILE}")
    lines.append(f"Output csv: {OUT_CSV}")
    lines.append("")
    lines.append(f"Rolling window: {ROLLING_WINDOW}")
    lines.append(f"Min periods: {MIN_PERIODS}")
    lines.append("")
    lines.append(f"Final shape: {features.shape}")
    lines.append("")
    lines.append("Signal score summary:")
    lines.append(str(features["signal_score"].describe()))
    lines.append("")
    lines.append("Long signal counts:")
    lines.append(str(features["long_signal"].value_counts()))
    lines.append("")
    lines.append("Signal strength counts:")
    lines.append(str(features["signal_strength"].value_counts(dropna=False)))
    lines.append("")
    lines.append("Top signal days:")
    lines.append(
        str(
            features.sort_values("signal_score", ascending=False)
            .head(30)
            [
                [
                    "trade_date",
                    "near_iv",
                    "next_iv",
                    "term_slope_next_near",
                    "near_iv_zscore",
                    "iv_score",
                    "slope_score",
                    "signal_score",
                    "long_signal",
                ]
            ]
        )
    )

    REPORT_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nDONE")
    print("Saved feature parquet:")
    print(OUT_FILE)
    print("Saved feature csv:")
    print(OUT_CSV)
    print("Saved report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()