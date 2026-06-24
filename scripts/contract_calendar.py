from datetime import datetime

# =====================================
# CFFEX IO Option Expiry Calendar
# =====================================

EXPIRY_DATES = {

    # January 2025
    "2501": datetime(2025, 1, 17),

    # February 2025
    "2502": datetime(2025, 2, 21),

    # March 2025
    "2503": datetime(2025, 3, 21),

    # June 2025
    "2506": datetime(2025, 6, 20),
    "2601": datetime(2026, 1, 16),
    "2602": datetime(2026, 2, 20),
    "2603": datetime(2026, 3, 20),
    "2606": datetime(2026, 6, 19),
    "2609": datetime(2026, 9, 18),
    "2612": datetime(2026, 12, 18),

}


def get_expiry_date(expiry_code: str):
    """
    Input:
        2501

    Output:
        datetime(2025,1,17)
    """
    return EXPIRY_DATES.get(expiry_code)


def time_to_expiry(
    trade_date: datetime,
    expiry_code: str
):
    """
    Return:
        T in years
    """

    expiry = get_expiry_date(expiry_code)

    if expiry is None:
        return None

    days = (expiry - trade_date).days

    return max(days, 0) / 365.0