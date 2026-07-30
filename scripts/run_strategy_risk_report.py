from pathlib import Path
import sys

sys.path.append(".")


import pandas as pd


from analysis.strategy_risk_report import (
    StrategyRiskReport,
)



def main():


    print("="*80)

    print(
        "Running Strategy Risk Report"
    )

    print("="*80)



    # ---------------------------------
    # Load return matrix
    # ---------------------------------

    return_file = Path(

        "research/portfolio/"
        "strategy_return_matrix_v1_0.csv"

    )


    print("\nLoading return matrix:")

    print(return_file)



    returns = pd.read_csv(

        return_file

    )



    # ---------------------------------
    # Trade files
    # ---------------------------------

    trade_files = {


        "long_atm_strangle":

        "research/exports/"
        "option_strategy_backtest_strangle_v1_1.csv",



        "long_call_butterfly":

        "research/exports/"
        "option_strategy_backtest_butterfly_v1_1.csv",



        "calendar_spread":

        "research/exports/"
        "option_strategy_backtest_calendar_v1_1.csv",

    }



    report_builder = StrategyRiskReport(

        returns,

        trade_files,

    )



    report = report_builder.generate()



    print("\nStrategy Risk Report")

    print("-"*80)

    print(report)



    output = Path(

        "research/portfolio/"
        "strategy_risk_report_v1_1.csv"

    )


    output.parent.mkdir(

        parents=True,

        exist_ok=True

    )


    report.to_csv(

        output,

        index=False,

        encoding="utf-8-sig"

    )


    print("\nSaved:")

    print(output)



if __name__ == "__main__":

    main()