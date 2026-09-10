from typing import Annotated

from pydantic import BaseModel, Field

from api.schemas import GreeksRequest, FiniteNumber


class ValuationRequest(GreeksRequest):
    steps: Annotated[int, Field(strict=True, ge=1, le=2000)] = 500


class ValuationResponse(BaseModel):
    black_scholes_price: FiniteNumber
    binomial_price: FiniteNumber
    absolute_error: FiniteNumber
    steps: int
