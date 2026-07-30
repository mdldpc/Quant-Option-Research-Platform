import sys
from pathlib import Path


# ==================================================
# Add project root to Python path
# ==================================================

ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(ROOT)
)



import pandas as pd


from framework.strategy.strategy_registry import (
    get_strategy,
)


# ==========================================================
# Generate raw executable signals
# Mimic actual SignalGenerator logic
# ==========================================================

def generate_raw_signals(
    strategy_name,
    df,
):

    df = df.copy()



    # ==================================================
    # Long ATM Strangle
    # ==================================================

    if strategy_name == "long_atm_strangle":


        signals = df[
            df["long_signal"] == 1
        ].copy()


        signals["entry_idx"] = (
            signals.index
        )


        signals["exit_idx"] = (
            signals["entry_idx"]
            +
            5
        )


        signals = signals.sort_values(
            "entry_idx"
        ).reset_index(drop=True)


        return signals



    # ==================================================
    # Long Call Butterfly
    # ==================================================

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
        ).reset_index(drop=True)



        daily["trade_idx"] = (
            daily.index
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



        trades = []


        in_position = False

        entry_idx = None



        for i,row in daily.iterrows():


            if not in_position:


                if (
                    row["butterfly_zscore"]
                    <= -1
                ):

                    in_position = True

                    entry_idx = i


                continue



            holding_days = (
                i - entry_idx
            )


            exit_reason = None



            if (
                row["butterfly_zscore"]
                >= 0
            ):

                exit_reason = "zscore_exit"



            if holding_days >= 10:

                exit_reason = "max_holding"



            if i == len(daily)-1:

                exit_reason = "end_of_data"



            if exit_reason is not None:


                trades.append(
                    {

                        "entry_idx":
                            entry_idx,


                        "exit_idx":
                            i,


                        "exit_reason":
                            exit_reason,

                    }
                )


                in_position = False

                entry_idx = None



        return pd.DataFrame(trades)



    # ==================================================
    # Calendar Spread
    # ==================================================

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


        daily["trade_date_dt"] = pd.to_datetime(
            daily["trade_date"]
            .astype(str)
        )


        daily = daily.sort_values(
            "trade_date_dt"
        ).reset_index(drop=True)



        daily["trade_idx"] = (
            daily.index
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



        trades = []


        in_position = False

        entry_idx = None



        for i,row in daily.iterrows():


            if not in_position:


                if (
                    row["iv_spread_zscore"]
                    <= -1
                ):

                    in_position = True

                    entry_idx = i


                continue



            holding_days = (
                i - entry_idx
            )


            exit_reason = None



            if (
                row["iv_spread_zscore"]
                >= 0
            ):

                exit_reason = "zscore_exit"



            if holding_days >= 10:

                exit_reason = "max_holding"



            if i == len(daily)-1:

                exit_reason = "end_of_data"



            if exit_reason is not None:


                trades.append(
                    {

                        "entry_idx":
                            entry_idx,


                        "exit_idx":
                            i,


                        "exit_reason":
                            exit_reason,

                    }
                )


                in_position = False

                entry_idx = None



        return pd.DataFrame(trades)



    else:

        raise ValueError(
            f"Unknown strategy: {strategy_name}"
        )





# ==========================================================
# Non-overlap simulation
# ==========================================================

def simulate_non_overlap(
    signals
):

    if len(signals) == 0:

        return signals



    signals = (
        signals
        .sort_values(
            "entry_idx"
        )
        .reset_index(drop=True)
    )


    selected = []


    current_exit = None



    for _,row in signals.iterrows():


        entry = row["entry_idx"]

        exit_ = row["exit_idx"]



        if current_exit is None:


            selected.append(row)

            current_exit = exit_

            continue



        if entry >= current_exit:


            selected.append(row)

            current_exit = exit_



    if len(selected):

        return pd.DataFrame(selected)


    return pd.DataFrame(
        columns=signals.columns
    )





# ==========================================================
# Main consistency check
# ==========================================================

def check_strategy(
    strategy_name
):

    print("=" * 80)

    print(
        f"Checking: {strategy_name}"
    )

    print("=" * 80)



    config = get_strategy(
        strategy_name
    )


    df = pd.read_parquet(
        config["signal_input"]
    )



    # Actual generator

    generator = (
        config["signal_generator"]()
    )


    actual = generator.generate(
        df
    )



    # Raw simulator

    raw = generate_raw_signals(
        strategy_name,
        df,
    )


    executable = simulate_non_overlap(
        raw
    )



    print()

    print(
        "Actual generated signals:"
    )

    print(
        len(actual)
    )



    print()

    print(
        "Raw overlap executable:"
    )

    print(
        len(executable)
    )



    diff = (
        len(actual)
        -
        len(executable)
    )



    print()

    print(
        "Difference:"
    )

    print(
        diff
    )



    print()


    if diff == 0:

        print(
            "STATUS: PASS"
        )

    else:

        print(
            "STATUS: NEED REVIEW"
        )





if __name__ == "__main__":


    strategies = [

        "long_atm_strangle",

        "long_call_butterfly",

        "calendar_spread",

    ]


    for s in strategies:

        check_strategy(s)
