from typing import Annotated, Literal

from pydantic import BaseModel, Field, RootModel

FiniteNumber = Annotated[float, Field(allow_inf_nan=False, strict=True)]
PositiveNumber = Annotated[FiniteNumber, Field(gt=0)]


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class GreeksRequest(BaseModel):
    spot: PositiveNumber
    strike: PositiveNumber
    maturity: PositiveNumber = Field(description="Time to expiry in years.")
    rate: FiniteNumber = Field(description="Annual continuously compounded rate, decimal.")
    volatility: PositiveNumber = Field(description="Annual volatility, decimal.")
    option_type: Literal["call", "put"]


class OptionPosition(GreeksRequest):
    quantity: FiniteNumber = Field(description="Signed units; no contract multiplier.")


class PortfolioRequest(RootModel[list[OptionPosition]]):
    """A JSON array of positions; an empty array represents zero exposure."""


class GreeksResponse(BaseModel):
    delta: FiniteNumber
    gamma: FiniteNumber
    vega: FiniteNumber = Field(description="Sensitivity per 1.0 volatility change, not 1%.")
