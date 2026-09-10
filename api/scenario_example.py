"""Generate the synthetic report, JSON evidence and heatmaps without market data.

Run: python -m api.scenario_example
Optionally: python -m api.scenario_example --output-dir path/to/output
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from api.scenario_schemas import ScenarioRequest
from api.scenarios import run_scenarios


def case_inputs():
    common = dict(spot=100, rate=0.04)
    positions = [
        dict(**common, position_id="long_call_100", quantity=10, strike=100,
             maturity=0.5, volatility=0.25, option_type="call"),
        dict(**common, position_id="short_put_95", quantity=-6, strike=95,
             maturity=0.75, volatility=0.28, option_type="put"),
        dict(**common, position_id="short_call_110", quantity=-4, strike=110,
             maturity=0.5, volatility=0.25, option_type="call"),
    ]
    scenarios = [
        dict(name="No shock"),
        dict(name="Small combined shock", spot_return=0.01, volatility_shift=0.005, days_elapsed=1),
        dict(name="Downside with volatility rise", spot_return=-0.10, volatility_shift=0.05, days_elapsed=7),
        dict(name="Severe downside", spot_return=-0.20, volatility_shift=0.10, days_elapsed=7),
        dict(name="Upside", spot_return=0.10, days_elapsed=7),
        dict(name="Time only", days_elapsed=7),
        dict(name="Rate only", rate_shift=0.01),
    ]
    return dict(positions=positions, scenarios=scenarios)


def save_heatmap(values, spot_shocks, vol_shifts, title, color_label, path):
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    fig.subplots_adjust(left=0.13, right=0.94, top=0.84, bottom=0.14)
    fig.patch.set_facecolor("#f8fafc")
    limit = max(float(np.abs(values).max()), 1e-9)
    image = ax.imshow(values, cmap="RdBu", vmin=-limit, vmax=limit, aspect="auto")
    ax.set_xticks(range(len(spot_shocks)), [f"{v:+.0%}" for v in spot_shocks])
    ax.set_yticks(range(len(vol_shifts)), [f"{100 * v:+g}" for v in vol_shifts])
    ax.set_xlabel("Relative spot shock", labelpad=12)
    ax.set_ylabel("Volatility shift (percentage points)", labelpad=12)
    ax.set_title(title + "\nSynthetic option units | 7 calendar days elapsed | rate unchanged", pad=16)
    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            value = values[row, column]
            ax.text(column, row, f"{value:+.2f}", ha="center", va="center",
                    color="white" if abs(value) > 0.55 * limit else "#172033", fontsize=10)
    fig.colorbar(image, ax=ax, label=color_label, shrink=0.86)
    fig.savefig(path, dpi=160, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)


def generate(output):
    output.mkdir(parents=True, exist_ok=True)
    inputs = case_inputs()
    results = run_scenarios(ScenarioRequest(**inputs))
    spot_shocks = [-0.20, -0.10, -0.05, 0, 0.05, 0.10, 0.20]
    vol_shifts = [-0.05, -0.025, 0, 0.025, 0.05, 0.10]
    grid_inputs = dict(positions=inputs["positions"], scenarios=[
        dict(name=f"spot={spot:+.3f};vol={vol:+.3f}", spot_return=spot,
             volatility_shift=vol, days_elapsed=7)
        for vol in vol_shifts for spot in spot_shocks
    ])
    grid = run_scenarios(ScenarioRequest(**grid_inputs))
    shape = (len(vol_shifts), len(spot_shocks))
    pnl = np.array([r.full_revaluation_pnl for r in grid.scenarios]).reshape(shape)
    error = np.array([r.approximation_error for r in grid.scenarios]).reshape(shape)
    save_heatmap(pnl, spot_shocks, vol_shifts, "Portfolio P&L: full revaluation",
                 "P&L (currency units)", output / "pnl_heatmap.png")
    save_heatmap(error, spot_shocks, vol_shifts, "Approximation error: full minus Greeks",
                 "Signed error (currency units)", output / "approximation_error.png")
    for name, data in [
        ("inputs.json", inputs), ("results.json", results.model_dump()),
        ("grid_inputs.json", grid_inputs), ("grid_results.json", grid.model_dump()),
    ]:
        (output / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    downside = results.scenarios[2]
    small = results.scenarios[1]
    severe = results.scenarios[3]
    worst = min(grid.scenarios, key=lambda item: item.full_revaluation_pnl)
    maximum_error = max(abs(r.approximation_error) for r in grid.scenarios)
    rows = "\n".join(
        f"| {r.name} | {r.stressed_value:.4f} | {r.full_revaluation_pnl:+.4f} | "
        f"{r.approximation_pnl:+.4f} | {r.approximation_error:+.4f} |"
        for r in results.scenarios
    )
    position_rows = "\n".join(
        f"| {p.position_id} | {p.base_value:.4f} | {p.stressed_value:.4f} | "
        f"{p.full_revaluation_pnl:+.4f} | {p.approximation_pnl:+.4f} |"
        for p in downside.positions
    )
    components = "\n".join(f"| {key.title()} | {value:+.4f} |"
                            for key, value in downside.components.model_dump().items())
    report = f"""# Derivatives Valuation and Scenario Risk: Synthetic Case Study

