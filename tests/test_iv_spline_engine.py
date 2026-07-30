import pandas as pd

from scripts.iv_spline_engine import (
    build_spline_surface,
)



def test_build_spline_surface():


    iv_df = pd.DataFrame(
        {
            "expiry_code":
            [
                "2601",
                "2601",
                "2601",
                "2601",
            ],

            "option_type":
            [
                "C",
                "C",
                "C",
                "C",
            ],

            "strike":
            [
                3800,
                4000,
                4200,
                4400,
            ],

            "implied_vol":
            [
                0.28,
                0.25,
                0.27,
                0.30,
            ],

            "future_price":
            [
                4100,
                4100,
                4100,
                4100,
            ],
        }
    )


    result = build_spline_surface(
        iv_df
    )


    assert not result.empty


    assert (
        "smoothed_iv"
        in result.columns
    )


    assert (
        len(result)
        ==
        4
    )


    assert (
        result["smoothed_iv"]
        .notna()
        .all()
    )


    assert (
        result["expiry_code"]
        .iloc[0]
        ==
        "2601"
    )


    assert (
        result["option_type"]
        .iloc[0]
        ==
        "C"
    )