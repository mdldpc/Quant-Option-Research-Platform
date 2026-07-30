import pandas as pd


from portfolio_all.portfolio_analysis.portfolio_performance import (
    PortfolioPerformance
)



def create_returns():


    return pd.DataFrame(

        {

            "strategy_a":
            [
                0.01,
                0.02,
                -0.01,
            ],


            "strategy_b":
            [
                0.005,
                -0.01,
                0.02,
            ],


            "strategy_c":
            [
                0.0,
                0.01,
                0.015,
            ],

        }

    )



def test_daily_return():


    returns = create_returns()


    weights = pd.Series(

        {

            "strategy_a":0.4,

            "strategy_b":0.4,

            "strategy_c":0.2,

        }

    )


    engine = PortfolioPerformance(

        returns,

        weights

    )


    result = (

        engine

        .calculate_daily_return()

    )


    assert len(result)==3



def test_equity_curve():


    returns = create_returns()


    weights = pd.Series(

        {

            "strategy_a":0.4,

            "strategy_b":0.4,

            "strategy_c":0.2,

        }

    )


    engine = PortfolioPerformance(

        returns,

        weights

    )


    curve = (

        engine

        .calculate_equity_curve()

    )


    assert "equity" in curve.columns


    assert (

        curve["equity"].iloc[0]

        >

        0

    )