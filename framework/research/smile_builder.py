from pathlib import Path
import numpy as np
import pandas as pd

from config.data_version import (
    ALL_GREEKS_FILE,
    SMILE_DATASET,
)

from framework.research.base import ResearchBuilder
from framework.research.contracts import ResearchDatasetResult


PREVIEW_PATH = Path("research/exports/smile_dataset_near_2026H1_v1_1_preview.csv")
REPORT_PATH = Path("research/reports/smile_dataset_near_2026H1_v1_1_report.txt")


KEEP_COLS = [
    "trade_date",
    "time_bucket",
    "symbol",
    "expiry_code",
    "option_type",
    "strike",
    "future_price",
    "T",
    "implied_vol",
    "smoothed_iv",
    "delta",
    "gamma",
    "vega",
    "theta",
    "vanna",
    "vomma",
    "speed",
    "volume",
    "openInterest",
    "BP1",
    "AP1",
]


class SmileNearBuilder(ResearchBuilder):
    dataset_name = "smile_near"

    def build(self) -> ResearchDatasetResult:
        self.validate()

        print("Reading all Greeks v1.1...")
        df = pd.read_parquet(ALL_GREEKS_FILE, columns=KEEP_COLS)

        print("Source shape:")
        print(df.shape)

        df = df.dropna(
            subset=[
                "trade_date",
                "time_bucket",
                "expiry_code",
                "strike",
                "future_price",
                "T",
                "smoothed_iv",
            ]
        ).copy()

        print("Finding near expiry for each trade_date/time_bucket...")

        near_map = (
            df.groupby(["trade_date", "time_bucket"], as_index=False)
            .agg(near_T=("T", "min"))
        )

        df = df.merge(
            near_map,
            on=["trade_date", "time_bucket"],
            how="left",
        )

        print("Filtering near expiry rows...")
        near_df = df[df["T"] == df["near_T"]].copy()

        near_df["term_rank"] = 1

        print("Near smile shape:")
        print(near_df.shape)

        print("Calculating moneyness...")
        near_df["moneyness"] = near_df["strike"] / near_df["future_price"]
        near_df["log_moneyness"] = np.log(near_df["moneyness"])
        near_df["abs_log_moneyness"] = near_df["log_moneyness"].abs()

        print("Creating moneyness buckets...")

        bins = [
            -np.inf,
            0.90,
            0.95,
            0.98,
            1.02,
            1.05,
            1.10,
            np.inf,
        ]

        labels = [
            "deep_low_moneyness",
            "low_moneyness",
            "slightly_low_moneyness",
            "atm",
            "slightly_high_moneyness",
            "high_moneyness",
            "deep_high_moneyness",
        ]

        near_df["moneyness_bucket"] = pd.cut(
            near_df["moneyness"],
            bins=bins,
            labels=labels,
            include_lowest=True,
        )

        ordered_cols = [
            "trade_date",
            "time_bucket",
            "term_rank",
            "symbol",
            "expiry_code",
            "option_type",
            "strike",
            "future_price",
            "T",
            "moneyness",
            "log_moneyness",
            "abs_log_moneyness",
            "moneyness_bucket",
            "smoothed_iv",
            "implied_vol",
            "delta",
            "gamma",
            "vega",
            "theta",
            "vanna",
            "vomma",
            "speed",
            "volume",
            "openInterest",
            "BP1",
            "AP1",
        ]

        near_df = near_df[ordered_cols].sort_values(
            ["trade_date", "time_bucket", "expiry_code", "strike", "option_type"]
        ).reset_index(drop=True)

        SMILE_DATASET.parent.mkdir(parents=True, exist_ok=True)
        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

        near_df.to_parquet(SMILE_DATASET, index=False)
        near_df.head(100000).to_csv(PREVIEW_PATH, index=False, encoding="utf-8-sig")

        lines = []
        lines.append("Near Smile Dataset v1.1 Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Source file: {ALL_GREEKS_FILE}")
        lines.append(f"Output dataset: {SMILE_DATASET}")
        lines.append("")
        lines.append(f"Rows: {len(near_df)}")
        lines.append(f"Trade dates: {near_df['trade_date'].nunique()}")
        lines.append(f"Expiry codes: {near_df['expiry_code'].nunique()}")
        lines.append("")
        lines.append("Option type counts:")
        lines.append(str(near_df["option_type"].value_counts()))
        lines.append("")
        lines.append("Moneyness bucket counts:")
        lines.append(str(near_df["moneyness_bucket"].value_counts(dropna=False).sort_index()))
        lines.append("")
        lines.append("Smoothed IV summary:")
        lines.append(str(near_df["smoothed_iv"].describe()))
        lines.append("")
        lines.append("Log moneyness summary:")
        lines.append(str(near_df["log_moneyness"].describe()))
        lines.append("")
        lines.append("Rows by trade_date summary:")
        lines.append(str(near_df.groupby("trade_date").size().describe()))

        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

        return ResearchDatasetResult(
            dataset_name=self.dataset_name,
            dataset_path=SMILE_DATASET,
            preview_path=PREVIEW_PATH,
            report_path=REPORT_PATH,
            rows=len(near_df),
            status="success",
            message="Near smile dataset v1.1 built successfully.",
        )

    def validate(self) -> None:
        if not ALL_GREEKS_FILE.exists():
            raise FileNotFoundError(ALL_GREEKS_FILE)


def main():
    result = SmileNearBuilder().build()
    print(result)


if __name__ == "__main__":
    main()