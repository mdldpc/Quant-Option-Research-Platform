from pathlib import Path
import pandas as pd

from config.data_version import (
    ALL_GREEKS_FILE,
    ATM_IV_DATASET,
)

from framework.research.base import ResearchBuilder
from framework.research.contracts import ResearchDatasetResult


PREVIEW_PATH = Path("research/exports/atm_iv_dataset_2026H1_v1_1_preview.csv")
REPORT_PATH = Path("research/reports/atm_iv_dataset_2026H1_v1_1_report.txt")


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
]


class ATMBuilder(ResearchBuilder):
    dataset_name = "atm_iv"

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
                "smoothed_iv",
            ]
        ).copy()

        rows = []

        grouped = df.groupby(
            ["trade_date", "time_bucket", "expiry_code"],
            sort=False,
        )

        total = grouped.ngroups

        for i, (_, group) in enumerate(grouped, start=1):
            future_price = group["future_price"].median()

            group = group.copy()
            group["abs_moneyness"] = (
                group["strike"] - future_price
            ).abs()

            min_abs = group["abs_moneyness"].min()
            atm = group[group["abs_moneyness"] == min_abs].copy()

            call = atm[atm["option_type"] == "C"]
            put = atm[atm["option_type"] == "P"]

            call_row = call.iloc[-1] if len(call) else None
            put_row = put.iloc[-1] if len(put) else None

            has_call = call_row is not None
            has_put = put_row is not None
            has_both = has_call and has_put

            if not has_call and not has_put:
                continue

            ivs = []
            raw_ivs = []

            if has_call:
                ivs.append(call_row["smoothed_iv"])
                raw_ivs.append(call_row["implied_vol"])

            if has_put:
                ivs.append(put_row["smoothed_iv"])
                raw_ivs.append(put_row["implied_vol"])

            rows.append({
                "trade_date": group["trade_date"].iloc[0],
                "time_bucket": group["time_bucket"].iloc[0],
                "expiry_code": group["expiry_code"].iloc[0],
                "atm_strike": atm["strike"].median(),
                "future_price": future_price,
                "abs_moneyness": min_abs,
                "T": group["T"].median(),

                "atm_iv": sum(ivs) / len(ivs),
                "call_iv": call_row["smoothed_iv"] if has_call else None,
                "put_iv": put_row["smoothed_iv"] if has_put else None,
                "call_put_iv_spread": (
                    call_row["smoothed_iv"] - put_row["smoothed_iv"]
                    if has_both else None
                ),

                "has_call": has_call,
                "has_put": has_put,
                "has_both": has_both,

                "call_symbol": call_row["symbol"] if has_call else None,
                "put_symbol": put_row["symbol"] if has_put else None,

                "call_raw_iv": call_row["implied_vol"] if has_call else None,
                "put_raw_iv": put_row["implied_vol"] if has_put else None,

                "call_delta": call_row["delta"] if has_call else None,
                "put_delta": put_row["delta"] if has_put else None,
                "call_gamma": call_row["gamma"] if has_call else None,
                "put_gamma": put_row["gamma"] if has_put else None,
                "call_vega": call_row["vega"] if has_call else None,
                "put_vega": put_row["vega"] if has_put else None,
                "call_theta": call_row["theta"] if has_call else None,
                "put_theta": put_row["theta"] if has_put else None,
                "call_vanna": call_row["vanna"] if has_call else None,
                "put_vanna": put_row["vanna"] if has_put else None,
                "call_vomma": call_row["vomma"] if has_call else None,
                "put_vomma": put_row["vomma"] if has_put else None,
                "call_speed": call_row["speed"] if has_call else None,
                "put_speed": put_row["speed"] if has_put else None,
            })

            if i % 50000 == 0:
                print(f"Processed groups: {i}/{total}")

        out = pd.DataFrame(rows)

        out = out.sort_values(
            ["trade_date", "time_bucket", "expiry_code"]
        ).reset_index(drop=True)

        ATM_IV_DATASET.parent.mkdir(parents=True, exist_ok=True)
        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

        out.to_parquet(ATM_IV_DATASET, index=False)
        out.head(100000).to_csv(PREVIEW_PATH, index=False, encoding="utf-8-sig")

        lines = []
        lines.append("ATM IV Dataset v1.1 Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Source file: {ALL_GREEKS_FILE}")
        lines.append(f"Output dataset: {ATM_IV_DATASET}")
        lines.append("")
        lines.append(f"Rows: {len(out)}")
        lines.append(f"Trade dates: {out['trade_date'].nunique()}")
        lines.append(f"Expiry codes: {out['expiry_code'].nunique()}")
        lines.append("")
        lines.append("has_both counts:")
        lines.append(str(out["has_both"].value_counts()))
        lines.append("")
        lines.append("ATM IV summary:")
        lines.append(str(out["atm_iv"].describe()))
        lines.append("")
        lines.append("Rows by trade_date summary:")
        lines.append(str(out.groupby("trade_date").size().describe()))

        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

        return ResearchDatasetResult(
            dataset_name=self.dataset_name,
            dataset_path=ATM_IV_DATASET,
            preview_path=PREVIEW_PATH,
            report_path=REPORT_PATH,
            rows=len(out),
            status="success",
            message="ATM IV dataset v1.1 built successfully.",
        )

    def validate(self) -> None:
        if not ALL_GREEKS_FILE.exists():
            raise FileNotFoundError(ALL_GREEKS_FILE)


def main():
    result = ATMBuilder().build()
    print(result)


if __name__ == "__main__":
    main()