from pathlib import Path
import pandas as pd


SOURCE_FILE = Path("research/datasets/smile_dataset_near_2026H1.parquet")

OUT_DATASET = Path("research/datasets/option_strangle_dataset_2026H1.parquet")
OUT_CSV = Path("research/exports/option_strangle_dataset.csv")
OUT_REPORT = Path("research/reports/option_strangle_dataset_report.txt")


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


def build_strangle_snapshot(group: pd.DataFrame):
    trade_date = group["trade_date"].iloc[0]
    time_bucket = group["time_bucket"].iloc[0]
    expiry_code = group["expiry_code"].iloc[0]
    future_price = group["future_price"].median()
    T = group["T"].median()

    calls = group[
        (group["option_type"] == "C")
        & (group["strike"] > future_price)
    ].copy()

    puts = group[
        (group["option_type"] == "P")
        & (group["strike"] < future_price)
    ].copy()

    if calls.empty or puts.empty:
        return None

    call = calls.loc[(calls["strike"] - future_price).abs().idxmin()]
    put = puts.loc[(puts["strike"] - future_price).abs().idxmin()]

    call_price = (
        (call["BP1"] + call["AP1"]) / 2
        if call["BP1"] > 0 and call["AP1"] > 0
        else None
    )

    put_price = (
        (put["BP1"] + put["AP1"]) / 2
        if put["BP1"] > 0 and put["AP1"] > 0
        else None
    )

    strangle_price = (
        call_price + put_price
        if call_price is not None and put_price is not None
        else None
    )

    return {
        "trade_date": trade_date,
        "time_bucket": time_bucket,
        "expiry_code": expiry_code,
        "future_price": future_price,
        "T": T,
        "call_symbol": call["symbol"],
        "put_symbol": put["symbol"],
        "call_strike": call["strike"],
        "put_strike": put["strike"],
        "call_moneyness": call["strike"] / future_price,
        "put_moneyness": put["strike"] / future_price,
        "call_iv": call["smoothed_iv"],
        "put_iv": put["smoothed_iv"],
        "call_raw_iv": call["implied_vol"],
        "put_raw_iv": put["implied_vol"],
        "call_delta": call["delta"],
        "put_delta": put["delta"],
        "call_gamma": call["gamma"],
        "put_gamma": put["gamma"],
        "call_vega": call["vega"],
        "put_vega": put["vega"],
        "call_theta": call["theta"],
        "put_theta": put["theta"],
        "call_vanna": call["vanna"],
        "put_vanna": put["vanna"],
        "call_vomma": call["vomma"],
        "put_vomma": put["vomma"],
        "call_speed": call["speed"],
        "put_speed": put["speed"],
        "call_price": call_price,
        "put_price": put_price,
        "strangle_price": strangle_price,
        "has_call": True,
        "has_put": True,
        "has_both": True,
    }


def main():
    print("Reading near smile dataset...")
    df = pd.read_parquet(SOURCE_FILE, columns=KEEP_COLS)

    print("Source shape:")
    print(df.shape)

    df = df.dropna(subset=["trade_date", "time_bucket", "expiry_code", "strike", "future_price"])

    results = []

    grouped = df.groupby(["trade_date", "time_bucket", "expiry_code"], sort=False)

    total_groups = grouped.ngroups
    print(f"Groups: {total_groups}")

    for i, (_, group) in enumerate(grouped, start=1):
        row = build_strangle_snapshot(group)
        if row is not None:
            results.append(row)

        if i % 50000 == 0:
            print(f"Processed groups: {i}/{total_groups}")

    out = pd.DataFrame(results)

    out = out.sort_values(
        ["trade_date", "time_bucket", "expiry_code"]
    ).reset_index(drop=True)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Option Strangle Dataset Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
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
    lines.append("Rows by trade date summary:")
    lines.append(str(out.groupby("trade_date").size().describe()))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("\nDONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()