## Executive findings

The illustrative portfolio has a net model value of **{results.base_value:.4f} currency units**.
A 10% spot decline, 5-percentage-point volatility increase and seven elapsed
calendar days produce a full-revaluation P&L of **{downside.full_revaluation_pnl:+.4f}**.
The Greeks approximation gives **{downside.approximation_pnl:+.4f}**, leaving a signed
difference of **{downside.approximation_error:+.4f}** (full minus approximation).

The small combined shock has absolute approximation error {abs(small.approximation_error):.4f};
the severe downside case has error {abs(severe.approximation_error):.4f}. These measured
cases illustrate the limits of a local approximation. They do not establish an
error bound for arbitrary instruments, parameters or scenarios.

All inputs are synthetic. This is an educational, reproducible model-validation
case, not a client engagement, observed trading result or investment recommendation.

## Instrument terms and conventions

| Position ID | Quantity | Type | Strike | Maturity (years) | Volatility |
| --- | ---: | --- | ---: | ---: | ---: |
| long_call_100 | 10 | European call | 100 | 0.50 | 25% |
| short_put_95 | -6 | European put | 95 | 0.75 | 28% |
| short_call_110 | -4 | European call | 110 | 0.50 | 25% |

All options reference the same synthetic spot of 100 and a 4% continuously
compounded rate. All values share one currency. Quantities are option units;
there is no implicit 100-share or exchange contract multiplier. Negative
quantities represent short positions. Dividends are zero.

`spot_return=-0.10` means a 10% relative decline. `volatility_shift=0.05`
means an additive five-percentage-point change, not a 5% relative change.
`rate_shift=0.01` means 100 basis points. Elapsed calendar days use ACT/365.
The small combined shock is +1% spot, +0.5 volatility percentage points and
one day elapsed. Severe downside is -20% spot, +10 volatility percentage points
and seven days. Upside is +10% spot and seven days. Time-only is seven days;
rate-only is +100 basis points. Unspecified shocks are zero.

## Method and validation

Full revaluation reprices each option using Black-Scholes at the stressed
spot, volatility, rate and remaining maturity. Signed position values are
quantity times unit price; portfolio results sum position results.

The local approximation uses base-date sensitivities:

```text
P&L ≈ quantity × (Delta × dS + 0.5 × Gamma × dS²
                 + Vega × dVol + calendar-Theta × elapsedYears + Rho × dRate)
```

Theta is per calendar year; Vega and Rho are per 1.0 decimal change.
Gamma captures spot curvature. Volatility curvature, cross derivatives such
as Vanna and higher orders are omitted. Changes in volatility and time can
therefore amplify the difference from full revaluation.

