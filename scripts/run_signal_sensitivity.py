from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)


from analysis.signal_sensitivity import (
    SignalSensitivity,
)



OUTPUT_DIR = Path(
    "research/reports"
)



def run(strategy_name):


    print("="*80)

    print(
        f"Running sensitivity: {strategy_name}"
    )

    print("="*80)



    config = get_strategy(
        strategy_name
    )


    signal_input = config[
        "signal_input"
    ]


    print(
        "\nLoading:"
    )

    print(
        signal_input
    )


    df = pd.read_parquet(
        signal_input
    )


    generator = config[
        "signal_generator"
    ]()


    signals = generator.generate(
        df
    )


    print(
        "Generated signals:",
        len(signals)
    )



    score_column = config[
        "signal_score_column"
    ]


    direction = config[
        "signal_direction"
    ]



    analyzer = SignalSensitivity(

        signals,

        score_column,

        direction,

    )


    if direction == "negative":

        thresholds = [
            -3,
            -2.5,
            -2,
            -1.5,
            -1,
            -0.5,
            0,
        ]

    else:

        thresholds = [
            30,
            40,
            50,
            60,
            70,
            80,
            90,
        ]



    result = analyzer.analyze(
        thresholds
    )


    print(
        "\nSensitivity Result"
    )

    print("-"*80)

    print(
        result
    )



    output = OUTPUT_DIR / (
        strategy_name
        +
        "_signal_sensitivity_v1_0.csv"
    )


    analyzer.save(
        result,
        output,
    )


    print("\nSaved:")

    print(output)



if __name__ == "__main__":


    if len(sys.argv)<2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_signal_sensitivity.py strategy_name"
        )

        sys.exit(1)



    run(
        sys.argv[1]
    )