import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(ROOT)
)



import pandas as pd


from framework.strategy.strategy_registry import (
    get_strategy,
)


from analysis.strategy_capacity import (
    StrategyCapacityAnalyzer,
)


from analysis.raw_signal_generator import (
    RawSignalGenerator,
)


def run(strategy_name):


    print("=" * 80)

    print(
        f"Running capacity analysis: {strategy_name}"
    )

    print("=" * 80)



    config = get_strategy(
        strategy_name
    )


    df = pd.read_parquet(
        config["signal_input"]
    )



    generator = RawSignalGenerator(
        strategy_name
    )


    signals = generator.generate(
        df
    )



    print(
        f"Raw opportunities: {len(signals)}"
    )



    analyzer = StrategyCapacityAnalyzer(
        signals
    )



    result = analyzer.analyze()



    print()

    print(
        "Capacity Result"
    )

    print("-" * 80)

    print(
        result
    )



    output = Path(
        "research/reports"
    )


    output.mkdir(
        parents=True,
        exist_ok=True,
    )


    result.to_csv(
        output
        /
        f"{strategy_name}_capacity_analysis_v1_0.csv",
        index=False,
        encoding="utf-8-sig",
    )



    print()

    print(
        "Saved:"
    )

    print(
        output
        /
        f"{strategy_name}_capacity_analysis_v1_0.csv"
    )





if __name__ == "__main__":


    if len(sys.argv) < 2:

        raise ValueError(
            "Please provide strategy name"
        )


    run(
        sys.argv[1]
    )