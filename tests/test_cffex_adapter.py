import pandas as pd


from framework.data.adapters.cffex import (
    CFFEXAdapter,
)



def test_normalize_option():


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


    result = (
        CFFEXAdapter
        .normalize_option(raw)
    )


    assert list(result.columns) == [

        "symbol",

        "timestamp",

        "bid_price",

        "ask_price",

        "last_price",

        "volume",

        "open_interest",

    ]


    assert result.iloc[0]["bid_price"] == 100

    assert result.iloc[0]["ask_price"] == 102

    assert result.iloc[0]["last_price"] == 101