from pathlib import Path

import pandas as pd

from framework.reporting.documentation.documentation_builder import DocumentationBuilder


OUT_DOCX = Path("research/reports/quant_option_technical_white_paper_v3_0.docx")

NAV_FILE = Path("research/exports/portfolio_nav_timeseries_v1_1.csv")
CLEAN_FILE = Path("research/exports/clean_session_summary_v1_1.csv")


def safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def main():
    nav_df = safe_read_csv(NAV_FILE)
    clean_df = safe_read_csv(CLEAN_FILE)

    builder = DocumentationBuilder(
        nav_df=nav_df,
        clean_df=clean_df,
    )

    builder.build()
    builder.save(OUT_DOCX)

    print("DONE")
    print("Saved:")
    print(OUT_DOCX)


if __name__ == "__main__":
    main()