from pathlib import Path
import pandas as pd

from config.data_version import (
    ATM_IV_DATASET,
    TERM_STRUCTURE_DATASET,
)

from framework.research.base import ResearchBuilder
from framework.research.contracts import ResearchDatasetResult


PREVIEW_PATH = Path("research/exports/term_structure_wide_v1_1_preview.csv")
REPORT_PATH = Path("research/reports/term_structure_wide_v1_1_report.txt")


class TermStructureBuilder(ResearchBuilder):
    dataset_name = "term_structure"

    def build(self) -> ResearchDatasetResult:
        self.validate()

        print("Reading ATM IV dataset v1.1...")
        df = pd.read_parquet(ATM_IV_DATASET)

        df = df[df["has_both"] == True].copy()
        df = df.sort_values(["trade_date", "time_bucket", "T"])

        rows = []

        grouped = df.groupby(["trade_date", "time_bucket"], sort=False)

        total = grouped.ngroups

        for i, (_, group) in enumerate(grouped, start=1):
            group = group.sort_values("T").reset_index(drop=True)

            if len(group) < 2:
                continue

            row = {
                "trade_date": group["trade_date"].iloc[0],
                "time_bucket": group["time_bucket"].iloc[0],
            }

            labels = ["near", "next", "third", "fourth", "fifth", "sixth"]

            for rank, label in enumerate(labels):
                if rank < len(group):
                    g = group.iloc[rank]
                    row[f"{label}_expiry"] = g["expiry_code"]
                    row[f"{label}_T"] = g["T"]
                    row[f"{label}_iv"] = g["atm_iv"]
                    row[f"{label}_strike"] = g["atm_strike"]
                    row[f"{label}_future"] = g["future_price"]
                else:
                    row[f"{label}_expiry"] = None
                    row[f"{label}_T"] = None
                    row[f"{label}_iv"] = None
                    row[f"{label}_strike"] = None
                    row[f"{label}_future"] = None

            row["next_minus_near_iv"] = (
                row["next_iv"] - row["near_iv"]
                if row["next_iv"] is not None and row["near_iv"] is not None
                else None
            )
            row["third_minus_near_iv"] = (
                row["third_iv"] - row["near_iv"]
                if row["third_iv"] is not None and row["near_iv"] is not None
                else None
            )
            row["fourth_minus_near_iv"] = (
                row["fourth_iv"] - row["near_iv"]
                if row["fourth_iv"] is not None and row["near_iv"] is not None
                else None
            )
            row["sixth_minus_near_iv"] = (
                row["sixth_iv"] - row["near_iv"]
                if row["sixth_iv"] is not None and row["near_iv"] is not None
                else None
            )

            rows.append(row)

            if i % 50000 == 0:
                print(f"Processed groups: {i}/{total}")

        out = pd.DataFrame(rows)

        out = out.sort_values(
            ["trade_date", "time_bucket"]
        ).reset_index(drop=True)

        TERM_STRUCTURE_DATASET.parent.mkdir(parents=True, exist_ok=True)
        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

        out.to_parquet(TERM_STRUCTURE_DATASET, index=False)
        out.head(100000).to_csv(PREVIEW_PATH, index=False, encoding="utf-8-sig")

        lines = []
        lines.append("Term Structure Wide Dataset v1.1 Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Source file: {ATM_IV_DATASET}")
        lines.append(f"Output dataset: {TERM_STRUCTURE_DATASET}")
        lines.append("")
        lines.append(f"Rows: {len(out)}")
        lines.append(f"Trade dates: {out['trade_date'].nunique()}")
        lines.append("")
        lines.append("next_minus_near_iv summary:")
        lines.append(str(out["next_minus_near_iv"].describe()))
        lines.append("")
        lines.append("third_minus_near_iv summary:")
        lines.append(str(out["third_minus_near_iv"].describe()))
        lines.append("")
        lines.append("Rows by trade_date summary:")
        lines.append(str(out.groupby("trade_date").size().describe()))

        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

        return ResearchDatasetResult(
            dataset_name=self.dataset_name,
            dataset_path=TERM_STRUCTURE_DATASET,
            preview_path=PREVIEW_PATH,
            report_path=REPORT_PATH,
            rows=len(out),
            status="success",
            message="Term structure dataset v1.1 built successfully.",
        )

    def validate(self) -> None:
        if not ATM_IV_DATASET.exists():
            raise FileNotFoundError(ATM_IV_DATASET)


def main():
    result = TermStructureBuilder().build()
    print(result)


if __name__ == "__main__":
    main()