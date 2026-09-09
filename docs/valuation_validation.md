# European Option Valuation and Model Validation

## Purpose and scope

This independent API extension compares a Black-Scholes closed-form price with
a Cox-Ross-Rubinstein (CRR) binomial price. The case study uses synthetic inputs,
not market quotes or a client portfolio. It demonstrates numerical verification,
not evidence that either model accurately describes observed market prices.

Both implementations assume European exercise, zero dividends, constant
volatility and a constant continuously compounded risk-free rate. Time is in
years; rates and volatility are decimals. Prices are per option unit in the
same currency as spot and strike, without a contract multiplier.

## Implementation

`api/valuation.py` contains independent numerical functions. The CRR model uses
u = exp(sigma * sqrt(T / N)), d = 1 / u and
p = (exp(r * T / N) - d) / (u - d). Terminal payoffs are discounted through
backward induction. Runtime is O(N squared), with O(N) memory. The API accepts
integer steps from 1 to 2,000 (default 500). Invalid risk-neutral probabilities
are rejected rather than clipped; increasing steps may resolve a coarse tree.
Non-finite inputs, invalid domains and numerical overflow produce HTTP 422.

The pricing functions expect schema-validated inputs. Existing Black-76 research
functions are not reused because their underlying-price convention differs.
The existing Greeks service and research pipeline are unchanged.

## Reproduction

From the repository root, activate the environment with requirements installed:

```powershell
python -m pytest tests -q
python -m api.valuation_example
uvicorn api.main:app --reload
```

Use POST `/valuation/price` with:

```json
{"spot":100,"strike":100,"maturity":1,"rate":0.05,"volatility":0.2,"option_type":"call","steps":500}
```

The response contains `black_scholes_price`, `binomial_price`, `absolute_error`
and `steps`. Swagger UI is available at `/docs`. No historical data is needed.

## Synthetic convergence results

S = K = 100; T = 1 year; r = 5%; volatility = 20%.
The following table is reproduced by `python -m api.valuation_example`.

| Type | Steps | Black-Scholes | CRR | Absolute error |
| --- | ---: | ---: | ---: | ---: |
| call | 25 | 10.45058357 | 10.52096562 | 0.07038205 |
| call | 50 | 10.45058357 | 10.41069154 | 0.03989203 |
| call | 100 | 10.45058357 | 10.43061166 | 0.01997191 |
| call | 250 | 10.45058357 | 10.44258871 | 0.00799486 |
| call | 500 | 10.45058357 | 10.44658514 | 0.00399844 |
| call | 1000 | 10.45058357 | 10.44858410 | 0.00199947 |
| put | 25 | 5.57352602 | 5.64390807 | 0.07038205 |
| put | 50 | 5.57352602 | 5.53363399 | 0.03989203 |
| put | 100 | 5.57352602 | 5.55355411 | 0.01997191 |
| put | 250 | 5.57352602 | 5.56553116 | 0.00799486 |
| put | 500 | 5.57352602 | 5.56952759 | 0.00399844 |
| put | 1000 | 5.57352602 | 5.57152655 | 0.00199947 |

For this case, the 1,000-step absolute error is approximately 0.002 currency
units. This is not a universal error bound. Odd/even tree alignment can cause
oscillating errors; convergence tests compare coarse and fine grids without
assuming every increase in steps decreases the error.

## Verification evidence

The local suite passed 123 parameterized cases: 84 existing API cases and 39
new valuation cases. The environment emitted one Starlette/httpx test-client
deprecation warning. Historical data-dependent research scripts were not run.

New checks cover fixed call/put benchmarks, a hand-worked one-step tree,
put-call parity across negative/zero/positive rates, convergence at three spot
levels, and centered finite differences for Delta, Gamma and Vega for calls
and puts. Spot perturbations are S * 0.0001; volatility perturbations are
0.00001. Absolute Greek tolerances are 1e-7 for Delta/Gamma and 1e-6 for Vega.
These checks cover representative cases, not the entire floating-point domain.

## Interpretation and limitations

Agreement provides evidence of implementation consistency under shared
assumptions. It does not validate those assumptions against market data.
Dividends, early exercise, volatility smiles, funding differences, liquidity
and transaction costs are outside this version. Extreme inputs can exceed
floating-point limits. Deep out-of-the-money closed-form prices may lose
relative precision through subtraction; nonnegative rounding is enforced.

For a valuation engagement, appropriate market inputs, instrument terms and
model suitability would require separate review. This service is a research
demonstration, without authentication, rate limits or production deployment.
