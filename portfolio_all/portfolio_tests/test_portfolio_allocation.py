import pandas as pd


from portfolio_all.portfolio_analysis.portfolio_allocation import (
    PortfolioAllocator
)



def create_test_returns():


    return pd.DataFrame(

        {

            "strategy_a":
            [
                0.01,
                0.02,
                -0.01,
                0.03,
            ],


            "strategy_b":
            [
                0.005,
                0.01,
                0.002,
                0.008,
            ],


            "strategy_c":
            [
                -0.01,
                0.02,
                0.01,
                0.015,
            ],

        }

    )



def test_equal_weight():


    returns = create_test_returns()


    allocator = PortfolioAllocator(

        returns

    )


    weights = (

        allocator
        .equal_weight()

    )


    assert abs(

        weights.sum()-1

    ) < 1e-8



    assert (

        weights >= 0

    ).all()



def test_generate_allocation_table():


    returns = create_test_returns()


    allocator = PortfolioAllocator(

        returns

    )


    table = (

        allocator
        .generate_allocation_table()

    )


    assert table.shape == (

        3,

        4

    )


    assert (

        abs(
            table.sum(axis=0)-1
        )

        <

        1e-8

    ).all().all()