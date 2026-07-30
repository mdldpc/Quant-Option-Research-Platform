import pandas as pd
import pytest

from framework.strategy.strangle_builder import (
    StrangleBuilder,
)

import framework.strategy.strangle_builder as strangle_module



def test_strangle_builder(tmp_path):


    fake_file = tmp_path / "all_greeks.parquet"


    df = pd.DataFrame(
        {

            "trade_date":[
                "2026-01-05",
                "2026-01-05",
            ],

            "time_bucket":[
                100,
                100,
            ],


            "symbol":[
                "IO2602-C-4000",
                "IO2602-P-4000",
            ],


            "expiry_code":[
                "2602",
                "2602",
            ],


            "option_type":[
                "C",
                "P",
            ],


            "strike":[
                4000,
                4000,
            ],


            "future_price":[
                4000,
                4000,
            ],


            "T":[
                30/365,
                30/365,
            ],


            "smoothed_iv":[
                0.25,
                0.27,
            ],


            "implied_vol":[
                0.24,
                0.26,
            ],


            "delta":[
                0.5,
                -0.5,
            ],


            "gamma":[
                0.01,
                0.01,
            ],


            "vega":[
                10,
                10,
            ],


            "theta":[
                -1,
                -1,
            ],


            "vanna":[
                0,
                0,
            ],


            "vomma":[
                1,
                1,
            ],


            "speed":[
                0,
                0,
            ],


            "BP1":[
                100,
                80,
            ],


            "AP1":[
                102,
                82,
            ],

        }
    )


    df.to_parquet(
        fake_file,
        index=False,
    )


    # patch input

    strangle_module.ALL_GREEKS_FILE = fake_file


    # patch outputs

    strangle_module.STRANGLE_DATASET = (
        tmp_path /
        "strangle.parquet"
    )


    strangle_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )


    strangle_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = StrangleBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    assert len(output) == 1


    row = output.iloc[0]


    assert row["call_symbol"] == (
        "IO2602-C-4000"
    )


    assert row["put_symbol"] == (
        "IO2602-P-4000"
    )


    # midpoint:
    #
    # call=(100+102)/2=101
    # put=(80+82)/2=81
    #
    # strangle=182

    assert row["call_price"] == pytest.approx(
        101
    )


    assert row["put_price"] == pytest.approx(
        81
    )


    assert row["strangle_price"] == pytest.approx(
        182
    )


    assert row["call_iv"] == pytest.approx(
        0.25
    )


    assert row["put_iv"] == pytest.approx(
        0.27
    )