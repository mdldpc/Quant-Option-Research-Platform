import pandas as pd


from analysis.raw_signal_overlap import (
    RawSignalOverlapDiagnostics,
)



def test_raw_overlap():


    df = pd.DataFrame(

        {

            "entry_date":
            [
                1,
                3,
                10,
            ],

            "exit_date":
            [
                5,
                8,
                15,
            ]

        }

    )


    diag = RawSignalOverlapDiagnostics(
        df
    )


    result = diag.summary()


    assert result["raw_opportunities"] == 3

    assert result["executable_trades"] == 2

    assert result["blocked_opportunities"] == 1