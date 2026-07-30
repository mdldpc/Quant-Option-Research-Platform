from pathlib import Path
import sys


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)


from analysis.signal_backtest_sensitivity import (
    SignalBacktestSensitivity,
)



def run(strategy_name):


    print("="*80)

    print(
        "Running:",
        strategy_name
    )

    print("="*80)



    config = get_strategy(
        strategy_name
    )


    analyzer = SignalBacktestSensitivity(
        config
    )



    if config["signal_direction"]=="negative":

        thresholds=[
            -3,
            -2.5,
            -2,
            -1.5,
            -1,
        ]

    else:

        thresholds=[
            50,
            60,
            70,
            80,
            90,
        ]



    result = analyzer.analyze(
        thresholds
    )


    print(result)



    output = Path(
        "research/reports/"
        +
        strategy_name
        +
        "_backtest_sensitivity_v1_1.csv"
    )


    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    result.to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )


    print(
        "Saved:"
    )

    print(output)



if __name__=="__main__":


    run(
        sys.argv[1]
    )