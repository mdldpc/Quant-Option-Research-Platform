import pandas as pd

from portfolio_all.portfolio_analysis.portfolio_optimizer import (
    PortfolioOptimizer
)



def test_minimum_variance():


    returns = pd.DataFrame(

        {

            "strategy_a":
            [
                0.01,
                0.02,
                -0.01,
                0.03,
            ],


            "strategy_b":
            [
                0.005,
                0.01,
                0.002,
                0.008,
            ],


            "strategy_c":
            [
                -0.01,
                0.02,
                0.01,
                0.015,
            ],

        }

    )



    optimizer = PortfolioOptimizer(
        returns
    )


    weights = (
        optimizer
        .minimum_variance()
    )


    assert abs(
        weights.sum()-1
    ) < 1e-8



    assert (
        weights >= 0
    ).all()

def test_maximum_sharpe():


    returns = pd.DataFrame(

        {

            "strategy_a":
            [
                0.01,
                0.02,
                -0.01,
                0.03,
            ],


            "strategy_b":
            [
                0.005,
                0.01,
                0.002,
                0.008,
            ],


            "strategy_c":
            [
                -0.01,
                0.02,
                0.01,
                0.015,
            ],

        }

    )


    optimizer = PortfolioOptimizer(
        returns
    )


    weights = (
        optimizer
        .maximum_sharpe()
    )


    assert abs(
        weights.sum()-1
    ) < 1e-8


    assert (
        weights >= 0
    ).all()


    assert len(weights) == 3

def test_risk_parity():


    returns = pd.DataFrame(

        {

            "strategy_a":
            [
                0.01,
                0.02,
                -0.01,
                0.03,
            ],


            "strategy_b":
            [
                0.005,
                0.01,
                0.002,
                0.008,
            ],


            "strategy_c":
            [
                -0.01,
                0.02,
                0.01,
                0.015,
            ],

        }

    )


    optimizer = PortfolioOptimizer(
        returns
    )


    weights = (
        optimizer
        .risk_parity()
    )


    assert abs(
        weights.sum()-1
    ) < 1e-8


    assert (
        weights >= 0
    ).all()


    assert len(weights) == 3