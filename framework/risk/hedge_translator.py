import math
from dataclasses import dataclass
from typing import Iterable, List

from framework.risk.hedge_rules import HedgeRecommendation
from framework.risk.instrument_specs import get_instrument_spec


@dataclass
class HedgeExecutionPlan:
    risk_type: str
    risk_level: str
    action: str
    hedge_instrument: str
    trade_direction: str
    trade_units: int
    requested_hedge_size: float
    exposure_per_unit: float
    estimated_hedged_exposure: float
    estimated_residual_exposure: float
    reason: str
    notes: str


def _round_units(size: float, min_trade_unit: int) -> int:
    if size <= 0:
        return 0
    return int(math.ceil(size / min_trade_unit) * min_trade_unit)


def _resolve_instrument_name(rec: HedgeRecommendation) -> str:
    if rec.hedge_instrument == "option_vol_structure":
        return "calendar_spread"

    if rec.hedge_instrument == "option_structure":
        if rec.risk_type == "gamma":
            return "butterfly"
        if rec.risk_type == "theta":
            return "calendar_spread"

    return rec.hedge_instrument


def _exposure_per_unit(spec, risk_type: str) -> float:
    if risk_type == "delta":
        return spec.delta_per_unit
    if risk_type == "gamma":
        return spec.gamma_per_unit
    if risk_type == "vega":
        return spec.vega_per_unit
    if risk_type == "theta":
        return spec.theta_per_unit
    return 0.0


def _trade_direction(rec: HedgeRecommendation) -> str:
    if rec.action == "no_action":
        return "none"

    if rec.action in ["sell_futures", "reduce_long_vol", "reduce_gamma_exposure"]:
        return "sell"

    if rec.action in ["buy_futures", "reduce_short_vol"]:
        return "buy"

    if rec.action == "reduce_theta_decay":
        return "reduce_position"

    return "review"


def _signed_current_exposure(rec: HedgeRecommendation) -> float:
    if rec.action in ["sell_futures", "reduce_long_vol", "reduce_gamma_exposure", "reduce_theta_decay"]:
        return abs(rec.hedge_size)

    if rec.action in ["buy_futures", "reduce_short_vol"]:
        return -abs(rec.hedge_size)

    return 0.0


def translate_recommendation(rec: HedgeRecommendation) -> HedgeExecutionPlan:
    if rec.action == "no_action" or rec.hedge_size <= 0:
        return HedgeExecutionPlan(
            risk_type=rec.risk_type,
            risk_level=rec.risk_level,
            action=rec.action,
            hedge_instrument=rec.hedge_instrument,
            trade_direction="none",
            trade_units=0,
            requested_hedge_size=rec.hedge_size,
            exposure_per_unit=0.0,
            estimated_hedged_exposure=0.0,
            estimated_residual_exposure=0.0,
            reason=rec.reason,
            notes="No hedge required.",
        )

    instrument_name = _resolve_instrument_name(rec)
    spec = get_instrument_spec(instrument_name)

    unit = _exposure_per_unit(spec, rec.risk_type)

    if unit <= 0:
        return HedgeExecutionPlan(
            risk_type=rec.risk_type,
            risk_level=rec.risk_level,
            action=rec.action,
            hedge_instrument=instrument_name,
            trade_direction="review",
            trade_units=0,
            requested_hedge_size=rec.hedge_size,
            exposure_per_unit=unit,
            estimated_hedged_exposure=0.0,
            estimated_residual_exposure=_signed_current_exposure(rec),
            reason=rec.reason,
            notes=f"No valid {rec.risk_type}_per_unit defined for {instrument_name}.",
        )

    units = _round_units(rec.hedge_size / unit, spec.min_trade_unit)
    direction = _trade_direction(rec)

    current_exposure = _signed_current_exposure(rec)

    if direction in ["sell", "reduce_position"]:
        hedged = -units * unit
    elif direction == "buy":
        hedged = units * unit
    else:
        hedged = 0.0

    residual = current_exposure + hedged

    return HedgeExecutionPlan(
        risk_type=rec.risk_type,
        risk_level=rec.risk_level,
        action=rec.action,
        hedge_instrument=instrument_name,
        trade_direction=direction,
        trade_units=units,
        requested_hedge_size=rec.hedge_size,
        exposure_per_unit=unit,
        estimated_hedged_exposure=hedged,
        estimated_residual_exposure=residual,
        reason=rec.reason,
        notes=spec.notes,
    )


def translate_recommendations(
    recommendations: Iterable[HedgeRecommendation],
) -> List[HedgeExecutionPlan]:
    return [
        translate_recommendation(rec)
        for rec in recommendations
    ]