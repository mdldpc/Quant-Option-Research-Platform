"""
Unified Strategy Evaluation Report

Combine:

1. Trade Quality Analysis
2. Performance Evaluation

into one research report.
"""


import pandas as pd


from analysis.trade_quality import (
    TradeQualityAnalyzer,
)


from analysis.trade_performance_adapter import (
    TradePerformanceAdapter,
)


from analysis.strategy_evaluation import (
    StrategyEvaluator,
)



class EvaluationReport:



    @classmethod
    def generate(
        cls,
        trades: pd.DataFrame,
    ):


        if trades.empty:

            raise ValueError(
                "Empty trade dataframe"
            )


        strategy = (
            trades["strategy"]
            .iloc[0]
        )


        # ----------------------------
        # Trade quality
        # ----------------------------

        quality = (
            TradeQualityAnalyzer
            .analyze(
                trades
            )
        )


        # ----------------------------
        # Performance
        # ----------------------------

        performance_trades = (
            TradePerformanceAdapter
            .adapt(
                trades
            )
        )


        evaluator = StrategyEvaluator(
            performance_trades
        )


        performance = (
            evaluator
            .evaluate()
        )


        # ----------------------------
        # Merge
        # ----------------------------

        result = {}


        result.update(
            quality
        )


        result.update(
            performance
        )


        result["strategy"] = strategy


        return result