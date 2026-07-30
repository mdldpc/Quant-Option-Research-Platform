import pandas as pd
import pytest
from pathlib import Path

from framework.research.atm_builder import ATMBuilder
import framework.research.atm_builder as atm_module



def test_atm_builder(tmp_path):


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
                "IO2601-C-4000",
                "IO2601-P-4000",
            ],

            "expiry_code":[
                "2601",
                "2601",
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

            "implied_vol":[
                0.24,
                0.26,
            ],

            "smoothed_iv":[
                0.25,
                0.27,
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

        }
    )


    df.to_parquet(
        fake_file,
        index=False,
    )


    # replace source file

    atm_module.ALL_GREEKS_FILE = fake_file


    # replace output paths

    atm_module.ATM_IV_DATASET = (
        tmp_path /
        "atm.parquet"
    )


    atm_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )


    atm_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = ATMBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    assert len(output) == 1


    row = output.iloc[0]


    assert row["has_both"]


    assert row["atm_iv"] == 0.26


    assert row["call_iv"] == 0.25


    assert row["put_iv"] == 0.27


    assert row["call_put_iv_spread"] == pytest.approx(
        -0.02
    )