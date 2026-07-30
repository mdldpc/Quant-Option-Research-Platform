from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")


from framework.strategy.strategy_registry import (
    get_strategy,
)


from analysis.raw_signal_overlap import (
    RawSignalOverlapDiagnostics,
)



def generate_raw_signals(strategy_name, df):


    df = df.copy()


    # =====================================
    # Long ATM Strangle
    # =====================================

    if strategy_name == "long_atm_strangle":


        signals = df[
            df["long_signal"] == 1
        ].copy()


        signals["entry_date"] = pd.to_datetime(
            signals["trade_date"].astype(str)
        )


        signals["exit_date"] = (
            signals["entry_date"]
            +
            pd.Timedelta(days=5)
        )


        return signals



    # =====================================
    # Butterfly
    # =====================================

    elif strategy_name == "long_call_butterfly":


        daily = (
            df
            .groupby(
                "trade_date",
                as_index=False,
            )
            .agg(
                butterfly_price=(
                    "butterfly_price",
                    "mean",
                )
            )
        )


        daily = daily.sort_values(
            "trade_date"
        )


        daily["mean"] = (
            daily["butterfly_price"]
            .rolling(20)
            .mean()
        )


        daily["std"] = (
            daily["butterfly_price"]
            .rolling(20)
            .std()
        )


        daily["butterfly_zscore"] = (

            (
                daily["butterfly_price"]
                -
                daily["mean"]
            )

            /

            daily["std"]

        )


        signals = daily[
            daily["butterfly_zscore"]
            <= -1
        ].copy()



        signals["entry_date"] = pd.to_datetime(
            signals["trade_date"].astype(str)
        )


        signals["exit_date"] = (
            signals["entry_date"]
            +
            pd.Timedelta(days=10)
        )


        return signals



    # =====================================
    # Calendar Spread
    # =====================================

    elif strategy_name == "calendar_spread":


        daily = (
            df
            .groupby(
                "trade_date",
                as_index=False,
            )
            .agg(
                iv_spread=(
                    "iv_spread",
                    "mean",
                )
            )
        )


        daily = daily.sort_values(
            "trade_date"
        )



        daily["mean"] = (
            daily["iv_spread"]
            .rolling(20)
            .mean()
        )


        daily["std"] = (
            daily["iv_spread"]
            .rolling(20)
            .std()
        )


        daily["iv_spread_zscore"] = (

            (
                daily["iv_spread"]
                -
                daily["mean"]
            )

            /

            daily["std"]

        )


        signals = daily[
            daily["iv_spread_zscore"]
            <= -1
        ].copy()



        signals["entry_date"] = pd.to_datetime(
            signals["trade_date"].astype(str)
        )


        signals["exit_date"] = (
            signals["entry_date"]
            +
            pd.Timedelta(days=10)
        )


        return signals



    else:

        raise ValueError(
            f"Unknown strategy: {strategy_name}"
        )



def run(strategy_name):


    print("="*80)

    print(
        f"Running raw overlap diagnostics: {strategy_name}"
    )

    print("="*80)



    config = get_strategy(
        strategy_name
    )


    df = pd.read_parquet(
        config["signal_input"]
    )


    print(
        "Feature rows:",
        len(df)
    )



    signals = generate_raw_signals(
        strategy_name,
        df,
    )


    print(
        "Raw opportunities:",
        len(signals)
    )



    if len(signals)==0:

        return



    diagnostics = RawSignalOverlapDiagnostics(
        signals
    )


    result = diagnostics.summary()



    print()

    print(
        "Overlap Summary"
    )

    print("-"*80)


    for k,v in result.items():

        print(
            f"{k}: {v}"
        )



    output = Path(
        "research/reports/"
        +
        strategy_name
        +
        "_raw_overlap_diagnostics_v1_1.csv"
    )


    pd.DataFrame(
        [result]
    ).to_csv(
        output,
        index=False,
        encoding="utf-8-sig",
    )


    print()

    print(
        "Saved:"
    )

    print(output)



if __name__=="__main__":


    if len(sys.argv)<2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_raw_overlap_diagnostics.py strategy_name"
        )

        sys.exit(1)


    run(
        sys.argv[1]
    )