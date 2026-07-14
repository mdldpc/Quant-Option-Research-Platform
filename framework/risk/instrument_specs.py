from dataclasses import dataclass


@dataclass(frozen=True)
class HedgeInstrumentSpec:

    name: str
    instrument_type: str

    delta_per_unit: float
    gamma_per_unit: float
    vega_per_unit: float
    theta_per_unit: float

    min_trade_unit: int = 1

    notes: str = ""


INSTRUMENT_SPECS = {

    "IF_futures": HedgeInstrumentSpec(

        name="IF_futures",
        instrument_type="futures",

        delta_per_unit=1.0,
        gamma_per_unit=0.0,
        vega_per_unit=0.0,
        theta_per_unit=0.0,

        notes="Placeholder futures exposure.",
    ),

    "calendar_spread": HedgeInstrumentSpec(

        name="calendar_spread",
        instrument_type="option_structure",

        delta_per_unit=5.0,
        gamma_per_unit=0.02,
        vega_per_unit=180.0,
        theta_per_unit=150.0,

        notes="Placeholder values. Replace with empirical averages.",
    ),

    "strangle": HedgeInstrumentSpec(

        name="strangle",
        instrument_type="option_structure",

        delta_per_unit=0.0,
        gamma_per_unit=0.04,
        vega_per_unit=250.0,
        theta_per_unit=220.0,

        notes="Placeholder values.",
    ),

    "butterfly": HedgeInstrumentSpec(

        name="butterfly",
        instrument_type="option_structure",

        delta_per_unit=0.0,
        gamma_per_unit=0.05,
        vega_per_unit=60.0,
        theta_per_unit=40.0,

        notes="Placeholder values.",
    ),
}


def get_instrument_spec(name):

    if name not in INSTRUMENT_SPECS:
        raise KeyError(name)

    return INSTRUMENT_SPECS[name]


def list_hedge_instruments():

    return list(INSTRUMENT_SPECS.keys())