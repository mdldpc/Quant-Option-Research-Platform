import pytest
import pandas as pd

from framework.research.surface_builder import (
    SurfaceNearBuilder,
)

import framework.research.surface_builder as surface_module



def test_surface_builder(tmp_path):


    fake_smile = tmp_path / "smile.parquet"


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

            "moneyness_bucket":[
                "atm",
                "atm",
                "high_moneyness",
            ],

            "smoothed_iv":[
                0.25,
                0.27,
                0.30,
            ],

            "implied_vol":[
                0.24,
                0.26,
                0.29,
            ],

            "moneyness":[
                1.0,
                1.0,
                1.05,
            ],

            "log_moneyness":[
                0,
                0,
                0.04879,
            ],

            "abs_log_moneyness":[
                0,
                0,
                0.04879,
            ],

            "T":[
                0.03,
                0.03,
                0.03,
            ],

            "option_type":[
                "C",
                "P",
                "C",
            ],

            "volume":[
                10,
                20,
                30,
            ],

            "openInterest":[
                100,
                200,
                300,
            ],

        }
    )


    df.to_parquet(
        fake_smile,
        index=False,
    )


    # patch input

    surface_module.SMILE_DATASET = fake_smile


    # patch outputs

    surface_module.SURFACE_DATASET = (
        tmp_path /
        "surface.parquet"
    )

    surface_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )

    surface_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = SurfaceNearBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    assert len(output) == 2


    atm = output[
        output["surface_moneyness_bucket"]=="atm"
    ].iloc[0]


    assert atm["row_count"] == 2


    assert atm["smoothed_iv_mean"] == pytest.approx(
        0.26
    )


    assert atm["call_count"] == 1

    assert atm["put_count"] == 1



    high = output[
        output["surface_moneyness_bucket"]
        ==
        "high_moneyness"
    ].iloc[0]


    assert high["row_count"] == 1

    assert high["smoothed_iv_mean"] == pytest.approx(
        0.30
    )