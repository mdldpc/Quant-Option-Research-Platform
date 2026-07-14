# Trade Construction Rules Specification

**Version:** v1.1

**Status:** Draft

**Project:** Quant Option Research Framework

---

# 1. Purpose

This document defines the rules for converting trading signals into executable option positions.

The objective is to ensure that every strategy uses a consistent, reproducible, and auditable trade construction process.

---

# 2. Scope

This specification defines:

- Trade construction
- Contract selection
- Snapshot selection
- Expiry selection
- Calendar pair selection
- Missing data handling
- Trade lifecycle

This specification does NOT define:

- Signal generation
- Portfolio allocation
- Position sizing
- Execution cost model
- Transaction cost model

These topics are governed by separate specifications.

---

# 3. Design Philosophy

The following principles govern the entire Strategy Framework.

## Principle G1

Signals determine **when** to trade.

Signals never determine which contracts to trade.

---

## Principle G2

Snapshots determine **what** to trade.

The Snapshot dataset is the single source of truth for tradable contracts.

---

## Principle G3

Trade construction must never reference contracts that do not exist in the Snapshot universe.

A missing contract should be interpreted as a trade construction issue rather than a market data issue.

---

## Principle G4

Trade construction should always be deterministic.

Given identical signals and identical snapshots, the generated trades must always be identical.

---

# 4. General Trade Lifecycle

The standard lifecycle is:

Signal
↓

Snapshot Universe

↓

Contract Selection

↓

Trade Construction

↓

Backtest

↓

Performance Evaluation

---

# 5. Snapshot Rules

## Rule S1

Trade construction must always use Snapshot datasets.

Raw option tables shall never be used directly during trade construction.

---

## Rule S2

Current execution snapshot:

latest_valid

This rule may be replaced by a fixed execution time in future versions.

Examples:

- 14:55
- 14:59:50
- Market Close

---

# 6. Expiry Selection Rules

## Rule E1

Expiry selection is determined from the Snapshot available on the entry date.

---

## Rule E2

If multiple expiries exist, strategy-specific rules determine which expiry is selected.

---

## Rule E3

Once selected, the expiry remains fixed throughout the trade.

Automatic expiry rollover is NOT permitted.

---

## Rule E4

If the selected expiry disappears before exit, the trade is terminated.

The trade is NOT automatically reconstructed.

---

# 7. Strategy Rules

## 7.1 Long ATM Strangle

### Entry

Entry Date:

Signal entry date.

Expiry:

Nearest available expiry from Snapshot.

Strike Selection:

Nearest ATM call and nearest ATM put.

---

### Exit

Exit Date:

Signal exit date.

Contract:

Same expiry selected at entry.

---

### Missing Contract

If the selected expiry no longer exists,

Trade Status:

contract_expired

---

## 7.2 Long Call Butterfly

### Entry

Entry Date:

Signal entry date.

Expiry:

Nearest available expiry.

Strike Construction:

ATM-centered butterfly.

---

### Premium Filter

Butterfly premium must exceed the minimum premium threshold.

Default threshold:

Premium >= 1

Future versions may replace this threshold with a tick-based rule.

---

### Exit

Same expiry.

No automatic rollover.

---

## 7.3 Calendar Spread

### Entry

Entry Date:

Signal entry date.

Near expiry:

Nearest expiry.

Next expiry:

Second nearest expiry.

---

### Exit

The original expiry pair must remain unchanged.

Example:

Entry:

2602 / 2603

Exit:

2602 / 2603

Allowed.

---

Example:

Entry:

2602 / 2603

Exit:

2603 / 2606

Not allowed.

Trade Status:

calendar_pair_expired

---

Automatic calendar rolling is NOT supported.

Rolling calendars constitute a separate strategy.

---

# 8. Missing Data Rules

The following statuses are valid.

## Expected

expected_missing_abnormal_date

calendar_pair_expired

contract_expired

no_valid_snapshot

---

## Unexpected

missing_snapshot

missing_entry_snapshot

missing_exit_snapshot

These indicate implementation errors or data integrity problems.

Unexpected statuses should be investigated before research conclusions are drawn.

---

# 9. Research Quality Rules

Research datasets must satisfy the following:

Every trade must be reproducible.

Every contract must exist in Snapshot.

Every expiry selection must be deterministic.

Every missing trade must have an explicit reason.

No hidden assumptions are permitted.

---

# 10. Future Extensions

The following features are intentionally excluded from Version 1.1.

- Expiry rolling
- Calendar rolling
- Portfolio allocation
- Multi-strategy capital allocation
- Position sizing
- Bid/Ask execution model
- Slippage
- Transaction costs
- Margin model
- Greeks hedging
- Dynamic delta hedging

Each feature should be introduced through a dedicated specification.

---

# 11. Summary

Trade construction is governed by two fundamental principles.

Signals determine **when** to trade.

Snapshots determine **what** to trade.

This separation ensures that trading strategies remain reproducible, deterministic, and independent of future data pipeline implementations.