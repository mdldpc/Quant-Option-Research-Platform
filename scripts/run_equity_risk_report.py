from pathlib import Path
import sys

sys.path.append(".")


from analysis.equity_risk_report import (
    EquityRiskReport,
)



def main():


    print("="*80)

    print(
        "Running Equity Risk Report"
    )

    print("="*80)



    equity_files = {


        "long_atm_strangle":

        "research/portfolio/"
        "equity_curves/"
        "long_atm_strangle_equity_v1_0.csv",



        "long_call_butterfly":

        "research/portfolio/"
        "equity_curves/"
        "long_call_butterfly_equity_v1_0.csv",



        "calendar_spread":

        "research/portfolio/"
        "equity_curves/"
        "calendar_spread_equity_v1_0.csv",

    }



    report = EquityRiskReport(

        equity_files

    )


    result = report.generate()



    print("\nEquity Risk Report")

    print("-"*80)

    print(result)



    output = Path(

        "research/portfolio/"
        "strategy_risk_report_v1_2.csv"

    )


    result.to_csv(

        output,

        index=False,

        encoding="utf-8-sig"

    )


    print("\nSaved:")

    print(output)



if __name__ == "__main__":

    main()