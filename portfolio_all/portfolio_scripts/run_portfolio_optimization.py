"""
Portfolio Optimization Runner v1.1

Pipeline:

Strategy Return Matrix
        |
        v
Portfolio Allocation
        |
        v
Portfolio Weights

        |
        +----------------+
        |                |
        v                v

Raw Portfolio      Risk Scaled Portfolio

        |
        v

Performance Comparison


Outputs:

1. portfolio weights
2. raw equity curves
3. scaled equity curves
4. comparison report

"""


import os

import pandas as pd


from portfolio_all.portfolio_analysis.portfolio_allocation import (
    PortfolioAllocator,
)


from portfolio_all.portfolio_analysis.portfolio_performance import (
    PortfolioPerformance,
)


from portfolio_all.portfolio_analysis.portfolio_risk_scaling import (
    PortfolioRiskScaler,
)



# =====================================================
# Configuration
# =====================================================


INPUT_FILE = (

    "research/portfolio/"
    "strategy_return_matrix_v1_0.csv"

)


OUTPUT_DIR = (

    "research/portfolio/results"

)


TARGET_VOLATILITY = 0.15



os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)



# =====================================================
# Load Return Matrix
# =====================================================


print("=" * 80)

print(
    "Running Portfolio Optimization v1.1"
)

print("=" * 80)



print("\nLoading:")

print(INPUT_FILE)



returns = pd.read_csv(
    INPUT_FILE
)



print("\nReturn Matrix")

print(
    returns.head()
)



# -----------------------------------------------------
# Keep only strategy return columns
# -----------------------------------------------------

if "trade_date" in returns.columns:

    strategy_returns = (

        returns

        .drop(
            columns=[
                "trade_date"
            ]
        )

    )

else:

    strategy_returns = returns.copy()



# =====================================================
# Portfolio Allocation
# =====================================================


allocator = PortfolioAllocator(

    strategy_returns

)



allocation_table = (

    allocator

    .generate_allocation_table()

)



print("\nPortfolio Weights")

print("-" * 80)

print(
    allocation_table
)



weights_file = os.path.join(

    OUTPUT_DIR,

    "portfolio_weights_v1_1.csv"

)



allocation_table.to_csv(

    weights_file

)



print("\nSaved:")

print(weights_file)



# =====================================================
# Portfolio Performance
# =====================================================


methods = [

    "equal_weight",

    "minimum_variance",

    "maximum_sharpe",

    "risk_parity",

]



comparison_results = []



for method in methods:


    print("\n")

    print("=" * 80)

    print(method)

    print("=" * 80)



    weights = (

        allocation_table[method]

    )



    # ---------------------------------
    # Raw Portfolio
    # ---------------------------------


    performance = PortfolioPerformance(

        strategy_returns,

        weights,

    )


    raw_equity = (

        performance

        .calculate_equity_curve()

    )


    raw_metrics = (

        performance

        .summary()

    )


    raw_metrics["portfolio"] = method

    raw_metrics["type"] = "raw"



    comparison_results.append(

        raw_metrics

    )



    raw_file = os.path.join(

        OUTPUT_DIR,

        f"{method}_raw_equity_v1_1.csv"

    )


    raw_equity.to_csv(

        raw_file

    )



    print("\nRaw Equity Saved:")

    print(raw_file)



    # ---------------------------------
    # Risk Scaled Portfolio
    # ---------------------------------


    raw_returns = (

        performance

        .calculate_daily_return()

    )



    scaler = PortfolioRiskScaler(

        raw_returns,

        target_volatility=TARGET_VOLATILITY,

    )



    scaled_equity = (

        scaler

        .equity_curve()

    )


    scaled_metrics = (

        scaler

        .summary()

    )



    scaled_metrics["portfolio"] = method

    scaled_metrics["type"] = "scaled"



    comparison_results.append(

        scaled_metrics

    )



    scaled_file = os.path.join(

        OUTPUT_DIR,

        f"{method}_scaled_equity_v1_1.csv"

    )



    scaled_equity.to_csv(

        scaled_file

    )



    print("\nScaled Equity Saved:")

    print(scaled_file)



# =====================================================
# Comparison Report
# =====================================================


comparison = pd.DataFrame(

    comparison_results

)



comparison = comparison[

    [

        "portfolio",

        "type",

        "total_return",

        "annual_return",

        "volatility",

        "sharpe_ratio",

        "max_drawdown",

        "scaling_factor",

    ]

]



print("\n")

print("=" * 80)

print("Portfolio Comparison")

print("=" * 80)


print(

    comparison

)



report_file = os.path.join(

    OUTPUT_DIR,

    "portfolio_comparison_v1_1.csv"

)



comparison.to_csv(

    report_file,

    index=False

)



print("\nSaved:")

print(report_file)