import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
from analysis.experiments import (
    threshold_experiment,
    holding_experiment,
    cost_experiment,
)


def main():

    # 用你真实数据
    df = pd.read_parquet(
        r"D:\Quant_Option_Project\research\backtest\option_strategy_backtest_v2.parquet"
    )

    print("\nThreshold:")
    print(threshold_experiment(df, 80))

    print("\nHolding:")
    print(holding_experiment(df, 5))

    print("\nCost:")
    print(cost_experiment(df, 0.001))


if __name__ == "__main__":
    main()