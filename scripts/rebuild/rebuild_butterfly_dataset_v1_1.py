from pathlib import Path
import pandas as pd


INPUT_FILE = Path("research/datasets/smile_dataset_near_2026H1_v1_1.parquet")

OUT_DATASET = Path("research/datasets/butterfly_dataset_2026H1_v1_1.parquet")
OUT_CSV = Path("research/exports/butterfly_dataset_v1_1.csv")
OUT_REPORT = Path("research/reports/butterfly_dataset_v1_1_report.txt")


def mid_price(row):
    if row["BP1"] > 0 and row["AP1"] > 0:
        return (row["BP1"] + row["AP1"]) / 2
    if row["BP1"] > 0:
        return row["BP1"]
    if row["AP1"] > 0:
        return row["AP1"]
    return None


def main():
    print("Reading near smile v1.1 dataset...")
    df = pd.read_parquet(INPUT_FILE)

    print("Source shape:")
    print(df.shape)

    df = df[df["option_type"] == "C"].copy()

    rows = []

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

        rows.append({
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

            "net_delta": (
                lower_row["delta"]
                - 2 * middle_row["delta"]
                + upper_row["delta"]
            ),
            "net_gamma": (
                lower_row["gamma"]
                - 2 * middle_row["gamma"]
                + upper_row["gamma"]
            ),
            "net_vega": (
                lower_row["vega"]
                - 2 * middle_row["vega"]
                + upper_row["vega"]
            ),
            "net_theta": (
                lower_row["theta"]
                - 2 * middle_row["theta"]
                + upper_row["theta"]
            ),
            "net_vanna": (
                lower_row["vanna"]
                - 2 * middle_row["vanna"]
                + upper_row["vanna"]
            ),
            "net_vomma": (
                lower_row["vomma"]
                - 2 * middle_row["vomma"]
                + upper_row["vomma"]
            ),
        })

        if i % 50000 == 0:
            print(f"Processed groups: {i}/{total}")

    out = pd.DataFrame(rows)

    out = out.sort_values(
        ["trade_date", "time_bucket", "expiry_code"]
    ).reset_index(drop=True)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Long Call Butterfly Dataset v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
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

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()