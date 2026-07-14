from abc import ABC, abstractmethod

from framework.strategy.contracts import BacktestResult


class StrategyBacktester(ABC):
    """
    Base class for all strategy backtesters.
    """

    strategy_name = "unknown_strategy"

    @abstractmethod
    def run(self) -> BacktestResult:
        raise NotImplementedError

    def validate_inputs(self) -> None:
        pass