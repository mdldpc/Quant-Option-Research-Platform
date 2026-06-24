from datetime import datetime

from contract_calendar import (
    get_expiry_date,
    time_to_expiry
)

trade_date = datetime(2025, 1, 1)

for code in [
    "2501",
    "2502",
    "2503",
    "2506"
]:

    expiry = get_expiry_date(code)

    T = time_to_expiry(
        trade_date,
        code
    )

    print(
        code,
        expiry.date(),
        round(T, 6)
    )