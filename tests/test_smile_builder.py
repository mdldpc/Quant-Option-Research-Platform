import pandas as pd


from framework.research.smile_builder import (
    SmileNearBuilder,
)

import framework.research.smile_builder as smile_module



def test_smile_builder(tmp_path):


    fake_file = tmp_path / "all_greeks.parquet"


    df = pd.DataFrame(
        {

            "trade_date":[
                "2026-01-05",
                "2026-01-05",
                "2026-01-05",
            ],

            "time_bucket":[
                100,
                100,
                100,
            ],

            "symbol":[
                "IO2601-C-4000",
                "IO2601-C-4200",
                "IO2602-C-4000",
            ],

            "expiry_code":[
                "2601",
                "2601",
                "2602",
            ],

            "option_type":[
                "C",
                "C",
                "C",
            ],

            "strike":[
                4000,
                4200,
                4000,
            ],

            "future_price":[
                4000,
                4000,
                4000,
            ],

            "T":[
                10/365,
                10/365,
                40/365,
            ],

            "implied_vol":[
                0.20,
                0.25,
                0.22,
            ],

            "smoothed_iv":[
                0.21,
                0.26,
                0.23,
            ],

            "delta":[
                0.5,
                0.3,
                0.5,
            ],

            "gamma":[
                0.01,
                0.01,
                0.01,
            ],

            "vega":[
                10,
                10,
                10,
            ],

            "theta":[
                -1,
                -1,
                -1,
            ],

            "vanna":[
                0,
                0,
                0,
            ],

            "vomma":[
                1,
                1,
                1,
            ],

            "speed":[
                0,
                0,
                0,
            ],

            "volume":[
                1,
                1,
                1,
            ],

            "openInterest":[
                10,
                10,
                10,
            ],

            "BP1":[
                100,
                50,
                80,
            ],

            "AP1":[
                101,
                51,
                81,
            ],

        }
    )


    df.to_parquet(
        fake_file,
        index=False
    )


    smile_module.ALL_GREEKS_FILE = fake_file

    smile_module.SMILE_DATASET = (
        tmp_path /
        "smile.parquet"
    )

    smile_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )

    smile_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = SmileNearBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    # only near expiry remains
    assert output["expiry_code"].nunique() == 1

    assert (
        output["expiry_code"]
        .iloc[0]
        ==
        "2601"
    )


    # moneyness check
    atm = output[
        output["strike"] == 4000
    ].iloc[0]


    assert atm["moneyness"] == 1.0


    assert (
        atm["moneyness_bucket"]
        ==
        "atm"
    )


    high = output[
        output["strike"] == 4200
    ].iloc[0]


    assert (
        high["moneyness"]
        ==
        1.05
    )