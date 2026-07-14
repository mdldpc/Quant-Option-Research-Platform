from pathlib import Path
import pandas as pd

from framework.strategy.strategy_registry import (
    list_strategies,
    get_strategy,
)


SIGNAL_FILE = Path("research/exports/option_strategy_backtest_v2.csv")

REPORT_FILE = Path(
    "research/reports/build_all_trade_rules_v1_1_report.txt"
)


def load_signals(strategy_name: str) -> pd.DataFrame:
    signals = pd.read_csv(SIGNAL_FILE)

    if "status" in signals.columns:
        signals = signals[signals["status"] == "ok"].copy()

    return signals.reset_index(drop=True)


def build_one_strategy(strategy_name: str) -> dict:
    print("=" * 70)
    print("Building:", strategy_name)

    cfg = get_strategy(strategy_name)

    signals = load_signals(strategy_name)
    snapshot = pd.read_parquet(cfg["snapshot"])

    constructor_cls = cfg["constructor"]
    constructor = constructor_cls(snapshot)

    trades = constructor.build_all(signals)

    out_file = cfg["trade_output"]
    out_file.parent.mkdir(parents=True, exist_ok=True)

    trades.to_csv(out_file, index=False, encoding="utf-8-sig")

    print("Saved:", out_file)
    print("Trades:", len(trades))

    valid_expired_statuses = [
        "contract_expired",
        "calendar_pair_expired",
    ]

    valid_statuses = [
        "constructed",
        *valid_expired_statuses,
    ]

    return {
        "strategy": strategy_name,
        "rows": len(trades),
        "constructed": int((trades["status"] == "constructed").sum()),
        "expired": int(trades["status"].isin(valid_expired_statuses).sum()),
        "other": int((~trades["status"].isin(valid_statuses)).sum()),
        "output": str(out_file),
    }


def main():
    print("=" * 70)
    print("Trade Construction Runner v1.1")
    print("=" * 70)

    summaries = []

    for strategy in list_strategies():
        summaries.append(build_one_strategy(strategy))

    report_lines = []

    report_lines.append("Trade Construction Runner v1.1")
    report_lines.append("=" * 80)
    report_lines.append("")

    total_rows = 0

    for s in summaries:
        total_rows += s["rows"]

        report_lines.append(f"Strategy : {s['strategy']}")
        report_lines.append(f"Rows      : {s['rows']}")
        report_lines.append(f"Construct : {s['constructed']}")
        report_lines.append(f"Expired   : {s['expired']}")
        report_lines.append(f"Other     : {s['other']}")
        report_lines.append(f"Output    : {s['output']}")
        report_lines.append("")
        report_lines.append("-" * 80)
        report_lines.append("")

    report_lines.append(f"Strategies : {len(summaries)}")
    report_lines.append(f"Total Rows : {total_rows}")

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print()
    print("=" * 70)
    print("DONE")
    print("=" * 70)
    print("Report:")
    print(REPORT_FILE)


if __name__ == "__main__":
    main()