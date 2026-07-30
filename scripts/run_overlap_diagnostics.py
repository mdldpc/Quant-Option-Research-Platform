from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)


from analysis.overlap_diagnostics import (
    OverlapDiagnostics,
)



def run(strategy_name):


    print("=" * 80)

    print(
        f"Running overlap diagnostics: {strategy_name}"
    )

    print("=" * 80)



    config = get_strategy(
        strategy_name
    )



    signal_generator_cls = config[
        "signal_generator"
    ]


    df = pd.read_parquet(
        config["signal_input"]
    )


    generator = signal_generator_cls()


    signals = generator.generate(
        df
    )


    print()

    print(
        "Generated signals:",
        len(signals)
    )



    if len(signals)==0:

        print(
            "No signals."
        )

        return



    diagnostics = OverlapDiagnostics(
        signals
    )


    result = diagnostics.summary()



    print()

    print(
        "Overlap Summary"
    )

    print("-"*80)


    for k,v in result.items():

        print(
            f"{k}: {v}"
        )



    output = Path(
        "research/reports/"
        f"{strategy_name}_overlap_diagnostics_v1_0.csv"
    )


    pd.DataFrame(
        [result]
    ).to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )


    print()

    print(
        "Saved:"
    )

    print(output)



if __name__=="__main__":


    if len(sys.argv)<2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_overlap_diagnostics.py strategy_name"
        )

        sys.exit(1)


    run(
        sys.argv[1]
    )