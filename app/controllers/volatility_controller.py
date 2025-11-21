from app.services.volatility_runner import run_plugins
from app.services.parser import parse_all_outputs

def run_volatility_analysis(dump_path):
    """
    Controller that:
    1. Runs volatility plugins on the memory dump
    2. Parses plugin outputs into structured JSON
    """

    # Step 1: Execute volatility plugins
    raw_outputs = run_plugins(dump_path)

    if raw_outputs is None:
        return {"status": "error", "message": "Volatility execution failed"}

    # Step 2: Parse the output
    parsed_data = parse_all_outputs(raw_outputs)

    return {
        "status": "success",
        "message": "Volatility analysis completed",
        "results": parsed_data
    }
