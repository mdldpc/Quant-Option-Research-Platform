from pathlib import Path
import pandas as pd

from framework.strategy.contracts import BacktestResult
from analysis.performance_metrics import PerformanceMetrics
from analysis.trade_metrics import TradeMetrics

class StrategyComparison:


    def __init__(
        self,
        results: list[BacktestResult],
    ):
        self.results = results


    def to_dataframe(self):

        rows = []

        for r in self.results:

            trade_metrics = (
                self.calculate_trade_metrics(r)
            )

            risk = self.calculate_risk_metrics(r)

            rows.append(
                {
                    "strategy_name":
                        r.strategy_name,

                    "total_trades":
                        r.total_trades,

                    "completed_trades":
                        r.completed_trades,

                    "skipped_trades":
                        r.skipped_trades,

                    "win_rate":
                        r.win_rate,

                    "final_equity":
                        r.final_equity,

                    "total_return":
                        r.final_equity - 1,

                    "max_drawdown":
                        r.max_drawdown,

                    "average_return":
                        r.average_return,

                    "annualized_return":
                        risk.get(
                            "annualized_return"
                        ),

                    "annualized_volatility":
                        risk.get(
                            "annualized_volatility"
                        ),

                    "sharpe_ratio":
                        risk.get(
                            "sharpe_ratio"
                        ),

                    "sortino_ratio":
                        risk.get(
                            "sortino_ratio"
                        ),

                    "profit_factor":
                        risk.get(
                            "profit_factor"
                        ),

                    # -----------------------
                    # Trade Metrics v1.3
                    # -----------------------

                    "average_holding_days":
                        trade_metrics.get(
                            "average_holding_days"
                        ),


                    "trades_per_year":
                        trade_metrics.get(
                            "trades_per_year"
                        ),


                    "trade_annualized_return":
                        trade_metrics.get(
                            "annualized_return"
                        ),


                    "average_win":
                        trade_metrics.get(
                            "average_win"
                        ),


                    "average_loss":
                        trade_metrics.get(
                            "average_loss"
                        ),


                    "trade_profit_factor":
                        trade_metrics.get(
                            "profit_factor"
                        ),
                    
                    "status":
                        r.status,
                }
            )


        return pd.DataFrame(rows)


    def save(
        self,
        csv_path: Path,
        report_path: Path,
    ):

        df = self.to_dataframe()


        csv_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        df.to_csv(
            csv_path,
            index=False,
            encoding="utf-8-sig",
        )


        lines = []

        lines.append(
            "Strategy Comparison Report v1.3"
        )

        lines.append(
            "=" * 80
        )

        lines.append("")

        lines.append(
            str(df)
        )


        report_path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )


        return df
    

    def calculate_risk_metrics(
        self,
        result: BacktestResult,
    ):

        if result.trades_path is None:
            return {}


        df = pd.read_csv(
            result.trades_path
        )


        if "net_return" not in df.columns:
            return {}


        returns = (
            df["net_return"]
            .dropna()
            .astype(float)
        )


        if len(returns) == 0:
            return {}


        metrics = PerformanceMetrics(
            returns
        )


        summary = metrics.summary()


        return {

            "annualized_return":
                summary["annualized_return"],

            "annualized_volatility":
                summary["annualized_volatility"],

            "sharpe_ratio":
                summary["sharpe_ratio"],

            "sortino_ratio":
                summary["sortino_ratio"],

            "profit_factor":
                summary["profit_factor"],
        }

    def calculate_trade_metrics(
        self,
        result: BacktestResult,
    ):

        if result.trades_path is None:
            return {}


        trades = pd.read_csv(
            result.trades_path
        )


        metrics = TradeMetrics(
            trades
        )


        return metrics.summary()