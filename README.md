# StrategyLab MVP — AI-Guided NIFTY Backtester

## Project Goal

StrategyLab MVP is an AI-guided historical backtesting application for NIFTY.

The application accepts a natural language strategy prompt, uses AI to parse it into a structured strategy configuration, performs a preliminary LLM-based calculation, runs a deterministic Python backtest, evaluates the LLM output against Python, and displays results in a Streamlit interface.

## Important Disclaimer

This project is for historical backtesting and learning only.

It does not:
- provide live trading advice
- place orders
- connect to order placement APIs
- guarantee profit

## MVP Architecture

```text
User natural language strategy
        ↓
AI Strategy Parser
        ↓
Allowed Strategy Validator
        ↓
LLM Preliminary Backtest
        ↓
Python Deterministic Backtest
        ↓
Evaluation Layer
        ↓
AI Final Explanation
        ↓
Streamlit UI + Reports