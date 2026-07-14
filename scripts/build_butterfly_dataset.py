from pathlib import Path
import pandas as pd

from framework.strategy_dataset_builder import StrategyDatasetBuilder
from framework.builder import BuilderResult


SOURCE_FILE = Path("data_parquet/batch_2026/all_greeks_2026H1.parquet")

OUT_DATASET = Path("research/datasets/butterfly_dataset_2026H1.parquet")
OUT_CSV = Path("research/exports/butterfly_dataset_preview.csv")
OUT_REPORT = Path("research/reports/butterfly_dataset_report.txt")


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
    "BP1",
    "AP1",
]


class LongCallButterflyBuilder(StrategyDatasetBuilder):
    strategy_name = "long_call_butterfly"
    source_file = SOURCE_FILE
    output_dataset = OUT_DATASET
    output_report = OUT_REPORT

    def build(self) -> BuilderResult:
        self.validate_inputs()

        print("Reading all Greeks dataset...")
        df = pd.read_parquet(self.source_file, columns=KEEP_COLS)

        df = df[df["option_type"] == "C"].copy()
        df = df.dropna(subset=["trade_date", "time_bucket", "expiry_code", "strike", "future_price"])

        print("Source call shape:")
        print(df.shape)

        results = []

        grouped = df.groupby(["trade_date", "time_bucket", "expiry_code"], sort=False)
        total = grouped.ngroups

        for i, (_, group) in enumerate(grouped, start=1):
            future_price = group["future_price"].median()

            strikes = sorted(group["strike"].dropna().unique())

            if len(strikes) < 3:
                continue

            middle = min(strikes, key=lambda x: abs(x - future_price))
            middle_idx = strikes.index(middle)

            if middle_idx == 0 or middle_idx == len(strikes) - 1:
                continue

            lower = strikes[middle_idx - 1]
            upper = strikes[middle_idx + 1]

            lower_row = group[group["strike"] == lower].iloc[-1]
            middle_row = group[group["strike"] == middle].iloc[-1]
            upper_row = group[group["strike"] == upper].iloc[-1]

            def mid_price(row):
                if row["BP1"] > 0 and row["AP1"] > 0:
                    return (row["BP1"] + row["AP1"]) / 2
                return None

            lower_price = mid_price(lower_row)
            middle_price = mid_price(middle_row)
            upper_price = mid_price(upper_row)

            butterfly_price = None
            if (
                lower_price is not None
                and middle_price is not None
                and upper_price is not None
            ):
                butterfly_price = lower_price - 2 * middle_price + upper_price

            results.append(
                {
                    "trade_date": group["trade_date"].iloc[0],
                    "time_bucket": group["time_bucket"].iloc[0],
                    "expiry_code": group["expiry_code"].iloc[0],
                    "future_price": future_price,
                    "T": group["T"].median(),
                    "lower_symbol": lower_row["symbol"],
                    "middle_symbol": middle_row["symbol"],
                    "upper_symbol": upper_row["symbol"],
                    "lower_strike": lower,
                    "middle_strike": middle,
                    "upper_strike": upper,
                    "strike_width_low": middle - lower,
                    "strike_width_high": upper - middle,
                    "is_symmetric": (middle - lower) == (upper - middle),
                    "lower_price": lower_price,
                    "middle_price": middle_price,
                    "upper_price": upper_price,
                    "butterfly_price": butterfly_price,
                    "net_delta": lower_row["delta"] - 2 * middle_row["delta"] + upper_row["delta"],
                    "net_gamma": lower_row["gamma"] - 2 * middle_row["gamma"] + upper_row["gamma"],
                    "net_vega": lower_row["vega"] - 2 * middle_row["vega"] + upper_row["vega"],
                    "net_theta": lower_row["theta"] - 2 * middle_row["theta"] + upper_row["theta"],
                    "net_vanna": lower_row["vanna"] - 2 * middle_row["vanna"] + upper_row["vanna"],
                    "net_vomma": lower_row["vomma"] - 2 * middle_row["vomma"] + upper_row["vomma"],
                }
            )

            if i % 50000 == 0:
                print(f"Processed groups: {i}/{total}")

        out = pd.DataFrame(results)

        out = out.sort_values(["trade_date", "time_bucket", "expiry_code"]).reset_index(drop=True)

        OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

        out.to_parquet(OUT_DATASET, index=False)
        out.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

        lines = []
        lines.append("Long Call Butterfly Dataset Report")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Source file: {self.source_file}")
        lines.append(f"Output dataset: {OUT_DATASET}")
        lines.append("")
        lines.append(f"Rows: {len(out)}")
        lines.append(f"Trade dates: {out['trade_date'].nunique()}")
        lines.append(f"Expiry codes: {out['expiry_code'].nunique()}")
        lines.append("")
        lines.append("Symmetry counts:")
        lines.append(str(out["is_symmetric"].value_counts()))
        lines.append("")
        lines.append("Butterfly price summary:")
        lines.append(str(out["butterfly_price"].describe()))
        lines.append("")
        lines.append("Net Greeks summary:")
        lines.append(str(out[["net_delta", "net_gamma", "net_vega", "net_theta"]].describe()))

        OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

        return BuilderResult(
            strategy_name=self.strategy_name,
            dataset_path=OUT_DATASET,
            report_path=OUT_REPORT,
            rows=len(out),
            status="success",
            message="Long call butterfly dataset built successfully.",
        )


def main():
    builder = LongCallButterflyBuilder()
    result = builder.build()
    print(result)


if __name__ == "__main__":
    main()