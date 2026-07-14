LONG_CALL_BUTTERFLY = {
    "metadata": {
        "strategy_id": "S002",
        "name": "Long Call Butterfly",
        "category": "Convexity / Defined Risk",
        "research_stage": "Prototype",
        "implementation_status": "Completed",
        "portfolio_support": True,
        "risk_support": True,
        "hedge_support": True,
        "report_support": True,
        "created": "2026-04",
        "last_updated": "2026-06",
    },

    "title": "10.2 Long Call Butterfly",

    "snapshot": [
        ["Strategy ID", "S002"],
        ["Category", "Convexity / Defined Risk"],
        ["Research Stage", "Prototype"],
        ["Implementation", "Completed"],
        ["Portfolio Integration", "Yes"],
        ["Risk Monitoring", "Yes"],
        ["Hedge Recommendation", "Yes"],
        ["Historical Backtest", "Completed on current 2026 sample"],
        ["Documentation", "Complete"],
    ],

    "overview": (
        "The Long Call Butterfly is a defined-risk option structure constructed with three "
        "call strikes. It is designed to benefit when the underlying settles near the middle "
        "strike. The strategy has limited downside and limited upside, making it useful for "
        "researching convexity, strike selection, and range-based market views."
    ),

    "motivation": [
        "Study defined-risk convexity structures.",
        "Compare limited-risk structures with outright long-volatility premium-buying strategies.",
        "Explore payoff concentration around a selected target strike.",
        "Provide a strategy type that can be monitored through portfolio Greeks.",
    ],

    "research_questions": [
        "Can strike-centered convexity structures improve risk-adjusted performance?",
        "How sensitive is performance to middle-strike selection?",
        "Can butterfly structures reduce premium cost relative to outright long volatility?",
        "Can butterfly positions be integrated into a multi-strategy option portfolio?",
    ],

    "market_conditions": [
        ["Expected settlement near target strike", "Highly suitable"],
        ["Moderate directional or range-bound view", "Suitable"],
        ["Low-cost convexity opportunity", "Suitable"],
        ["Large breakout market", "Less suitable"],
        ["Strong volatility expansion", "Less suitable than strangle"],
    ],

    "construction": [
        "Buy one lower-strike call option.",
        "Sell two middle-strike call options.",
        "Buy one upper-strike call option.",
        "Use approximately symmetric strike spacing when possible.",
        "Use the same expiry for all legs.",
    ],

    "payoff": [
        "Maximum profit occurs when the underlying settles near the middle strike at expiry.",
        "Maximum loss is limited to the net premium paid.",
        "The payoff is bounded on both upside and downside.",
        "The strategy is sensitive to strike placement and time to expiration.",
    ],

    "greek_profile": [
        ["Delta", "Depends on underlying location", "Can be directional near entry"],
        ["Gamma", "Nonlinear / location-dependent", "Convexity changes across price regions"],
        ["Vega", "Usually limited", "Less pure long-volatility exposure than strangle"],
        ["Theta", "Location-dependent", "Can be favorable near the middle strike"],
    ],

    "entry_rules": [
        "Target strike is identified from current underlying level or strategy signal.",
        "Strike spacing is valid and approximately symmetric.",
        "Net premium is within acceptable risk budget.",
        "Portfolio-level Greeks remain within risk limits.",
    ],

    "exit_rules": [
        "Profit target is reached.",
        "Underlying moves away from the target zone.",
        "Maximum holding period is reached.",
        "Risk exposure becomes inconsistent with portfolio limits.",
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
        "Defined maximum loss.",
        "Lower premium cost than outright long straddle or strangle.",
        "Useful for range-bound or target-price research.",
        "Can be integrated into portfolio risk monitoring.",
    ],

    "limitations": [
        "Profit zone is narrow.",
        "Performance depends strongly on strike selection.",
        "Limited upside even if the market moves strongly.",
        "Historical sample is currently limited.",
        "Transaction-cost and slippage assumptions require further calibration.",
    ],

    "future_work": [
        "Automated strike selection.",
        "Dynamic width selection.",
        "Full butterfly backtesting across all available trading days.",
        "Transaction-cost-aware evaluation.",
        "Comparison with strangle and calendar structures.",
    ],

    "references": [
        "Options spread strategy literature",
        "Convexity and payoff engineering",
        "Hull Options, Futures and Other Derivatives",
    ],

    "roadmap": [
        ["v1.0", "Strategy structure implemented"],
        ["v1.1", "Portfolio integration"],
        ["v1.2", "Risk monitoring integration"],
        ["Future", "Full backtest and robustness analysis"],
    ],
}