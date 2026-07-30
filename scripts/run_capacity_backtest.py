from pathlib import Path
import sys

import pandas as pd


sys.path.append(".")



from analysis.raw_signal_generator import (
    RawSignalGenerator,
)


from analysis.capacity_executor import (
    CapacityExecutor,
)


from analysis.capacity_signal_adapter import (
    CapacitySignalAdapter,
)


from framework.strategy.strategy_registry import (
    get_strategy,
)



from framework.strategy.trade_constructor import (
    StrangleTradeConstructor,
    ButterflyTradeConstructor,
    CalendarTradeConstructor,
)



from framework.strategy.backtesters.strangle import (
    StrangleBacktester,
)

from framework.strategy.backtesters.butterfly import (
    ButterflyBacktester,
)

from framework.strategy.backtesters.calendar import (
    CalendarBacktester,
)





CONSTRUCTOR_MAP = {

    "long_atm_strangle":
        StrangleTradeConstructor,


    "long_call_butterfly":
        ButterflyTradeConstructor,


    "calendar_spread":
        CalendarTradeConstructor,

}





BACKTESTER_MAP = {

    "long_atm_strangle":
        StrangleBacktester,


    "long_call_butterfly":
        ButterflyBacktester,


    "calendar_spread":
        CalendarBacktester,

}





def run_capacity_backtest(
    strategy_name
):


    print("=" * 80)

    print(
        f"Running capacity backtest: {strategy_name}"
    )

    print("=" * 80)



    config = get_strategy(
        strategy_name
    )



    # ==================================================
    # 1. Load feature input
    # ==================================================

    feature_path = config[
        "signal_input"
    ]


    print("\nLoading feature:")

    print(feature_path)



    df = pd.read_parquet(
        feature_path
    )


    print(
        "Feature rows:",
        len(df)
    )



    # ==================================================
    # 2. Generate RAW opportunities
    # ==================================================

    raw_generator = RawSignalGenerator(
        strategy_name
    )
    
    raw_signals = raw_generator.generate(
        df,
    )


    print(
        "\nRaw opportunities:",
        len(raw_signals)
    )



    if raw_signals.empty:

        print(
            "No raw signals."
        )

        return



    results = []



    # ==================================================
    # 3. Capacity loop
    # ==================================================

    for capacity in [

        1,
        2,
        3,
        None,

    ]:


        print(
            "\nTesting capacity:",
            capacity
        )



        executor = CapacityExecutor(

            raw_signals,

            capacity=capacity,

        )



        selected = executor.execute()



        print(
            "Executable signals:",
            len(selected)
        )



        if selected.empty:

            results.append(

                {

                "capacity":
                    capacity,

                "trades":
                    0,

                "final_equity":
                    None,

                }

            )

            continue



        # ==================================================
        # 4. Convert raw signal format
        # ==================================================

        signals = CapacitySignalAdapter.adapt(

            selected,

            strategy_name,

        )



        # ==================================================
        # 5. Load snapshot
        # ==================================================

        snapshot = pd.read_parquet(

            config["snapshot"]

        )



        # ==================================================
        # 6. Trade construction
        # ==================================================

        constructor = (

            CONSTRUCTOR_MAP[
                strategy_name
            ]

        )(

            snapshot

        )


        trades = constructor.build_all(

            signals

        )



        # ==================================================
        # 7. Backtest
        # ==================================================

        backtester = (

            BACKTESTER_MAP[
                strategy_name
            ]

        )(

            trades

        )


        report_path = Path(

            "research/reports"

        ) / (

            f"{strategy_name}_capacity_{capacity}_report.txt"

        )


        trade_path = Path(

            "research/exports"

        ) / (

            f"{strategy_name}_capacity_{capacity}_trades.csv"

        )


        result = backtester.backtest(

            report_path=report_path,

            trades_path=trade_path,

        )



        results.append(

            {

            "capacity":
                capacity,

            "trades":
                result.total_trades,

            "win_rate":
                result.win_rate,

            "final_equity":
                result.final_equity,

            "max_drawdown":
                result.max_drawdown,

            }

        )




    # ==================================================
    # 8. Save result
    # ==================================================

    result_df = pd.DataFrame(
        results
    )


    print("\nCapacity Backtest Result")

    print("-"*80)

    print(
        result_df
    )



    output = Path(

        "research/reports"

    ) / (

        f"{strategy_name}_capacity_backtest_v1_1.csv"

    )


    result_df.to_csv(

        output,

        index=False,

    )


    print("\nSaved:")

    print(output)





if __name__ == "__main__":


    if len(sys.argv)<2:

        print(
            "Usage:"
        )

        print(
            "python scripts/run_capacity_backtest.py strategy_name"
        )

        sys.exit(1)



    run_capacity_backtest(

        sys.argv[1]

    )