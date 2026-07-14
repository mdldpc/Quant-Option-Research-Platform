from pathlib import Path
import pandas as pd


GREEKS_FILE = Path("research/datasets/smile_dataset_near_2026H1.parquet")
TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")

OUT_DATASET = Path("research/datasets/portfolio_greeks_2026H1.parquet")
OUT_CSV = Path("research/exports/portfolio_greeks_2026H1.csv")
OUT_REPORT = Path("research/reports/portfolio_greeks_summary.txt")


GREEK_COLS = ["delta", "gamma", "vega", "theta", "vanna", "vomma"]


def main():
    print("Reading trades...")
    trades = pd.read_csv(TRADES_FILE)
    trades = trades[trades["status"] == "ok"].copy()

    print("Reading option-level Greeks...")
    greeks = pd.read_parquet(
        GREEKS_FILE,
        columns=[
            "trade_date",
            "time_bucket",
            "symbol",
            "expiry_code",
            "option_type",
            "strike",
            "delta",
            "gamma",
            "vega",
            "theta",
            "vanna",
            "vomma",
        ],
    )

    greeks["trade_date"] = greeks["trade_date"].astype(int)
    greeks["expiry_code"] = greeks["expiry_code"].astype(int)
    greeks["strike"] = greeks["strike"].astype(float)

    rows = []

    for trade_id, trade in trades.reset_index(drop=True).iterrows():
        entry = int(trade["entry_date"])
        exit_ = int(trade["exit_date"])
        expiry = int(trade["expiry_code"])
        strike = float(trade["strike"])

        trade_g = greeks[
            (greeks["trade_date"] >= entry)
            & (greeks["trade_date"] <= exit_)
            & (greeks["expiry_code"] == expiry)
            & (greeks["strike"] == strike)
            & (greeks["option_type"].isin(["C", "P"]))
        ].copy()

        if trade_g.empty:
            print(f"WARNING: no Greeks found for trade {trade_id + 1}")
            continue

        daily = (
            trade_g.groupby(["trade_date", "option_type"], as_index=False)[GREEK_COLS]
            .mean()
        )

        wide = daily.pivot(
            index="trade_date",
            columns="option_type",
            values=GREEK_COLS,
        )

        wide.columns = [f"{opt.lower()}_{greek}" for greek, opt in wide.columns]
        wide = wide.reset_index()

        for greek in GREEK_COLS:
            c = f"c_{greek}"
            p = f"p_{greek}"

            if c not in wide.columns:
                wide[c] = 0.0
            if p not in wide.columns:
                wide[p] = 0.0

            wide[f"net_{greek}"] = wide[c] + wide[p]

        wide["trade_id"] = trade_id + 1
        wide["strategy"] = "long_atm_straddle"
        wide["entry_date"] = entry
        wide["exit_date"] = exit_
        wide["expiry_code"] = expiry
        wide["strike"] = strike

        wide = wide.sort_values("trade_date")
        wide["holding_day"] = range(1, len(wide) + 1)

        rows.append(wide)

    if not rows:
        raise RuntimeError("No portfolio Greeks generated.")

    out = pd.concat(rows, ignore_index=True)

    ordered_cols = [
        "trade_id",
        "strategy",
        "trade_date",
        "holding_day",
        "entry_date",
        "exit_date",
        "expiry_code",
        "strike",
        "c_delta",
        "p_delta",
        "net_delta",
        "c_gamma",
        "p_gamma",
        "net_gamma",
        "c_vega",
        "p_vega",
        "net_vega",
        "c_theta",
        "p_theta",
        "net_theta",
        "c_vanna",
        "p_vanna",
        "net_vanna",
        "c_vomma",
        "p_vomma",
        "net_vomma",
    ]

    out = out[ordered_cols]

    OUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    out.to_parquet(OUT_DATASET, index=False)
    out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Portfolio Greeks Summary")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input Greeks file: {GREEKS_FILE}")
    lines.append(f"Input trades file: {TRADES_FILE}")
    lines.append(f"Output dataset: {OUT_DATASET}")
    lines.append("")
    lines.append(f"Rows: {len(out)}")
    lines.append(f"Trades: {out['trade_id'].nunique()}")
    lines.append("")
    lines.append("Net Greeks Summary:")
    lines.append(str(out[[f'net_{g}' for g in GREEK_COLS]].describe()))
    lines.append("")
    lines.append("Rows by trade:")
    lines.append(str(out.groupby("trade_id").size()))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_DATASET)
    print(OUT_CSV)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()