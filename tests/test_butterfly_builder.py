import pandas as pd
import pytest


from framework.strategy.butterfly_builder import (
    ButterflyBuilder,
)


import framework.strategy.butterfly_builder as butterfly_module



def test_butterfly_builder(tmp_path):


    fake_file = tmp_path / "smile_dataset.parquet"


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
                "IO2602-C-3900",
                "IO2602-C-4000",
                "IO2602-C-4100",
            ],


            "expiry_code":[
                "2602",
                "2602",
                "2602",
            ],


            "option_type":[
                "C",
                "C",
                "C",
            ],


            "strike":[
                3900,
                4000,
                4100,
            ],


            "future_price":[
                4000,
                4000,
                4000,
            ],


            "T":[
                30/365,
                30/365,
                30/365,
            ],


            "smoothed_iv":[
                0.24,
                0.25,
                0.26,
            ],


            "BP1":[
                100,
                80,
                70,
            ],


            "AP1":[
                102,
                82,
                72,
            ],


            "delta":[
                0.7,
                0.5,
                0.3,
            ],


            "gamma":[
                0.01,
                0.02,
                0.01,
            ],


            "vega":[
                10,
                12,
                10,
            ],


            "theta":[
                -1,
                -2,
                -1,
            ],


            "vanna":[
                1,
                2,
                1,
            ],


            "vomma":[
                3,
                4,
                3,
            ],

        }
    )


    df.to_parquet(
        fake_file,
        index=False,
    )


    # replace input

    butterfly_module.SMILE_DATASET = fake_file


    # replace outputs

    butterfly_module.BUTTERFLY_DATASET = (
        tmp_path /
        "butterfly.parquet"
    )


    butterfly_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )


    butterfly_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = ButterflyBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    assert len(output) == 1


    row = output.iloc[0]


    # strike selection

    assert row["lower_strike"] == 3900

    assert row["middle_strike"] == 4000

    assert row["upper_strike"] == 4100



    # symmetry

    assert row["is_symmetric"]



    # midpoint prices:
    #
    # lower  = (100+102)/2 = 101
    # middle = (80+82)/2  = 81
    # upper  = (70+72)/2  = 71
    #
    # BF = 101 - 2*81 + 71
    #    = 10

    assert row["lower_price"] == pytest.approx(
        101
    )

    assert row["middle_price"] == pytest.approx(
        81
    )

    assert row["upper_price"] == pytest.approx(
        71
    )


    assert row["butterfly_price"] == pytest.approx(
        10
    )



    # Greeks:
    #
    # delta:
    # 0.7 - 2*0.5 + 0.3 = 0

    assert row["net_delta"] == pytest.approx(
        0
    )


    # gamma:
    #
    # 0.01 - 2*0.02 + 0.01 = -0.02

    assert row["net_gamma"] == pytest.approx(
        -0.02
    )


    # vega:
    #
    # 10 - 24 + 10 = -4

    assert row["net_vega"] == pytest.approx(
        -4
    )


    # theta:
    #
    # -1 -2*(-2) + (-1)
    # = 2

    assert row["net_theta"] == pytest.approx(
        2
    )