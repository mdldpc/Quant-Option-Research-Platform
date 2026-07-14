RISK_ACTIONS = {
    "positive_delta":
        "Sell IF futures (or equivalent delta) to reduce positive delta exposure.",

    "negative_delta":
        "Buy IF futures (or equivalent delta) to reduce negative delta exposure.",

    "high_gamma":
        "Reduce option position size or shorten holding period.",

    "high_vega":
        "Reduce long volatility exposure or partially close option positions.",

    "high_theta":
        "Monitor theta decay closely and consider exiting earlier."
}


def classify_risk(row):
    """
    Return a list of risk tags.
    """

    tags = []

    if row.get("delta_warning", False):
        if row.get("net_delta", 0) > 0:
            tags.append("positive_delta")
        else:
            tags.append("negative_delta")

    if row.get("gamma_warning", False):
        tags.append("high_gamma")

    if row.get("vega_warning", False):
        tags.append("high_vega")

    if row.get("theta_warning", False):
        tags.append("high_theta")

    return tags


def recommend_risk_action(row):
    """
    Convert risk tags into hedge recommendations.
    """

    tags = classify_risk(row)

    if not tags:
        return "No immediate hedge action required."

    return " | ".join(RISK_ACTIONS[tag] for tag in tags)