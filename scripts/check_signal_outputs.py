import sys

sys.path.append(".")

import pandas as pd

from framework.strategy.strategy_registry import get_strategy


strategies = [
    "long_atm_strangle",
    "long_call_butterfly",
    "calendar_spread",
]


for name in strategies:

    print("=" * 80)
    print(name)
    print("=" * 80)

    config = get_strategy(name)

    df = pd.read_parquet(
        config["signal_input"]
    )

    print("Feature rows:", len(df))


    generator = config["signal_generator"]()


    signals = generator.generate(
        df
    )


    print("Generated signals:", len(signals))

    print("\nColumns:")
    print(
        signals.columns.tolist()
    )


    print("\nHead:")
    print(
        signals.head()
    )

    print("\n")