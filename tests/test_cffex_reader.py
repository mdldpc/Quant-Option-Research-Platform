import pandas as pd


from framework.data.adapters.cffex import (
    CFFEXAdapter,
)



def test_read_option_file(tmp_path):


    raw = pd.DataFrame(

        {

            "symbol":
            [
                "IO2502-C-3850"
            ],

            "iRecvTime":
            [
                1000000
            ],

            "BP1":
            [
                100
            ],

            "AP1":
            [
                102
            ],

            "lastPrice":
            [
                101
            ],

            "volume":
            [
                500
            ],

            "openInterest":
            [
                1000
            ],

        }

    )


    file = (
        tmp_path
        /
        "sample.csv.xz"
    )


    raw.to_csv(
        file,
        index=False,
        compression="xz",
    )


    result = (
        CFFEXAdapter
        .read_option_file(file)
    )


    assert (
        "bid_price"
        in result.columns
    )


    assert (
        result.iloc[0]["last_price"]
        ==
        101
    )