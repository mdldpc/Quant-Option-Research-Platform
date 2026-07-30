from abc import ABC, abstractmethod

import pandas as pd


class BaseSignalGenerator(ABC):
    """
    Base interface for all strategy signals.
    """

    signal_name = "base_signal"


    @abstractmethod
    def generate(
        self,
        dataset: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate entry/exit signals.

        Returns
        -------
        pd.DataFrame

        Required columns:

        entry_date
        exit_date

        Optional:

        holding_days
        entry_signal_score
        exit_signal_score
        exit_reason
        """

        raise NotImplementedError