LONG_ATM_STRANGLE = {

    "metadata": {

        "strategy_id": "S001",

        "name": "Long ATM Strangle",

        "category": "Volatility",

        "research_stage": "Prototype",

        "implementation_status": "Completed",

        "portfolio_support": True,

        "risk_support": True,

        "hedge_support": True,

        "report_support": True,

        "created": "2026-01",

        "last_updated": "2026-06",

    },


    "title": "10.1 Long ATM Strangle",


    "snapshot": [

        ["Strategy ID", "S001"],

        ["Category", "Volatility"],

        ["Research Stage", "Prototype"],

        ["Implementation", "Completed"],

        ["Portfolio Integration", "Yes"],

        ["Risk Monitoring", "Yes"],

        ["Hedge Recommendation", "Yes"],

        ["Historical Backtest", "Completed"],

        ["Documentation", "Complete"],

    ],


    "overview":

        """
        Long ATM Strangle is a long-volatility strategy designed to benefit
        from significant underlying price movements regardless of direction.

        The strategy purchases a near-the-money call and put option with the
        same maturity and seeks situations where realized volatility exceeds
        implied volatility.
        """,


    "motivation": [

        "Capture volatility expansion.",

        "Reduce dependence on directional prediction.",

        "Create a baseline volatility strategy.",

        "Provide a foundation for portfolio volatility allocation.",

    ],


    "research_questions": [

        "Can volatility signals identify profitable long-volatility opportunities?",

        "Can implied volatility underestimate future realized volatility?",

        "Can this strategy improve portfolio diversification?",

    ],


    "market_conditions": [

        ["High uncertainty", "Highly suitable"],

        ["Expected volatility expansion", "Highly suitable"],

        ["Large expected movement", "Suitable"],

        ["Low volatility environment", "Not recommended"],

    ],


    "construction": [

        "Buy ATM call.",

        "Buy ATM put.",

        "Use identical maturity.",

        "Enter after signal confirmation.",

    ],


    "payoff": [

        "Profit increases with large movement in either direction.",

        "Maximum loss equals premium paid.",

        "Requires sufficient movement to overcome theta decay.",

    ],


    "greek_profile": [

        ["Delta", "Near Neutral", "Limited directional exposure"],

        ["Gamma", "Positive", "Benefits from movement"],

        ["Vega", "Positive", "Benefits from volatility increase"],

        ["Theta", "Negative", "Time decay cost"],

    ],


    "entry_rules": [

        "Signal score exceeds entry threshold.",

        "Liquidity requirements are satisfied.",

        "Portfolio risk remains acceptable.",

    ],


    "exit_rules": [

        "Profit target reached.",

        "Signal weakens.",

        "Maximum holding period reached.",

        "Risk limit exceeded.",

    ],


    "performance": [

        ["Evaluation", "Backtested on current 2026 sample"],

        ["Trades", "Generated dynamically"],

        ["Status", "Preliminary validation"],

    ],


    "evidence": [

        ["Payoff Analysis", "Available"],

        ["Greeks Analysis", "Available"],

        ["Portfolio Integration", "Available"],

        ["Risk Monitoring", "Available"],

        ["Backtest", "Completed"],

    ],


    "advantages": [

        "Direction neutral.",

        "Simple structure.",

        "Positive volatility exposure.",

    ],


    "limitations": [

        "Negative theta.",

        "Requires large movement.",

        "Sensitive to volatility crush.",

    ],


    "future_work": [

        "Adaptive signal.",

        "Dynamic strike selection.",

        "Transaction cost optimization.",

    ],


    "references": [

        "Black (1976)",

        "Hull Options, Futures and Other Derivatives",

    ],


    "roadmap": [

        ["v1.0", "Prototype"],

        ["v1.1", "Portfolio integration"],

        ["Future", "Adaptive volatility model"],

    ],

}