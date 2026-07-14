from abc import ABC, abstractmethod

from framework.research.contracts import ResearchDatasetResult


class ResearchBuilder(ABC):
    """
    Base class for all research dataset builders.
    """

    dataset_name = "unknown"

    @abstractmethod
    def build(self) -> ResearchDatasetResult:
        """
        Build the research dataset.
        """
        raise NotImplementedError

    def validate(self) -> None:
        """
        Optional validation hook.
        """
        pass

    def qc(self) -> None:
        """
        Optional quality control hook.
        """
        pass

    def save(self) -> None:
        """
        Optional save hook.
        """
        pass