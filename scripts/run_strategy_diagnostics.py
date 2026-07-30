from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)

from analysis.strategy_diagnostics import (
    StrategyDiagnostics,
)



def run_diagnostics(strategy_name: str):

    print("=" * 80)
    print(f"Running diagnostics: {strategy_name}")
    print("=" * 80)


    # --------------------------------------------------
    # Load strategy configuration
    # --------------------------------------------------

    config = get_strategy(
        strategy_name
    )


    signal_input = config["signal_input"]


    print("\nLoading signal input:")
    print(signal_input)


    # --------------------------------------------------
    # Load signal dataset
    # --------------------------------------------------

    df = pd.read_parquet(
        signal_input
    )


    print(
        "Feature source rows:",
        len(df)
    )


    signal_generator_cls = config["signal_generator"]


    generator = signal_generator_cls()


    signals = generator.generate(
        df
    )


    print(
        "Generated signals:",
        len(signals)
    )


    diagnostics = StrategyDiagnostics(
        signals=signals,

        score_column=config.get(
            "signal_score_column",
            "entry_signal_score"
        ),

        signal_direction=config.get(
            "signal_direction",
            "positive"
        ),
    )


    summary = diagnostics.summary()


    print("\nSignal Summary")
    print("-" * 80)


    for key, value in summary.items():

        print(
            f"{key}: {value}"
        )



    # --------------------------------------------------
    # Threshold analysis
    # --------------------------------------------------

    threshold_df = diagnostics.threshold_analysis()


    print("\nThreshold Analysis")
    print("-" * 80)

    print(
        threshold_df
    )



    # --------------------------------------------------
    # Save reports
    # --------------------------------------------------

    report_dir = Path(
        "research/reports"
    )


    report_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    summary_file = (
        report_dir
        /
        f"{strategy_name}_diagnostics_summary_v1_1.csv"
    )


    threshold_file = (
        report_dir
        /
        f"{strategy_name}_threshold_analysis_v1_1.csv"
    )


    pd.DataFrame(
        [summary]
    ).to_csv(
        summary_file,
        index=False,
        encoding="utf-8-sig",
    )


    threshold_df.to_csv(
        threshold_file,
        index=False,
        encoding="utf-8-sig",
    )


    print("\nSaved:")
    print(summary_file)
    print(threshold_file)


    print("\nDONE")



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_strategy_diagnostics.py strategy_name"
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



    run_diagnostics(
        sys.argv[1]
    )