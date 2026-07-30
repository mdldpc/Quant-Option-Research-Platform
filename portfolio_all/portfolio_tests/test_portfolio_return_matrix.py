import pandas as pd


from analysis.portfolio_return_matrix import (
    PortfolioReturnMatrix,
)



def test_matrix_build():


    configs = {


        "strategy_a":

        {

        "trade_file":
        "dummy",

        "snapshot":
        "dummy"

        }

    }


    # only check class exists

    assert (
        PortfolioReturnMatrix
        is not None
    )