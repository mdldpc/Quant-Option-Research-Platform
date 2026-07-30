from pathlib import Path
import pandas as pd
import sys


sys.path.append(".")


from analysis.trade_performance_adapter import (
    TradePerformanceAdapter,
)


from analysis.strategy_evaluation import (
    StrategyEvaluator,
)



EXPORT_DIR = Path(
    "research/exports"
)


REPORT_DIR = Path(
    "research/reports"
)



STRATEGY_FILES = {


    "long_atm_strangle":
    "option_strategy_backtest_strangle_v1_1.csv",


    "long_call_butterfly":
    "option_strategy_backtest_butterfly_v1_1.csv",


    "calendar_spread":
    "option_strategy_backtest_calendar_v1_1.csv",

}



def evaluate_strategy(
    strategy_name,
    filename,
):


    path = (
        EXPORT_DIR
        /
        filename
    )


    print("\n" + "="*80)

    print(
        strategy_name
    )

    print(
        "Loading:",
        path
    )



    trades = pd.read_csv(
        path
    )


    print(
        "Trades:",
        len(trades)
    )



    performance = (
        TradePerformanceAdapter
        .adapt(
            trades
        )
    )



    evaluator = StrategyEvaluator(
        performance
    )


    result = (
        evaluator
        .evaluate()
    )


    result["strategy"] = (
        strategy_name
    )


    return result



def run():


    results = []


    for strategy, file in STRATEGY_FILES.items():


        result = evaluate_strategy(
            strategy,
            file,
        )


        results.append(
            result
        )



    comparison = pd.DataFrame(
        results
    )



    columns = [

        "strategy",

        "total_trades",

        "win_rate",

        "average_return",

        "total_return",

        "volatility",

        "sharpe_ratio",

        "max_drawdown",

        "profit_factor",

        "average_holding_days",

    ]


    comparison = comparison[
        columns
    ]



    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    output = (
        REPORT_DIR
        /
        "strategy_comparison_v1_0.csv"
    )


    comparison.to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )


    print("\n" + "="*80)

    print(
        "Strategy Comparison"
    )

    print(
        comparison
    )


    print(
        "\nSaved:"
    )

    print(
        output
    )



if __name__ == "__main__":

    run()