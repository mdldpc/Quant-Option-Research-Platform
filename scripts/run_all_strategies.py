from pathlib import Path
import sys


sys.path.append(".")


from framework.strategy.strategy_registry import (
    list_strategies,
)

from scripts.run_strategy import (
    run_strategy,
)

from analysis.strategy_comparison import (
    StrategyComparison,
)


# 这里先留一个容器
# 后续需要让 run_strategy 返回 result


def main():

    results = []


    for strategy in list_strategies():

        print("\n")
        print("#" * 100)

        print(
            f"Running {strategy}"
        )

        print("#" * 100)


        result = run_strategy(
            strategy
        )


        results.append(
            result
        )


    comparison = StrategyComparison(
        results
    )


    comparison.save(
        csv_path=Path(
            "research/reports/strategy_comparison_v1_3.csv"
        ),

        report_path=Path(
            "research/reports/strategy_comparison_v1_3.txt"
        ),
    )


if __name__ == "__main__":

    main()