import pandas as pd


from analysis.raw_signal_generator import (
    RawSignalGenerator,
)



def test_strangle_raw_signal():


    df = pd.DataFrame(

        {

            "long_signal":
            [
                0,
                1,
                1,
                0,
            ]

        }

    )


    generator = RawSignalGenerator(
        "long_atm_strangle"
    )


    result = generator.generate(df)


    assert len(result) == 2




def test_unknown_strategy():


    generator = RawSignalGenerator(
        "wrong"
    )


    try:

        generator.generate(
            pd.DataFrame()
        )

        assert False


    except ValueError:

        assert True