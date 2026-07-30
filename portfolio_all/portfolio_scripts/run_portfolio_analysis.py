from pathlib import Path
import sys


sys.path.append(".")


import pandas as pd


from analysis.portfolio_metrics import (
    PortfolioMetrics,
)



def main():


    input_file = Path(
        "research/portfolio/"
        "strategy_return_matrix_v1_0.csv"
    )


    print("="*80)

    print(
        "Running Portfolio Analysis"
    )

    print("="*80)



    print("\nLoading:")

    print(input_file)



    returns = pd.read_csv(
        input_file
    )


    print(
        "\nRows:",
        len(returns)
    )



    metrics = PortfolioMetrics(
        returns
    )



    # ---------------------------------
    # Correlation
    # ---------------------------------

    corr = (
        metrics
        .correlation_matrix()
    )


    corr_file = Path(
        "research/portfolio/"
        "correlation_matrix_v1_0.csv"
    )


    corr.to_csv(
        corr_file
    )



    # ---------------------------------
    # Covariance
    # ---------------------------------

    cov = (
        metrics
        .covariance_matrix()
    )


    cov_file = Path(
        "research/portfolio/"
        "covariance_matrix_v1_0.csv"
    )


    cov.to_csv(
        cov_file
    )



    # ---------------------------------
    # Volatility
    # ---------------------------------

    vol = (
        metrics
        .volatility()
        .to_frame(
            "annual_volatility"
        )
    )


    vol_file = Path(
        "research/portfolio/"
        "volatility_v1_0.csv"
    )


    vol.to_csv(
        vol_file
    )



    # ---------------------------------
    # Equal weight portfolio
    # ---------------------------------

    summary = (
        metrics
        .equal_weight_performance()
        .to_frame(
            "value"
        )
    )


    summary_file = Path(
        "research/portfolio/"
        "portfolio_summary_v1_0.csv"
    )


    summary.to_csv(
        summary_file
    )



    print("\nCorrelation Matrix")

    print("----------------")

    print(corr)



    print("\nVolatility")

    print("----------------")

    print(vol)



    print("\nEqual Weight Portfolio")

    print("----------------")

    print(summary)



    print("\nSaved:")

    print(corr_file)

    print(cov_file)

    print(vol_file)

    print(summary_file)



if __name__ == "__main__":

    main()