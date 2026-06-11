from src.prompt_parser import parse_strategy_prompt
from src.config_validator import validate_strategy_config
from src.data_loader import load_historical_data
from src.data_loader import filter_data_by_date
from src.data_loader import prepare_sample_for_llm
from src.llm_backtester import run_llm_preliminary_backtest
from src.backtest_engine import run_python_backtest
from src.report_generator import save_trade_report
from src.report_generator import save_json_report
from src.evaluator import create_evaluation_report
from src.ai_result_analyzer import generate_ai_final_report


def run_strategylab_workflow(user_prompt):
    strategy_config = parse_strategy_prompt(user_prompt)

    validation_result = validate_strategy_config(strategy_config)

    if not validation_result["is_valid"]:
        return {
            "success": False,
            "error_stage": "validation",
            "message": "Strategy validation failed",
            "strategy_config": strategy_config,
            "validation_result": validation_result
        }

    strategy_config = validation_result["config"]

    df = load_historical_data("data/nifty_day.csv")

    filtered_df = filter_data_by_date(
        df,
        strategy_config["from_date"],
        strategy_config["to_date"]
    )

    if len(filtered_df) == 0:
        return {
            "success": False,
            "error_stage": "data_loading",
            "message": "No historical data found for selected date range.",
            "strategy_config": strategy_config
        }

    # MVP mode: same 10 rows for LLM and Python
    sample_df = filtered_df.head(10)

    historical_sample = prepare_sample_for_llm(
        sample_df,
        max_rows=10
    )

    ai_preliminary_result = run_llm_preliminary_backtest(
        strategy_config,
        historical_sample
    )

    trades, python_summary = run_python_backtest(
        strategy_config,
        sample_df
    )

    evaluation_report = create_evaluation_report(
        ai_preliminary_result,
        python_summary
    )

    ai_final_report = generate_ai_final_report(
        strategy_config,
        python_summary,
        evaluation_report
    )

    trade_report_path = save_trade_report(trades)

    summary_report_path = save_json_report(
        python_summary,
        report_name="summary_report"
    )

    ai_preliminary_report_path = save_json_report(
        ai_preliminary_result,
        report_name="ai_preliminary_report"
    )

    evaluation_report_path = save_json_report(
        evaluation_report,
        report_name="evaluation_report"
    )

    ai_final_report_path = save_json_report(
        ai_final_report,
        report_name="ai_final_report"
    )

    return {
        "success": True,
        "strategy_config": strategy_config,
        "rows_loaded_for_period": len(filtered_df),
        "rows_used_for_mvp": len(sample_df),
        "ai_preliminary_result": ai_preliminary_result,
        "python_summary": python_summary,
        "trades": trades,
        "evaluation_report": evaluation_report,
        "ai_final_report": ai_final_report,
        "report_paths": {
            "trade_report": trade_report_path,
            "summary_report": summary_report_path,
            "ai_preliminary_report": ai_preliminary_report_path,
            "evaluation_report": evaluation_report_path,
            "ai_final_report": ai_final_report_path
        }
    }