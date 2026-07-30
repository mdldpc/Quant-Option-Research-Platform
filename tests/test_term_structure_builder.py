import pytest
import pandas as pd


from framework.research.term_structure_builder import (
    TermStructureBuilder,
)

import framework.research.term_structure_builder as term_module



def test_term_structure_builder(tmp_path):


    fake_atm = tmp_path / "atm.parquet"


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

            "expiry_code":[
                "2602",
                "2601",
                "2603",
                "2606",
            ],

            "T":[
                0.08,
                0.03,
                0.15,
                0.40,
            ],

            "atm_iv":[
                0.27,
                0.25,
                0.30,
                0.35,
            ],

            "atm_strike":[
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

            "has_both":[
                True,
                True,
                True,
                False,
            ],

        }
    )


    df.to_parquet(
        fake_atm,
        index=False,
    )


    term_module.ATM_IV_DATASET = fake_atm


    term_module.TERM_STRUCTURE_DATASET = (
        tmp_path /
        "term.parquet"
    )


    term_module.PREVIEW_PATH = (
        tmp_path /
        "preview.csv"
    )

    term_module.REPORT_PATH = (
        tmp_path /
        "report.txt"
    )


    result = TermStructureBuilder().build()


    assert result.status == "success"


    output = pd.read_parquet(
        result.dataset_path
    )


    assert len(output) == 1


    row = output.iloc[0]


    # maturity ordering

    assert row["near_expiry"] == "2601"

    assert row["next_expiry"] == "2602"

    assert row["third_expiry"] == "2603"


    # IV values

    assert row["near_iv"] == pytest.approx(
        0.25
    )

    assert row["next_iv"] == pytest.approx(
        0.27
    )


    assert row["third_iv"] == pytest.approx(
        0.30
    )


    # spread

    assert row["next_minus_near_iv"] == pytest.approx(
        0.02
    )