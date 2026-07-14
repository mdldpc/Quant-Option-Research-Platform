from pathlib import Path
import pandas as pd


INPUT_FILE = Path("research/datasets/smile_dataset_near_2026H1_v1_1.parquet")

OUT_DATASET = Path("research/datasets/option_strangle_dataset_2026H1_v1_1.parquet")
OUT_CSV = Path("research/exports/option_strangle_dataset_v1_1.csv")
OUT_REPORT = Path("research/reports/option_strangle_dataset_v1_1_report.txt")


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

    rows = []

    grouped = df.groupby(["trade_date", "time_bucket", "expiry_code"], sort=False)
    total = grouped.ngroups

    for i, (_, group) in enumerate(grouped, start=1):
        future_price = group["future_price"].median()

        calls = group[group["option_type"] == "C"].copy()
        puts = group[group["option_type"] == "P"].copy()

        if calls.empty or puts.empty:
            continue

        calls["abs_moneyness"] = (calls["strike"] - future_price).abs()
        puts["abs_moneyness"] = (puts["strike"] - future_price).abs()

        call_row = calls.sort_values("abs_moneyness").iloc[0]
        put_row = puts.sort_values("abs_moneyness").iloc[0]

        call_price = mid_price(call_row)
        put_price = mid_price(put_row)

        if call_price is None or put_price is None:
            strangle_price = None
        else:
            strangle_price = call_price + put_price

        rows.append({
            "trade_date": group["trade_date"].iloc[0],
            "time_bucket": group["time_bucket"].iloc[0],
            "expiry_code": group["expiry_code"].iloc[0],
            "future_price": future_price,
            "T": group["T"].median(),

            "call_symbol": call_row["symbol"],
            "put_symbol": put_row["symbol"],

            "call_strike": call_row["strike"],
            "put_strike": put_row["strike"],

            "call_moneyness": call_row["strike"] / future_price,
            "put_moneyness": put_row["strike"] / future_price,

            "call_iv": call_row["smoothed_iv"],
            "put_iv": put_row["smoothed_iv"],
            "call_raw_iv": call_row["implied_vol"],
            "put_raw_iv": put_row["implied_vol"],

            "call_delta": call_row["delta"],
            "put_delta": put_row["delta"],
            "call_gamma": call_row["gamma"],
            "put_gamma": put_row["gamma"],
            "call_vega": call_row["vega"],
            "put_vega": put_row["vega"],
            "call_theta": call_row["theta"],
            "put_theta": put_row["theta"],
            "call_vanna": call_row["vanna"],
            "put_vanna": put_row["vanna"],
            "call_vomma": call_row["vomma"],
            "put_vomma": put_row["vomma"],
            "call_speed": call_row["speed"],
            "put_speed": put_row["speed"],

            "call_price": call_price,
            "put_price": put_price,
            "strangle_price": strangle_price,

            "has_call": True,
            "has_put": True,
            "has_both": True,
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
    lines.append("Option Strangle Dataset v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input file: {INPUT_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Rows: {len(out)}")
    lines.append(f"Trade dates: {out['trade_date'].nunique()}")
    lines.append(f"Expiry codes: {out['expiry_code'].nunique()}")
    lines.append("")
    lines.append("Strangle price summary:")
    lines.append(str(out["strangle_price"].describe()))
    lines.append("")
    lines.append("Call moneyness summary:")
    lines.append(str(out["call_moneyness"].describe()))
    lines.append("")
    lines.append("Put moneyness summary:")
    lines.append(str(out["put_moneyness"].describe()))
    lines.append("")
    lines.append("Rows by trade_date summary:")
    lines.append(str(out.groupby("trade_date").size().describe()))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()