import pandas as pd
import pytest


from framework.strategy.calendar_builder import (
    CalendarBuilder,
)


import framework.strategy.calendar_builder as calendar_module



def test_calendar_builder(tmp_path):


    fake_file = tmp_path / "all_greeks.parquet"



    df = pd.DataFrame(
        {

            "trade_date":[
                "2026-01-05",
                "2026-01-05",
                "2026-01-05",
                "2026-01-05",
            ],


            "time_bucket":[
                100,
                100,
                100,
                100,
            ],


            "symbol":[

                "IO2601-C-4000",
                "IO2601-P-4000",

                "IO2602-C-4000",
                "IO2602-P-4000",

            ],



            "expiry_code":[

                "2601",
                "2601",

                "2602",
                "2602",

            ],



            "option_type":[

                "C",
                "P",

                "C",
                "P",

            ],



            "strike":[

                4000,
                4000,

                4000,
                4000,

            ],



            "future_price":[

                4000,
                4000,

                4000,
                4000,

            ],



            "T":[

                10/365,
                10/365,

                40/365,
                40/365,

            ],



            "smoothed_iv":[

                0.20,
                0.22,

                0.30,
                0.32,

            ],



            "BP1":[

                100,
                90,

                120,
                110,

            ],



            "AP1":[

                102,
                92,

                122,
                112,

            ],



            "delta":[

                0.5,
                -0.5,

                0.6,
                -0.6,

            ],



            "gamma":[

                0.01,
                0.01,

                0.02,
                0.02,

            ],



            "vega":[

                10,
                10,

                15,
                15,

            ],



            "theta":[

                -1,
                -1,

                -2,
                -2,

            ],



            "vanna":[

                1,
                1,

                2,
                2,

            ],



            "vomma":[

                3,
                3,

                4,
                4,

            ],

        }
    )



    df.to_parquet(
        fake_file,
        index=False,
    )



    # replace input

    calendar_module.ALL_GREEKS_FILE = fake_file



    # replace outputs

    calendar_module.CALENDAR_DATASET = (
        tmp_path /
        "calendar.parquet"
    )


    calendar_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )


    calendar_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )



    result = CalendarBuilder().build()



    assert result.status == "success"



    output = pd.read_parquet(
        result.dataset_path
    )



    assert len(output) == 1



    row = output.iloc[0]



    # expiry ordering

    assert row["near_expiry"] == "2601"

    assert row["next_expiry"] == "2602"



    # IV

    #
    # near:
    # (0.20+0.22)/2 = 0.21
    #
    # next:
    # (0.30+0.32)/2 = 0.31
    #

    assert row["near_iv"] == pytest.approx(
        0.21
    )


    assert row["next_iv"] == pytest.approx(
        0.31
    )



    assert row["iv_spread"] == pytest.approx(
        0.10
    )



    # Prices
    #
    # near:
    # call=(100+102)/2=101
    # put =(90+92)/2=91
    # straddle=192
    #
    # next:
    # call=121
    # put =111
    # straddle=232
    #
    # calendar=192-232=-40


    assert row["near_straddle_price"] == pytest.approx(
        192
    )


    assert row["next_straddle_price"] == pytest.approx(
        232
    )


    assert row["calendar_price"] == pytest.approx(
        -40
    )



    # Greeks
    #
    # delta:
    # near:
    # 0.5 + (-0.5)=0
    #
    # next:
    # 0.6 + (-0.6)=0
    #
    # result=0


    assert row["net_delta"] == pytest.approx(
        0
    )



    # gamma:
    #
    # near:
    # 0.01+0.01=0.02
    #
    # next:
    # 0.02+0.02=0.04
    #
    # net=-0.02


    assert row["net_gamma"] == pytest.approx(
        -0.02
    )



    # vega:
    #
    # near=20
    # next=30
    #
    # net=-10

    assert row["net_vega"] == pytest.approx(
        -10
    )



    # theta:
    #
    # near=-2
    # next=-4
    #
    # net=2


    assert row["net_theta"] == pytest.approx(
        2
    )


    assert (
        row["calendar_direction"]
        ==
        "long_near_short_next"
    )