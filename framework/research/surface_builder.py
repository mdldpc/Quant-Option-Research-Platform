from pathlib import Path
import pandas as pd

from config.data_version import (
    SMILE_DATASET,
    SURFACE_DATASET,
)

from framework.research.base import ResearchBuilder
from framework.research.contracts import ResearchDatasetResult


PREVIEW_PATH = Path("research/exports/surface_dataset_near_2026H1_v1_1_preview.csv")
REPORT_PATH = Path("research/reports/surface_dataset_near_2026H1_v1_1_report.txt")


class SurfaceNearBuilder(ResearchBuilder):
    dataset_name = "surface_near"

    def build(self) -> ResearchDatasetResult:
        self.validate()

        print("Reading near smile dataset v1.1...")
        df = pd.read_parquet(SMILE_DATASET)

        print("Source shape:")
        print(df.shape)

        df = df.copy()

        df["surface_moneyness_bucket"] = df["moneyness_bucket"].astype(str)

        out = (
            df.groupby(
                [
                    "trade_date",
                    "time_bucket",
                    "surface_moneyness_bucket",
                ],
                as_index=False,
            )
            .agg(
                smoothed_iv_mean=("smoothed_iv", "mean"),
                smoothed_iv_median=("smoothed_iv", "median"),
                smoothed_iv_std=("smoothed_iv", "std"),
                implied_vol_mean=("implied_vol", "mean"),
                row_count=("smoothed_iv", "count"),
                avg_moneyness=("moneyness", "mean"),
                avg_log_moneyness=("log_moneyness", "mean"),
                avg_abs_log_moneyness=("abs_log_moneyness", "mean"),
                avg_T=("T", "mean"),
                call_count=("option_type", lambda x: (x == "C").sum()),
                put_count=("option_type", lambda x: (x == "P").sum()),
                volume_sum=("volume", "sum"),
                openInterest_sum=("openInterest", "sum"),
            )
        )

        out = out.sort_values(
            [
                "trade_date",
                "time_bucket",
                "surface_moneyness_bucket",
            ]
        ).reset_index(drop=True)

        SURFACE_DATASET.parent.mkdir(parents=True, exist_ok=True)
        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

        out.to_parquet(SURFACE_DATASET, index=False)
        out.head(100000).to_csv(PREVIEW_PATH, index=False, encoding="utf-8-sig")

        lines = []
        lines.append("Near Surface Dataset v1.1 Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Source file: {SMILE_DATASET}")
        lines.append(f"Output dataset: {SURFACE_DATASET}")
        lines.append("")
        lines.append(f"Rows: {len(out)}")
        lines.append(f"Trade dates: {out['trade_date'].nunique()}")
        lines.append("")
        lines.append("Surface bucket counts:")
        lines.append(str(out["surface_moneyness_bucket"].value_counts()))
        lines.append("")
        lines.append("Smoothed IV mean summary:")
        lines.append(str(out["smoothed_iv_mean"].describe()))
        lines.append("")
        lines.append("Rows by trade_date summary:")
        lines.append(str(out.groupby("trade_date").size().describe()))

        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

        return ResearchDatasetResult(
            dataset_name=self.dataset_name,
            dataset_path=SURFACE_DATASET,
            preview_path=PREVIEW_PATH,
            report_path=REPORT_PATH,
            rows=len(out),
            status="success",
            message="Near surface dataset v1.1 built successfully.",
        )

    def validate(self) -> None:
        if not SMILE_DATASET.exists():
            raise FileNotFoundError(SMILE_DATASET)


def main():
    result = SurfaceNearBuilder().build()
    print(result)


if __name__ == "__main__":
    main()