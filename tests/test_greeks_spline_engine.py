import pandas as pd

from scripts.greeks_spline_engine_batch import (
    add_spline_greeks,
)


def test_add_spline_greeks():

    iv_df = pd.DataFrame(
        {
            "expiry_code": [
                "2601"
            ],

            "option_type": [
                "C"
            ],

            "strike": [
                4000
            ],

            "future_price": [
                4000
            ],

            "T": [
                30 / 365
            ],

        }
    )


    surface_df = pd.DataFrame(
        {
            "expiry_code": [
                "2601"
            ],

            "option_type": [
                "C"
            ],

            "strike": [
                4000
            ],

            "smoothed_iv": [
                0.25
            ],
        }
    )


    result = add_spline_greeks(
        iv_df,
        surface_df,
    )


    greek_cols = [
        "delta",
        "gamma",
        "vega",
        "theta",
        "vanna",
        "vomma",
        "speed",
    ]


    for col in greek_cols:

        assert col in result.columns

        assert (
            result[col]
            .notna()
            .all()
        )


    assert len(result) == 1