import pandas as pd

from analysis.trade_metrics import TradeMetrics



def test_trade_metrics():


    df = pd.DataFrame(
        {
            "status":
                [
                    "ok",
                    "ok",
                    "invalid_price",
                ],

            "option_return":
                [
                    0.10,
                    -0.05,
                    None,
                ],

            "holding_days":
                [
                    10,
                    20,
                    5,
                ],
        }
    )


    metrics = TradeMetrics(
        df
    )


    result = metrics.summary()


    assert result["trade_count"] == 2

    assert abs(
        result["win_rate"] - 0.5
    ) < 1e-10


    assert abs(
        result["average_return"] - 0.025
    ) < 1e-10


    assert abs(
        result["average_holding_days"] - 15
    ) < 1e-10