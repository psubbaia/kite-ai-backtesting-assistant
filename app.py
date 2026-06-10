import pandas as pd
import streamlit as st

from src.backtest_workflow import run_strategylab_workflow


st.set_page_config(
    page_title="StrategyLab MVP",
    page_icon="📈",
    layout="wide"
)

st.title("📈 StrategyLab MVP — AI-Guided NIFTY Backtester")

st.write(
    "Enter a natural language strategy. "
    "AI will parse the strategy, run an LLM preliminary backtest, "
    "then Python will run a deterministic reference backtest."
)

st.warning(
    "This MVP is for historical backtesting only. "
    "It does not provide live trading advice and does not place orders."
)

st.subheader("Supported MVP Strategies")

st.markdown(
    """
    - `buy_open_sell_close`
    - `moving_average_crossover`
    - `breakout`
    """
)

default_prompt = "Backtest NIFTY buy at open and sell at close for 2024 with quantity 50"

user_prompt = st.text_area(
    "Enter your strategy prompt",
    value=default_prompt,
    height=120
)

run_button = st.button("Run Backtest")

if run_button:
    if not user_prompt.strip():
        st.error("Please enter a strategy prompt.")
    else:
        with st.spinner("Running StrategyLab workflow..."):
            try:
                results = run_strategylab_workflow(user_prompt)
            except Exception as error:
                st.error("Unexpected error occurred.")
                st.exception(error)
                st.stop()

        if not results["success"]:
            st.error(results["message"])

            st.subheader("AI Parsed Strategy Config")
            st.json(results.get("strategy_config", {}))

            st.subheader("Validation Result")
            st.json(results.get("validation_result", {}))

            st.stop()

        st.success("Backtest workflow completed successfully.")

        st.subheader("AI Parsed Strategy Config")
        st.json(results["strategy_config"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Rows Loaded for Selected Period",
                results["rows_loaded_for_period"]
            )

        with col2:
            st.metric(
                "Rows Used in MVP Test",
                results["rows_used_for_mvp"]
            )

        st.subheader("LLM Preliminary Backtest Result")
        st.caption("This is AI preliminary calculation only, not the final verified result.")
        st.json(results["ai_preliminary_result"])

        st.subheader("Python Deterministic Backtest Summary")
        st.caption("This is the deterministic reference result.")
        st.json(results["python_summary"])

        st.subheader("Evaluation Report")
        st.caption("This compares the LLM preliminary result with Python deterministic result.")
        st.json(results["evaluation_report"])

        st.subheader("Executed Trades")

        trade_df = pd.DataFrame(results["trades"])

        if len(trade_df) == 0:
            st.warning("No trades were executed for this strategy.")
        else:
            st.dataframe(trade_df, use_container_width=True)

            total_pnl = results["python_summary"].get("total_pnl", 0)
            win_rate = results["python_summary"].get("win_rate", 0)
            total_trades = results["python_summary"].get("total_trades", 0)

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Total Trades", total_trades)

            with c2:
                st.metric("Win Rate", f"{win_rate}%")

            with c3:
                st.metric("Total P&L", total_pnl)

        st.subheader("Generated Reports")

        st.json(results["report_paths"])

        st.info(
            "MVP mode currently uses the first 10 rows after date filtering "
            "for both LLM and Python so the comparison is fair."
        )