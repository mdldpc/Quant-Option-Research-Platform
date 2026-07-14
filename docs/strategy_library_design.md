# Strategy Library Design

## Purpose

The Strategy Library is designed to evaluate multiple option strategy prototypes under a unified volatility and Greeks framework.

The objective is not to build production-ready trading systems, but to compare how different option structures respond to the same volatility signals, term structure conditions, and risk exposures.

---

## Design Principle

The strategy library follows one principle:

Same market view, different payoff structures.

All strategies should be connected to one or more of the following research views:

1. Implied volatility is unusually low or high.
2. ATM implied volatility exhibits partial mean reversion.
3. Volatility term structure may contain relative-value opportunities.
4. Greeks exposure should be measurable and comparable across strategies.

---

## Strategy Groups

### 1. Volatility Direction Strategies

These strategies express a direct view on future volatility.

Included strategies:

- Long ATM Straddle
- Long ATM Strangle

### 2. Hedged Exposure Strategies

These strategies aim to isolate option Greeks such as Vega and Gamma while reducing directional exposure.

Included strategies:

- Delta-Hedged Long Call
- Delta-Hedged Long Put

### 3. Term Structure Strategies

These strategies trade relative differences between near-term and longer-term implied volatility.

Included strategies:

- Calendar Spread

---

## Strategies Included in v1.1

| Strategy | Purpose | Market View |
|---|---|---|
| Long ATM Straddle | Baseline long-volatility strategy | IV mean reversion |
| Long ATM Strangle | Cheaper long-volatility exposure | Tail volatility expansion |
| Delta-Hedged Long Call | Isolate Vega/Gamma exposure | Volatility over direction |
| Delta-Hedged Long Put | Isolate downside volatility exposure | Volatility over direction |
| Calendar Spread | Trade term structure difference | Relative value across maturities |

---

## Strategies Not Included in v1.1

The following strategies are intentionally not included in v1.1:

- Butterfly
- Iron Condor
- Bull Call Spread
- Bear Put Spread
- Directional option spreads

These strategies are excluded because they either require more detailed surface calibration, focus more on directional views, or would make the v1.1 strategy library too broad relative to the current research objective.

---

## Unified Strategy Interface

Each strategy should be described using the same structure:

1. Strategy Name
2. Market View
3. Entry Rule
4. Position Construction
5. Exit Rule
6. Payoff Logic
7. Key Greeks
8. Risk Characteristics
9. Data Requirements
10. Limitations

---

## v1.1 Scope

Version 1.1 introduces the strategy library as a research prototype framework.

The strategies are used for feasibility testing, comparison, and future extension. Due to the currently limited sample size, their backtest results should be interpreted as preliminary rather than conclusive.

---

## Future Extensions

Future versions may include:

- Butterfly strategies
- Iron Condor strategies
- Diagonal spreads
- Volatility arbitrage strategies
- Delta-hedged portfolio backtesting
- Cross-market strategy comparison