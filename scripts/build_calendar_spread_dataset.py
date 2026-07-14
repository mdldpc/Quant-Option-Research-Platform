from pathlib import Path
import pandas as pd


SOURCE_FILE = Path("data_parquet/batch_2026/all_greeks_2026H1.parquet")

OUT_DATASET = Path("research/datasets/calendar_spread_dataset_2026H1.parquet")
OUT_CSV = Path("research/exports/calendar_spread_dataset_preview.csv")
OUT_REPORT = Path("research/reports/calendar_spread_dataset_report.txt")


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


def get_mid(row):
    if row["BP1"] > 0 and row["AP1"] > 0:
        return (row["BP1"] + row["AP1"]) / 2
    return None


def build_atm_straddle_by_expiry(group: pd.DataFrame):
    rows = []

    for expiry, g in group.groupby("expiry_code", sort=False):
        future_price = g["future_price"].median()

        calls = g[g["option_type"] == "C"].copy()
        puts = g[g["option_type"] == "P"].copy()

        if calls.empty or puts.empty:
            continue

        call = calls.loc[(calls["strike"] - future_price).abs().idxmin()]
        put = puts.loc[(puts["strike"] - future_price).abs().idxmin()]

        call_mid = get_mid(call)
        put_mid = get_mid(put)

        if call_mid is None or put_mid is None:
            continue

        rows.append({
            "expiry_code": int(expiry),
            "T": g["T"].median(),
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
        })

    return rows


def main():
    print("Reading all Greeks dataset...")
    df = pd.read_parquet(SOURCE_FILE, columns=KEEP_COLS)

    df = df.copy()
    df["trade_date"] = df["trade_date"].astype(int)
    df["expiry_code"] = df["expiry_code"].astype(int)

    df = df.dropna(
        subset=[
            "trade_date",
            "time_bucket",
            "expiry_code",
            "option_type",
            "strike",
            "future_price",
        ]
    )

    print("Source shape:")
    print(df.shape)

    rows = []

    grouped = df.groupby(["trade_date", "time_bucket"], sort=False)
    total = grouped.ngroups

    for i, ((trade_date, time_bucket), group) in enumerate(grouped, start=1):
        straddles = build_atm_straddle_by_expiry(group)

        if len(straddles) < 2:
            continue

        straddles = sorted(straddles, key=lambda x: x["T"])

        near = straddles[0]
        next_ = straddles[1]

        rows.append({
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

            # long near straddle, short next straddle
            "calendar_price": near["straddle_price"] - next_["straddle_price"],

            "net_delta": (
                near["call_delta"] + near["put_delta"]
                - next_["call_delta"] - next_["put_delta"]
            ),
            "net_gamma": (
                near["call_gamma"] + near["put_gamma"]
                - next_["call_gamma"] - next_["put_gamma"]
            ),
            "net_vega": (
                near["call_vega"] + near["put_vega"]
                - next_["call_vega"] - next_["put_vega"]
            ),
            "net_theta": (
                near["call_theta"] + near["put_theta"]
                - next_["call_theta"] - next_["put_theta"]
            ),
            "net_vanna": (
                near["call_vanna"] + near["put_vanna"]
                - next_["call_vanna"] - next_["put_vanna"]
            ),
            "net_vomma": (
                near["call_vomma"] + near["put_vomma"]
                - next_["call_vomma"] - next_["put_vomma"]
            ),

            "calendar_direction": "long_near_short_next",
        })

        if i % 50000 == 0:
            print(f"Processed groups: {i}/{total}")

    out = pd.DataFrame(rows)

    out = out.sort_values(["trade_date", "time_bucket"]).reset_index(drop=True)

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.head(100000).to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Calendar Spread Dataset Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Source file: {SOURCE_FILE}")
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