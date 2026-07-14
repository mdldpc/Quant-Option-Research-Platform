from pathlib import Path
import pandas as pd

from config.data_version import ALL_GREEKS_FILE


OUT_DATASET = Path("research/datasets/calendar_spread_dataset_2026H1_v1_1.parquet")
OUT_CSV = Path("research/exports/calendar_spread_dataset_v1_1.csv")
OUT_REPORT = Path("research/reports/calendar_spread_dataset_v1_1_report.txt")


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


def mid_price(row):
    if row["BP1"] > 0 and row["AP1"] > 0:
        return (row["BP1"] + row["AP1"]) / 2
    if row["BP1"] > 0:
        return row["BP1"]
    if row["AP1"] > 0:
        return row["AP1"]
    return None


def build_atm_straddle(group):
    future_price = group["future_price"].median()

    calls = group[group["option_type"] == "C"].copy()
    puts = group[group["option_type"] == "P"].copy()

    if calls.empty or puts.empty:
        return None

    call = calls.loc[(calls["strike"] - future_price).abs().idxmin()]
    put = puts.loc[(puts["strike"] - future_price).abs().idxmin()]

    call_mid = mid_price(call)
    put_mid = mid_price(put)

    if call_mid is None or put_mid is None:
        return None

    return {
        "expiry_code": int(group["expiry_code"].iloc[0]),
        "T": group["T"].median(),
        "atm_strike": (call["strike"] + put["strike"]) / 2,
        "future_price": future_price,
        "atm_iv": (call["smoothed_iv"] + put["smoothed_iv"]) / 2,
        "call_iv": call["smoothed_iv"],
        "put_iv": put["smoothed_iv"],
        "call_symbol": call["symbol"],
        "put_symbol": put["symbol"],
        "call_mid": call_mid,
        "put_mid": put_mid,
        "straddle_price": call_mid + put_mid,
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
    }


def compute_net_greek(near, next_, greek):
    return (
        near[f"call_{greek}"]
        + near[f"put_{greek}"]
        - next_[f"call_{greek}"]
        - next_[f"put_{greek}"]
    )


def main():
    print("Reading all Greeks v1.1...")
    df = pd.read_parquet(ALL_GREEKS_FILE, columns=KEEP_COLS)

    print("Source shape:")
    print(df.shape)

    rows = []

    grouped = df.groupby(["trade_date", "time_bucket"], sort=False)
    total = grouped.ngroups

    for i, ((trade_date, time_bucket), group) in enumerate(grouped, start=1):
        straddles = []

        for _, expiry_group in group.groupby("expiry_code", sort=False):
            item = build_atm_straddle(expiry_group)
            if item is not None:
                straddles.append(item)

        if len(straddles) < 2:
            continue

        straddles = sorted(straddles, key=lambda x: x["T"])

        near = straddles[0]
        next_ = straddles[1]

        row = {
            "trade_date": int(trade_date),
            "time_bucket": int(time_bucket),

            "near_expiry": near["expiry_code"],
            "next_expiry": next_["expiry_code"],

            "near_T": near["T"],
            "next_T": next_["T"],

            "near_strike": near["atm_strike"],
            "next_strike": next_["atm_strike"],

            "near_future": near["future_price"],
            "next_future": next_["future_price"],

            "near_iv": near["atm_iv"],
            "next_iv": next_["atm_iv"],
            "iv_spread": next_["atm_iv"] - near["atm_iv"],

            "near_call_symbol": near["call_symbol"],
            "near_put_symbol": near["put_symbol"],
            "next_call_symbol": next_["call_symbol"],
            "next_put_symbol": next_["put_symbol"],

            "near_call_mid": near["call_mid"],
            "near_put_mid": near["put_mid"],
            "next_call_mid": next_["call_mid"],
            "next_put_mid": next_["put_mid"],

            "near_straddle_price": near["straddle_price"],
            "next_straddle_price": next_["straddle_price"],

            "calendar_price": near["straddle_price"] - next_["straddle_price"],

            "net_delta": compute_net_greek(near, next_, "delta"),
            "net_gamma": compute_net_greek(near, next_, "gamma"),
            "net_vega": compute_net_greek(near, next_, "vega"),
            "net_theta": compute_net_greek(near, next_, "theta"),
            "net_vanna": compute_net_greek(near, next_, "vanna"),
            "net_vomma": compute_net_greek(near, next_, "vomma"),

            "calendar_direction": "long_near_short_next",
        }

        rows.append(row)

        if i % 50000 == 0:
            print(f"Processed groups: {i}/{total}")

    out = pd.DataFrame(rows)

    out = out.sort_values(
        ["trade_date", "time_bucket"]
    ).reset_index(drop=True)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Calendar Spread Dataset v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Source file: {ALL_GREEKS_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Rows: {len(out)}")
    lines.append(f"Trade dates: {out['trade_date'].nunique()}")
    lines.append("")
    lines.append("IV spread summary:")
    lines.append(str(out["iv_spread"].describe()))
    lines.append("")
    lines.append("Calendar price summary:")
    lines.append(str(out["calendar_price"].describe()))
    lines.append("")
    lines.append("Near straddle price summary:")
    lines.append(str(out["near_straddle_price"].describe()))
    lines.append("")
    lines.append("Next straddle price summary:")
    lines.append(str(out["next_straddle_price"].describe()))
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