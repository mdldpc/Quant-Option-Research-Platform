from framework.reporting.report_models import ReportData

from framework.strategy.contracts import BacktestResult


class ReportBuilder:
    """
    Convert internal backtest outputs
    into standardized ReportData.

    Responsibility:

    BacktestResult
          |
          v
    ReportData

    """


    def __init__(
        self,
        strategy_description="",
        display_name="",
    ):

        self.strategy_description = strategy_description

        self.display_name = display_name



    def build(
        self,
        result: BacktestResult,
        performance_metrics=None,
        trade_statistics=None,
        risk_metrics=None,
        charts=None,
    ) -> ReportData:
        """
        Build report-ready data.

        Parameters
        ----------

        result:
            Standard BacktestResult.

        performance_metrics:
            Output from PerformanceMetrics.

        trade_statistics:
            Trade level statistics.

        risk_metrics:
            Greeks / exposure metrics.

        """


        return ReportData(

            strategy_name=result.strategy_name,


            display_name=(
                self.display_name
                if self.display_name
                else result.strategy_name
            ),


            description=self.strategy_description,


            performance_metrics=(
                performance_metrics
                if performance_metrics
                else {}
            ),


            trade_statistics=(
                trade_statistics
                if trade_statistics
                else {}
            ),


            risk_metrics=(
                risk_metrics
                if risk_metrics
                else {}
            ),


            charts=(
                charts
                if charts
                else {}
            ),


            metadata={
                "status": result.status,
                "message": result.message,
            }

        )