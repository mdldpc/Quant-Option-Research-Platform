import pandas as pd


from analysis.capacity_backtest import (
    CapacityBacktester,
)



def test_capacity_execution_single():


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
            ],


            "return":
            [
                0.1,
                0.2,
                -0.1,
            ]

        }

    )



    bt = CapacityBacktester(
        df,
        capacity=1
    )


    result = bt.execute()


    assert len(result)==2





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


    bt = CapacityBacktester(
        df,
        capacity=None
    )


    result = bt.execute()


    assert len(result)==3