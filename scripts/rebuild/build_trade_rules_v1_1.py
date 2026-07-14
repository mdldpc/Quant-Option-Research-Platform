from pathlib import Path
import pandas as pd

from framework.strategy.trade_constructor import StrangleTradeConstructor


OLD_TRADES_FILE = Path("research/exports/option_strategy_backtest_v2.csv")
SNAPSHOT_FILE = Path("research/datasets/strangle_daily_snapshot_2026H1_v1_1.parquet")

OUT_FILE = Path("research/exports/option_strategy_backtest_v1_1.csv")
OUT_REPORT = Path("research/reports/trade_rules_v1_1_report.txt")


def main():
    print("Reading old signal/trade file...")
    signals = pd.read_csv(OLD_TRADES_FILE)

    signals = signals[signals["status"] == "ok"].copy()

    print("Reading strangle snapshot v1.1...")
    snapshot = pd.read_parquet(SNAPSHOT_FILE)

    constructor = StrangleTradeConstructor(snapshot)

    print("Constructing trades...")
    trades = constructor.build_all(signals)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    trades.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")

    lines = []
    lines.append("Trade Construction Rules v1.1 Report")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Input signal file: {OLD_TRADES_FILE}")
    lines.append(f"Snapshot file: {SNAPSHOT_FILE}")
    lines.append(f"Output file: {OUT_FILE}")
    lines.append("")
    lines.append(f"Trades: {len(trades)}")
    lines.append("")
    lines.append("Status counts:")
    lines.append(str(trades["status"].value_counts()))
    lines.append("")
    lines.append("Construction reason counts:")
    lines.append(str(trades["construction_reason"].value_counts()))
    lines.append("")
    lines.append("Trades:")
    lines.append(str(trades))

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("DONE")
    print("Saved:")
    print(OUT_FILE)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()