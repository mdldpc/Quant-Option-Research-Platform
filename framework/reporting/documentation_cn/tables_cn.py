import pandas as pd


def project_snapshot(nav_df, clean_df):

    if nav_df.empty:
        trading_days = 0
        active_days = 0
        final_nav = 0
        max_dd = 0

    else:

        trading_days = len(nav_df)

        active_days = int(
            (nav_df["positions"] > 0).sum()
        )

        final_nav = float(
            nav_df["current_nav"].iloc[-1]
        )

        max_dd = float(
            nav_df["drawdown"].min()
        )

    return pd.DataFrame(

        [

            ["文档版本","v3.0"],

            ["交易日数量",trading_days],

            ["有效交易时段",len(clean_df)],

            ["持仓交易日",active_days],

            [

                "策略",

                "ATM Straddle Prototype、Long ATM Strangle、Butterfly、Calendar",

            ],

            [

                "最终净值",

                f"{final_nav:,.2f}",

            ],

            [

                "最大回撤",

                f"{max_dd:.4%}",

            ],

            [

                "日度自动化流水线",

                "已完成",

            ],

            [

                "Word 技术白皮书",

                "已完成",

            ],

        ],

        columns=[

            "指标",

            "数值",

        ],

    )

def portfolio_summary(nav_df: pd.DataFrame) -> pd.DataFrame:
    if nav_df.empty:
        return pd.DataFrame(
            [
                ["最终净值", "0.00"],
                ["最高净值", "0.00"],
                ["最低净值", "0.00"],
                ["最大回撤", "0.0000%"],
                ["最佳单日损益", "0.00"],
                ["最差单日损益", "0.00"],
                ["持仓交易日", 0],
                ["交易日总数", 0],
            ],
            columns=[
                "指标",
                "数值",
            ],
        )

    return pd.DataFrame(
        [
            [
                "最终净值",
                f"{float(nav_df['current_nav'].iloc[-1]):,.2f}",
            ],
            [
                "最高净值",
                f"{float(nav_df['current_nav'].max()):,.2f}",
            ],
            [
                "最低净值",
                f"{float(nav_df['current_nav'].min()):,.2f}",
            ],
            [
                "最大回撤",
                f"{float(nav_df['drawdown'].min()):.4%}",
            ],
            [
                "最佳单日损益",
                f"{float(nav_df['unrealized_pnl'].max()):,.2f}",
            ],
            [
                "最差单日损益",
                f"{float(nav_df['unrealized_pnl'].min()):,.2f}",
            ],
            [
                "持仓交易日",
                int((nav_df["positions"] > 0).sum()),
            ],
            [
                "交易日总数",
                len(nav_df),
            ],
        ],
        columns=[
            "指标",
            "数值",
        ],
    )

def phase1_backtest_metrics():

    return pd.DataFrame(
        [
            [
                "交易次数",
                4,
            ],
            [
                "盈利交易次数",
                3,
            ],
            [
                "亏损交易次数",
                1,
            ],
            [
                "胜率",
                "75%",
            ],
            [
                "最终净值",
                "1.305",
            ],
            [
                "累计收益率",
                "30.5%",
            ],
            [
                "最大回撤",
                "-0.92%",
            ],
            [
                "平均持仓时间",
                "约4个交易日",
            ],
        ],
        columns=[
            "指标",
            "数值",
        ],
    )