Pricing is supported by the [independent valuation validation](../valuation_validation.md).
Scenario tests additionally verify quantity-weighted aggregation, no-shock and
offsetting identities, a call-minus-put replication identity, Theta/Rho finite
differences and small-shock approximation accuracy. These are implementation
checks under shared assumptions, not market calibration or external model approval.

## Scenario results

Base value: {results.base_value:.4f}. All table values are in currency units.

| Scenario | Stressed value | Full P&L | Approximate P&L | Full minus approximate |
| --- | ---: | ---: | ---: | ---: |
{rows}

### Position contributions: downside with volatility rise

| Position | Base value | Stressed value | Full P&L contribution | Approximate P&L |
| --- | ---: | ---: | ---: | ---: |
{position_rows}

The put's unit price rises in this downside scenario, increasing the liability
of the short position and producing a negative P&L contribution. The short call
can offset part of the directional loss. The differing strikes and maturities
mean these positions do not form a perfect hedge.

### Approximation attribution for the downside case

| Base sensitivity term | P&L contribution |
| --- | ---: |
{components}

These terms sum to the approximate P&L. They are Taylor terms, not a unique
allocation of the full-revaluation P&L. The remainder is the approximation error.

## Risk maps

The 42 grid scenarios combine spot shocks from -20% to +20% with volatility
shifts from -5 to +10 percentage points; seven days elapse and rates stay fixed.

![Full-revaluation P&L](pnl_heatmap.png)

![Signed approximation error](approximation_error.png)

The worst grid point is `{worst.name}` with P&L {worst.full_revaluation_pnl:+.4f}.
The largest absolute approximation error on this grid is {maximum_error:.4f}.
This worst point is only the minimum of the selected grid, not a worst-case
loss bound. Scenarios have no assigned probabilities; these outputs are not VaR.

## Model limitations and practical implications

This analysis isolates option mark-to-model changes. It excludes cash balances,
premium financing, collateral, margin calls, transaction costs, dividends,
counterparty/default risk and FX translation. Negative net option value is
a signed liability, not evidence of negative total account equity.

Inputs do not model a calibrated volatility surface, stochastic volatility,
early exercise or a realized price path. The API applies common shocks to all
positions and does not infer correlations. Cross-currency inputs must not be
summed without prior conversion. All positions must remain before expiry;
at-expiry and post-expiry requests are rejected because settlement and cash
flows need a separate specification. Invalid stressed volatility is also rejected.

For large shocks, use full revaluation as the model-consistent scenario result
and the approximation as a diagnostic. Suitability of the pricing model and
market inputs requires separate assessment. The service is a research demo;
authentication, rate limiting and production operations are outside this scope.

## Reproduce and inspect

From the repository root with dependencies installed:

```powershell
python -m pytest tests -q
python -m api.scenario_example
uvicorn api.main:app --reload
```

Send `inputs.json` to POST `/risk/scenarios` or inspect `/docs` for the schema.
`results.json` contains unrounded scenario and position results. `grid_inputs.json`
and `grid_results.json` contain the exact inputs and results behind both figures.
The generator writes only this case-study directory by default and requires
no external data, credentials or network access.

## Interview discussion

- Explain signed units, volatility percentage points and the ACT/365 time basis.
- Derive why Theta has the opposite sign from the maturity derivative.
- Use the call-minus-put identity to explain an independent scenario check.
- Explain why small-shock agreement does not imply accurate large-shock hedging.
- Distinguish model implementation validation from validation against market data.
"""
    (output / "README.md").write_text(report, encoding="utf-8")
    print(json.dumps({"report": str(output / "README.md"), "base_value": results.base_value,
                      "downside_pnl": downside.full_revaluation_pnl,
                      "downside_approximation": downside.approximation_pnl,
                      "grid_max_absolute_error": maximum_error}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "docs" / "scenario_case_study")
    generate(parser.parse_args().output_dir)
