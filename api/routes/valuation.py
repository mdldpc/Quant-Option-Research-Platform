from fastapi import APIRouter, HTTPException

from api.valuation import black_scholes_price, crr_price
from api.valuation_schemas import ValuationRequest, ValuationResponse

router = APIRouter(prefix="/valuation", tags=["valuation"])


@router.post("/price", response_model=ValuationResponse)
def price(option: ValuationRequest) -> ValuationResponse:
    """Compare zero-dividend European prices; units match spot and strike."""
    parameters = option.model_dump(exclude={"steps"})
    try:
        closed_form = black_scholes_price(**parameters)
        tree = crr_price(**parameters, steps=option.steps)
    except (ValueError, OverflowError, ZeroDivisionError, FloatingPointError) as exc:
        raise HTTPException(422, str(exc)) from exc
    return ValuationResponse(
        black_scholes_price=closed_form,
        binomial_price=tree,
        absolute_error=abs(closed_form - tree),
        steps=option.steps,
    )
