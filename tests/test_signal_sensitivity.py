import pandas as pd


from analysis.signal_sensitivity import (
    SignalSensitivity,
)



def test_positive_threshold():


    df = pd.DataFrame(
        {

            "score":[
                10,
                30,
                50,
                70,
            ]

        }
    )


    obj = SignalSensitivity(
        df,
        "score",
        "positive",
    )


    result = obj.analyze(
        [
            30,
            60,
        ]
    )


    assert result.iloc[0]["signal_count"] == 3

    assert result.iloc[1]["signal_count"] == 1




def test_negative_threshold():


    df = pd.DataFrame(
        {

            "score":[
                -3,
                -2,
                -1,
                0,
            ]

        }
    )


    obj = SignalSensitivity(
        df,
        "score",
        "negative",
    )


    result = obj.analyze(
        [
            -2,
            -1,
        ]
    )


    assert result.iloc[0]["signal_count"] == 2

    assert result.iloc[1]["signal_count"] == 3