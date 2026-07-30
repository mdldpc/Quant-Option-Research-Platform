import pandas as pd


from analysis.strategy_evaluation import (
    StrategyEvaluator,
)



def create_test_dataframe():

    return pd.DataFrame(

        {

            "return":
            [
                0.10,
                -0.05,
                0.20,
                -0.10,
            ],


            "holding_days":
            [
                5,
                3,
                7,
                4,
            ]

        }

    )



def test_basic_evaluation():


    df = create_test_dataframe()


    evaluator = StrategyEvaluator(
        df
    )


    result = evaluator.evaluate()



    assert (
        result["total_trades"]
        == 4
    )


    assert (
        result["winning_trades"]
        == 2
    )


    assert (
        result["losing_trades"]
        == 2
    )


    assert (
        result["win_rate"]
        == 0.5
    )



def test_risk_metrics():


    df = create_test_dataframe()


    result = StrategyEvaluator(
        df
    ).evaluate()



    assert (
        "total_return"
        in result
    )


    assert (
        "volatility"
        in result
    )


    assert (
        "sharpe_ratio"
        in result
    )


    assert (
        "max_drawdown"
        in result
    )


    assert (
        "profit_factor"
        in result
    )



    assert (
        result["profit_factor"]
        > 0
    )

def test_extended_metrics():


    df = create_test_dataframe()


    result = StrategyEvaluator(
        df
    ).evaluate()



    assert (
        "sortino_ratio"
        in result
    )


    assert (
        "skewness"
        in result
    )


    assert (
        "kurtosis"
        in result
    )


    assert (
        "recovery_time"
        in result
    )