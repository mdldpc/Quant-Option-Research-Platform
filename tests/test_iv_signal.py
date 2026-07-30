import pandas as pd

from framework.strategy.signals.iv_signal import (
    IVSignalGenerator,
)


def test_iv_signal_generate():

    df = pd.DataFrame(
        {
            "trade_date": [
                20260101,
                20260102,
                20260103,
                20260104,
                20260105,
            ],

            "near_iv": [
                0.20,
                0.21,
                0.22,
                0.25,
                0.23,
            ],

            "term_slope_next_near": [
                0.01,
                0.02,
                0.03,
                0.04,
                0.02,
            ],

            "near_iv_zscore": [
                -1,
                -1.5,
                -2,
                -2.5,
                -1,
            ],

            "signal_score": [
                0,
                80,
                85,
                20,
                10,
            ],

            "long_signal": [
                0,
                1,
                0,
                0,
                0,
            ],
        }
    )


    generator = IVSignalGenerator(
        max_holding_days=3,
        exit_score_threshold=40,
    )


    result = generator.generate(df)


    assert len(result) == 1


    row = result.iloc[0]


    assert row["entry_date"] == 20260102

    assert row["exit_date"] == 20260104

    assert row["holding_days"] == 2

    assert row["exit_reason"] == "score_exit"