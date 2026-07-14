from dataclasses import dataclass
from typing import List

from framework.risk.exposure import ExposureResult


@dataclass
class HedgeRecommendation:
    risk_type: str
    risk_level: str
    action: str
    hedge_instrument: str
    hedge_size: float
    residual_target: float
    reason: str


@dataclass
class HedgeRuleConfig:
    delta_warning: float = 50.0
    delta_critical: float = 100.0

    vega_warning: float = 500.0
    vega_critical: float = 1000.0

    gamma_warning: float = 0.5
    gamma_critical: float = 1.0

    theta_warning: float = -500.0
    theta_critical: float = -1000.0

    futures_delta_unit: float = 1.0
    vega_unit: float = 100.0


def classify_abs(value: float, warning: float, critical: float) -> str:
    x = abs(value)

    if x >= critical:
        return "critical"

    if x >= warning:
        return "warning"

    return "normal"


def classify_negative(value: float, warning: float, critical: float) -> str:
    if value <= critical:
        return "critical"

    if value <= warning:
        return "warning"

    return "normal"


def delta_hedge(exposure: ExposureResult, config: HedgeRuleConfig) -> HedgeRecommendation:
    level = classify_abs(
        exposure.net_delta,
        config.delta_warning,
        config.delta_critical,
    )

    if level == "normal":
        action = "no_action"
        size = 0.0
        reason = "Delta exposure is within threshold."
    elif exposure.net_delta > 0:
        action = "sell_futures"
        size = exposure.net_delta / config.futures_delta_unit
        reason = "Positive delta exposure should be reduced by selling futures."
    else:
        action = "buy_futures"
        size = abs(exposure.net_delta) / config.futures_delta_unit
        reason = "Negative delta exposure should be reduced by buying futures."

    return HedgeRecommendation(
        risk_type="delta",
        risk_level=level,
        action=action,
        hedge_instrument="IF_futures",
        hedge_size=size,
        residual_target=0.0,
        reason=reason,
    )


def vega_hedge(exposure: ExposureResult, config: HedgeRuleConfig) -> HedgeRecommendation:
    level = classify_abs(
        exposure.net_vega,
        config.vega_warning,
        config.vega_critical,
    )

    if level == "normal":
        action = "no_action"
        size = 0.0
        reason = "Vega exposure is within threshold."
    elif exposure.net_vega > 0:
        action = "reduce_long_vol"
        size = exposure.net_vega / config.vega_unit
        reason = "Positive vega exposure may be reduced by selling volatility structures."
    else:
        action = "reduce_short_vol"
        size = abs(exposure.net_vega) / config.vega_unit
        reason = "Negative vega exposure may be reduced by buying volatility structures."

    return HedgeRecommendation(
        risk_type="vega",
        risk_level=level,
        action=action,
        hedge_instrument="option_vol_structure",
        hedge_size=size,
        residual_target=0.0,
        reason=reason,
    )


def gamma_hedge(exposure: ExposureResult, config: HedgeRuleConfig) -> HedgeRecommendation:
    level = classify_abs(
        exposure.net_gamma,
        config.gamma_warning,
        config.gamma_critical,
    )

    if level == "normal":
        action = "no_action"
        size = 0.0
        reason = "Gamma exposure is within threshold."
    else:
        action = "reduce_gamma_exposure"
        size = abs(exposure.net_gamma)
        reason = "Gamma exposure is elevated; reduce convexity-sensitive positions."

    return HedgeRecommendation(
        risk_type="gamma",
        risk_level=level,
        action=action,
        hedge_instrument="option_structure",
        hedge_size=size,
        residual_target=0.0,
        reason=reason,
    )


def theta_hedge(exposure: ExposureResult, config: HedgeRuleConfig) -> HedgeRecommendation:
    level = classify_negative(
        exposure.net_theta,
        config.theta_warning,
        config.theta_critical,
    )

    if level == "normal":
        action = "no_action"
        size = 0.0
        reason = "Theta decay is within threshold."
    else:
        action = "reduce_theta_decay"
        size = abs(exposure.net_theta)
        reason = "Theta decay is elevated; reduce time-decay-heavy positions."

    return HedgeRecommendation(
        risk_type="theta",
        risk_level=level,
        action=action,
        hedge_instrument="option_structure",
        hedge_size=size,
        residual_target=0.0,
        reason=reason,
    )


def generate_hedge_recommendations(
    exposure: ExposureResult,
    config: HedgeRuleConfig | None = None,
) -> List[HedgeRecommendation]:
    if config is None:
        config = HedgeRuleConfig()

    return [
        delta_hedge(exposure, config),
        vega_hedge(exposure, config),
        gamma_hedge(exposure, config),
        theta_hedge(exposure, config),
    ]