from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)


def run_strategy(strategy_name: str):

    print("=" * 80)
    print(f"Running strategy: {strategy_name}")
    print("=" * 80)


    # --------------------------------------------------
    # Load strategy configuration
    # --------------------------------------------------

    config = get_strategy(
        strategy_name
    )


    signal_generator_cls = config.get(
        "signal_generator"
    )

    constructor_cls = config[
        "constructor"
    ]

    backtester_cls = config[
        "backtester"
    ]


    # --------------------------------------------------
    # Signal generation
    # --------------------------------------------------

    if signal_generator_cls is None:

        raise ValueError(
            f"No signal generator registered for {strategy_name}"
        )


    signal_input = config[
        "signal_input"
    ]


    print("\nLoading signal input:")
    print(signal_input)


    signal_df = pd.read_parquet(
        signal_input
    )


    print(
        "Signal source rows:",
        len(signal_df)
    )


    generator = signal_generator_cls()


    signals = generator.generate(
        signal_df
    )


    print(
        "Generated signals:",
        len(signals)
    )


    if signals.empty:

        print(
            "No signals generated."
        )

        return



    # --------------------------------------------------
    # Trade construction
    # --------------------------------------------------

    snapshot_path = config[
        "snapshot"
    ]


    print("\nLoading snapshot:")
    print(snapshot_path)


    snapshot = pd.read_parquet(
        snapshot_path
    )


    print(
        "Snapshot rows:",
        len(snapshot)
    )


    constructor = constructor_cls(
        snapshot
    )


    trades = constructor.build_all(
        signals
    )

    print("\nTrade status:")
    print(
        trades["status"].value_counts()
    )

    print(
        "Constructed trades:",
        len(trades)
    )


    trade_output = config[
        "trade_output"
    ]


    trade_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    trades.to_csv(
        trade_output,
        index=False,
        encoding="utf-8-sig",
    )


    print(
        "Saved trades:"
    )

    print(
        trade_output
    )


    # --------------------------------------------------
    # Backtest
    # --------------------------------------------------

    backtester = backtester_cls(
        trades
    )


    result = backtester.backtest(
        report_path=config["backtest_report"],
        trades_path=config["backtest_output"],
    )


    print("\nBacktest Result")
    print("-" * 80)

    print(
        result
    )


    print("\nDONE")

    return result


if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_strategy.py strategy_name"
        )

        print(
            "\nAvailable strategies:"
        )


        from framework.strategy.strategy_registry import (
            list_strategies,
        )


        for s in list_strategies():

            print(
                " -",
                s
            )

        sys.exit(1)


    run_strategy(
        sys.argv[1]
    )