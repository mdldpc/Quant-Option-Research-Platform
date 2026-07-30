import pandas as pd

from framework.strategy.signals.iv_signal import (
    IVSignalGenerator,
)

from framework.strategy.trade_constructor import (
    StrangleTradeConstructor,
)

from framework.strategy.backtesters.strangle import (
    StrangleBacktester,
)


def test_signal_constructor_backtest_pipeline():

    # =========================
    # 1. Fake signal features
    # =========================

    signal_df = pd.DataFrame(
        {
            "trade_date": [
                20260101,
                20260102,
                20260103,
                20260104,
            ],

            "near_iv": [
                0.20,
                0.25,
                0.30,
                0.22,
            ],

            "term_slope_next_near": [
                0.01,
                0.02,
                0.03,
                0.01,
            ],

            "near_iv_zscore": [
                -1,
                -2,
                -2.5,
                -0.5,
            ],

            "signal_score": [
                0,
                80,
                85,
                20,
            ],

            "long_signal": [
                0,
                1,
                0,
                0,
            ],
        }
    )


    # =========================
    # 2. Generate signal
    # =========================

    generator = IVSignalGenerator(
        max_holding_days=10,
        exit_score_threshold=40,
    )


    signals = generator.generate(
        signal_df
    )


    assert len(signals) == 1


    assert (
        "entry_date"
        in signals.columns
    )


    assert (
        "exit_date"
        in signals.columns
    )



    # =========================
    # 3. Fake option snapshot
    # =========================

    snapshot = pd.DataFrame(
        {
            "trade_date": [
                20260102,
                20260104,
            ],

            "expiry_code": [
                2601,
                2601,
            ],

            "T": [
                0.1,
                0.09,
            ],

            "strangle_price": [
                100,
                120,
            ],

            "call_strike": [
                4000,
                4000,
            ],

            "put_strike": [
                4000,
                4000,
            ],
        }
    )


    # =========================
    # 4. Constructor
    # =========================

    constructor = StrangleTradeConstructor(
        snapshot
    )


    trades = constructor.build_all(
        signals
    )


    assert len(trades) == 1


    assert (
        trades.iloc[0]["status"]
        ==
        "constructed"
    )


    # =========================
    # 5. Backtest
    # =========================

    backtester = StrangleBacktester(
        trades
    )


    result = backtester.run()


    assert len(result) == 1


    row = result.iloc[0]


    assert (
        row["option_pnl"]
        ==
        20
    )


    assert (
        row["option_return"]
        ==
        0.2
    )