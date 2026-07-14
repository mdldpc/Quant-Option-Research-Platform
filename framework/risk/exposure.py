from dataclasses import dataclass
import pandas as pd


@dataclass
class ExposureResult:

    net_delta: float
    net_gamma: float
    net_vega: float
    net_theta: float

    gross_delta: float
    gross_vega: float

    positions: int


def _safe_sum(df: pd.DataFrame, column: str) -> float:

    if column not in df.columns:
        return 0.0

    return float(df[column].fillna(0).sum())


def compute_exposure(df: pd.DataFrame) -> ExposureResult:
    """
    Aggregate portfolio Greeks.

    Expected columns
    ----------------
    net_delta
    net_gamma
    net_vega
    net_theta

    Missing columns are treated as zero.
    """

    delta = _safe_sum(df, "net_delta")
    gamma = _safe_sum(df, "net_gamma")
    vega = _safe_sum(df, "net_vega")
    theta = _safe_sum(df, "net_theta")

    gross_delta = _safe_sum(df.assign(v=df["net_delta"].abs()) if "net_delta" in df else pd.DataFrame({"v":[]}), "v")
    gross_vega = _safe_sum(df.assign(v=df["net_vega"].abs()) if "net_vega" in df else pd.DataFrame({"v":[]}), "v")

    return ExposureResult(
        net_delta=delta,
        net_gamma=gamma,
        net_vega=vega,
        net_theta=theta,
        gross_delta=gross_delta,
        gross_vega=gross_vega,
        positions=len(df),
    )