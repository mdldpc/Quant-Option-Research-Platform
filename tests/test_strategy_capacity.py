import pandas as pd


from analysis.strategy_capacity import (
    StrategyCapacityAnalyzer,
)



def test_capacity_single_position():


    df = pd.DataFrame(

        {

            "entry_idx":
            [
                1,
                3,
                10,
            ],


            "exit_idx":
            [
                5,
                8,
                15,
            ]

        }

    )


    analyzer = StrategyCapacityAnalyzer(
        df
    )


    result = analyzer.simulate(
        capacity=1
    )


    assert len(result) == 2




def test_capacity_two_positions():


    df = pd.DataFrame(

        {

            "entry_idx":
            [
                1,
                3,
                10,
            ],


            "exit_idx":
            [
                5,
                8,
                15,
            ]

        }

    )


    analyzer = StrategyCapacityAnalyzer(
        df
    )


    result = analyzer.simulate(
        capacity=2
    )


    assert len(result) == 3




def test_capacity_unlimited():


    df = pd.DataFrame(

        {

            "entry_idx":
            [
                1,
                3,
                10,
            ],


            "exit_idx":
            [
                5,
                8,
                15,
            ]

        }

    )


    analyzer = StrategyCapacityAnalyzer(
        df
    )


    result = analyzer.simulate(
        capacity=None
    )


    assert len(result) == 3