import pandas as pd


from analysis.overlap_diagnostics import (
    OverlapDiagnostics,
)



def test_overlap_detection():


    df = pd.DataFrame(

        {

            "entry_date":
            [
                20260101,
                20260103,
                20260110,
            ],


            "exit_date":
            [
                20260105,
                20260108,
                20260115,
            ]

        }

    )


    diag = OverlapDiagnostics(
        df
    )


    result = diag.summary()


    assert result["raw_signals"] == 3


    assert result["non_overlapping_trades"] == 2


    assert result["blocked_signals"] == 1