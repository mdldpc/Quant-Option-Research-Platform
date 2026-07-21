from pathlib import Path

import pandas as pd

from framework.reporting.backtest_charts import (
    draw_equity_curve,
    draw_drawdown,
    draw_return_distribution,
)



def test_backtest_charts(tmp_path):


    df = pd.DataFrame(
        {
            "equity":[1,1.05,1.1],

            "drawdown":[0,-0.01,0],

            "option_return":[
                0.05,
                -0.01,
                0.04
            ]
        }
    )


    chart_dir = tmp_path / "charts"


    equity = draw_equity_curve(
        df,
        chart_dir,
    )


    drawdown = draw_drawdown(
        df,
        chart_dir,
    )


    distribution = draw_return_distribution(
        df,
        chart_dir,
    )


    assert equity.exists()

    assert drawdown.exists()

    assert distribution.exists()



    assert isinstance(
        equity,
        Path
    )


    assert equity.exists()

    assert drawdown.exists()

    assert distribution.exists()