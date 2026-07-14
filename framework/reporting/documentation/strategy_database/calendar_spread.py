CALENDAR_SPREAD = {
    "metadata": {
        "strategy_id": "S003",
        "name": "Calendar Spread",
        "category": "Term Structure",
        "research_stage": "Prototype",
        "implementation_status": "Completed",
        "portfolio_support": True,
        "risk_support": True,
        "hedge_support": True,
        "report_support": True,
        "created": "2026-04",
        "last_updated": "2026-06",
    },

    "title": "10.3 Calendar Spread",

    "snapshot": [
        ["Strategy ID", "S003"],
        ["Category", "Term Structure"],
        ["Research Stage", "Prototype"],
        ["Implementation", "Completed"],
        ["Portfolio Integration", "Yes"],
        ["Risk Monitoring", "Yes"],
        ["Hedge Recommendation", "Yes"],
        ["Historical Backtest", "Completed on current 2026 sample"],
        ["Documentation", "Complete"],
    ],

    "overview": (
        "The Calendar Spread is a term-structure option strategy that compares near-expiry "
        "and next-expiry option prices or implied volatility. The strategy is designed to "
        "research maturity spread behavior, time decay differences, and term-structure shifts."
    ),

    "motivation": [
        "Study implied volatility term-structure behavior.",
        "Research differences between near-term and next-term option pricing.",
        "Create a strategy connected to maturity spread and theta behavior.",
        "Extend the platform beyond single-expiry volatility structures.",
    ],

    "research_questions": [
        "Can maturity-spread information be converted into systematic option strategies?",
        "How does near-expiry theta interact with next-expiry Vega?",
        "Can calendar spreads provide more stable exposure than outright long volatility?",
        "Can term-structure strategies improve multi-strategy portfolio diversification?",
    ],

    "market_conditions": [
        ["Stable underlying with term-structure opportunity", "Highly suitable"],
        ["Near-term IV distortion", "Suitable"],
        ["Expected term-structure normalization", "Suitable"],
        ["Large immediate directional movement", "Less suitable"],
        ["Severe liquidity imbalance across expiries", "Not recommended"],
    ],

    "construction": [
        "Construct near-expiry option exposure.",
        "Construct next-expiry option exposure.",
        "Compare near and next expiry straddle or option prices.",
        "Enter when the maturity spread or IV spread satisfies strategy conditions.",
        "Monitor Vega, Theta, and term-structure exposure.",
    ],

    "payoff": [
        "Payoff depends on relative changes between near-expiry and next-expiry options.",
        "The strategy is sensitive to time decay and volatility term-structure movement.",
        "It may benefit when the chosen maturity spread normalizes in the expected direction.",
        "Risk depends on underlying movement, IV shift, liquidity, and expiration timing.",
    ],

    "greek_profile": [
        ["Delta", "Can be near neutral", "Depends on selected strikes and expiries"],
        ["Gamma", "Mixed", "Near-expiry leg often has stronger Gamma"],
        ["Vega", "Term-structure sensitive", "Next-expiry leg often dominates Vega exposure"],
        ["Theta", "Mixed", "Near-expiry time decay is important"],
    ],

    "entry_rules": [
        "Near and next expiry contracts are both available.",
        "Term-structure or IV-spread condition is satisfied.",
        "Liquidity across both maturities is acceptable.",
        "Portfolio-level Vega and Theta exposure remain within limits.",
    ],

    "exit_rules": [
        "Spread normalizes or profit target is reached.",
        "Term-structure signal disappears.",
        "Near expiry becomes too close to expiration.",
        "Portfolio-level Vega or Theta risk exceeds threshold.",
    ],

    "performance": [
        ["Evaluation Status", "Backtested / evaluated on current 2026 sample"],
        ["Completed Trades", "Generated dynamically from exported results when available"],
        ["Win Rate", "Generated dynamically from exported results when available"],
        ["Cumulative Return", "Generated dynamically from exported results when available"],
        ["Maximum Drawdown", "Generated dynamically from exported results when available"],
        ["Evidence Status", "Preliminary due to limited sample period"],
    ],

    "evidence": [
        ["Payoff Analysis", "Available"],
        ["Greeks Analysis", "Available"],
        ["Portfolio Integration", "Available"],
        ["Risk Monitoring", "Available"],
        ["Historical Backtest", "Completed on current 2026 sample"],
        ["Transaction Cost Test", "Research-stage / preliminary"],
        ["Robustness Dashboard", "Research-stage / preliminary"],
    ],

    "advantages": [
        "Directly connected to volatility term structure.",
        "Can express relative-value views across maturities.",
        "Useful for studying Theta and Vega interaction.",
        "Integrated into portfolio, risk, and hedge reporting.",
    ],

    "limitations": [
        "More complex than single-expiry strategies.",
        "Sensitive to liquidity across expiries.",
        "Requires careful maturity selection.",
        "Historical sample is currently limited.",
        "Hedge calibration is still approximate.",
    ],

    "future_work": [
        "Automated maturity-pair selection.",
        "Term-structure signal calibration.",
        "Full historical calendar-spread backtesting.",
        "Transaction-cost-aware evaluation.",
        "Integration with volatility regime classification.",
    ],

    "references": [
        "Volatility term-structure strategy literature",
        "Calendar spread option strategy literature",
        "Hull Options, Futures and Other Derivatives",
    ],

    "roadmap": [
        ["v1.0", "Calendar structure implemented"],
        ["v1.1", "Portfolio integration"],
        ["v1.2", "Risk and monitoring integration"],
        ["Future", "Full backtest and term-structure signal calibration"],
    ],
}