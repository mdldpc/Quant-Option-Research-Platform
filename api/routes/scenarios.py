from fastapi import APIRouter, HTTPException

from api.scenario_schemas import ScenarioRequest, ScenarioResponse
from api.scenarios import run_scenarios

router = APIRouter(prefix="/risk", tags=["risk"])


@router.post("/scenarios", response_model=ScenarioResponse)
def scenarios(request: ScenarioRequest) -> ScenarioResponse:
    """Revalue same-currency option units under common deterministic shocks.

    All positions must remain before expiry. No implicit contract multiplier,
    premium financing, trading costs, cash flows or probability weights.
    """
    try:
        return run_scenarios(request)
    except (ValueError, OverflowError, ZeroDivisionError, FloatingPointError) as exc:
        raise HTTPException(422, "Scenario calculation exceeds the supported numerical range.") from exc
