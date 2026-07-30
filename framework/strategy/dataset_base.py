from abc import ABC, abstractmethod

from framework.strategy.dataset_contracts import (
    StrategyDatasetResult,
)


class StrategyDatasetBuilder(ABC):
    """
    Base class for all strategy dataset builders.
    """

    dataset_name = "unknown_strategy_dataset"


    @abstractmethod
    def build(self) -> StrategyDatasetResult:
        """
        Build strategy dataset.
        """
        raise NotImplementedError


    def validate(self) -> None:
        pass


    def qc(self) -> None:
        pass