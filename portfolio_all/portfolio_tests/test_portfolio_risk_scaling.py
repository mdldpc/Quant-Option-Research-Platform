import pandas as pd


from portfolio_all.portfolio_analysis.portfolio_risk_scaling import (
    PortfolioRiskScaler
)



def test_scaling_factor():


    returns = pd.Series(

        [

            0.01,

            -0.02,

            0.03,

            -0.01,

            0.02,

        ]

    )


    scaler = PortfolioRiskScaler(

        returns,

        target_volatility=0.15

    )


    factor = (

        scaler

        .scaling_factor()

    )


    assert factor > 0



def test_scaled_volatility():


    returns = pd.Series(

        [

            0.01,

            -0.02,

            0.03,

            -0.01,

            0.02,

        ]

    )


    scaler = PortfolioRiskScaler(

        returns,

        target_volatility=0.15

    )


    scaled = (

        scaler

        .scale_returns()

    )


    vol = (

        scaled.std()

        *

        252**0.5

    )


    assert abs(

        vol-0.15

    ) < 1e-10