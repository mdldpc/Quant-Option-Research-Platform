"""Explicit units and bounded work for European option scenario analysis."""

import math
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from api.schemas import FiniteNumber, OptionPosition


class ScenarioPosition(OptionPosition):
    position_id: Annotated[str, Field(min_length=1, max_length=80)]


class Scenario(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=80)]
    spot_return: Annotated[FiniteNumber, Field(gt=-1)] = Field(
        default=0.0, description="Relative spot shock: -0.10 means a 10% fall."
    )
    volatility_shift: FiniteNumber = Field(
        default=0.0, description="Additive decimal shift: +0.05 means +5 percentage points."
    )
    rate_shift: FiniteNumber = Field(
        default=0.0, description="Additive decimal shift: +0.01 means +100 basis points."
    )
    days_elapsed: Annotated[FiniteNumber, Field(ge=0)] = Field(
        default=0.0, description="Calendar days elapsed, converted using ACT/365."
    )


class ScenarioRequest(BaseModel):
    positions: Annotated[list[ScenarioPosition], Field(max_length=1000)]
    scenarios: Annotated[list[Scenario], Field(min_length=1, max_length=100)]

    @model_validator(mode="after")
    def validate_scenarios(self):
        if len(self.positions) * len(self.scenarios) > 10000:
            raise ValueError("At most 10,000 position-scenario pairs are supported.")
        ids = [p.position_id for p in self.positions]
        names = [s.name for s in self.scenarios]
        if len(set(ids)) != len(ids) or len(set(names)) != len(names):
            raise ValueError("Position IDs and scenario names must each be unique.")
        for scenario in self.scenarios:
            for position in self.positions:
                spot = position.spot * (1 + scenario.spot_return)
                vol = position.volatility + scenario.volatility_shift
                rate = position.rate + scenario.rate_shift
                maturity = position.maturity - scenario.days_elapsed / 365
                if not all(math.isfinite(x) for x in (spot, vol, rate, maturity)):
                    raise ValueError("Stressed parameters must be finite.")
                if spot <= 0 or vol <= 0 or maturity <= 0:
                    raise ValueError(
                        "Stressed spot, volatility and maturity must be positive; "
                        "scenarios at or beyond expiry are unsupported."
                    )
        return self


class PnLComponents(BaseModel):
    delta: FiniteNumber
    gamma: FiniteNumber
    vega: FiniteNumber
    theta: FiniteNumber
    rho: FiniteNumber


class PositionScenarioResult(BaseModel):
    position_id: str
    base_price: FiniteNumber
    stressed_price: FiniteNumber
    base_value: FiniteNumber
    stressed_value: FiniteNumber
    full_revaluation_pnl: FiniteNumber
    approximation_pnl: FiniteNumber
    approximation_error: FiniteNumber = Field(description="Full revaluation minus approximation.")
    components: PnLComponents


class ScenarioResult(BaseModel):
    name: str
    base_value: FiniteNumber
    stressed_value: FiniteNumber
    full_revaluation_pnl: FiniteNumber
    approximation_pnl: FiniteNumber
    approximation_error: FiniteNumber
    components: PnLComponents
    positions: list[PositionScenarioResult]


class ScenarioResponse(BaseModel):
    base_value: FiniteNumber
    scenarios: list[ScenarioResult]
