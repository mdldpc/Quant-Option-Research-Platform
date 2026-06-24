import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
from analysis.parameter_sweep import run_parameter_sweep


# fake backtest function（先测试框架）
def fake_backtest(data, threshold):

    # 模拟：threshold越高，收益越低（只是测试）
    return {
        "avg_return": 0.1 - threshold / 1000,
        "sharpe": 1.5 - threshold / 200,
    }


def main():

    df = pd.DataFrame({"dummy": [1, 2, 3]})

    result = run_parameter_sweep(
        base_data=df,
        param_name="threshold",
        values=[70, 75, 80, 85],
        run_func=fake_backtest,
    )

    print("\nFinal result:")
    print(result)


if __name__ == "__main__":
    main()