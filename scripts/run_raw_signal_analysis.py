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


from analysis.raw_signal_generator import (
    RawSignalGenerator,
)



def run(strategy_name):


    print("="*80)

    print(
        f"Running raw signal analysis: {strategy_name}"
    )

    print("="*80)



    config = get_strategy(
        strategy_name
    )



    df = pd.read_parquet(
        config["signal_input"]
    )


    print(
        f"Feature rows: {len(df)}"
    )



    generator = RawSignalGenerator(
        strategy_name
    )



    signals = generator.generate(
        df
    )


    print()

    print(
        "Raw opportunities:"
    )

    print(
        len(signals)
    )



    print()

    print(
        signals.head()
    )



    output = Path(
        "research/reports"
    )


    output.mkdir(
        parents=True,
        exist_ok=True,
    )



    signals.to_csv(

        output
        /
        f"{strategy_name}_raw_signal_v1_0.csv",

        index=False,

        encoding="utf-8-sig"

    )



    print()

    print(
        "Saved:"
    )

    print(
        output
        /
        f"{strategy_name}_raw_signal_v1_0.csv"
    )




if __name__ == "__main__":


    run(
        sys.argv[1]
    )