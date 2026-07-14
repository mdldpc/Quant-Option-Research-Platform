def build_toc(report):
    report.heading1("Table of Contents")

    sections = [
        "Executive Summary",
        "Part I - Research Foundation",
        "1. Project Background",
        "2. Dataset and Data Engineering",
        "3. Data Preprocessing and Cleaning",
        "4. Volatility Analytics",
        "5. Signal Methodology",
        "6. Strategy Construction",
        "7. Backtesting Framework",
        "8. Transaction Cost and Robustness Analysis",
        "Part II - Quant Research Platform",
        "9. System Architecture",
        "10. Expanded Strategy Library",
        "11. Portfolio Engine",
        "12. Greeks and Risk Monitoring",
        "13. Hedge Recommendation",
        "14. Automation and Reporting",
        "15. Portfolio Performance",
        "16. Current Limitations and Future Work",
        "Appendix A. Project Directory",
        "Appendix B. Software Environment",
        "Appendix C. Version History",
    ]

    for item in sections:
        report.paragraph(item)

    report.page_break()