def apply_transaction_cost(
    gross_return,
    commission_rate=0.0,
    slippage_rate=0.0,
    bid_ask_spread_rate=0.0,
):
    total_cost = commission_rate + slippage_rate + bid_ask_spread_rate
    return gross_return - total_cost


def apply_total_cost(gross_return, total_cost=0.0):
    return gross_return - total_cost