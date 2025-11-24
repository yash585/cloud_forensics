import os
import json

REPORT_FILE = os.path.join("reports", "final_report.json")

def save_report(data):
    """
    Saves final parsed volatility results to a JSON file.
    """
    os.makedirs("reports", exist_ok=True)

    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return REPORT_FILE


def load_report():
    """
    Loads report JSON file if available.
    """
    if not os.path.exists(REPORT_FILE):
        return None

    with open(REPORT_FILE, "r") as f:
        return json.load(f)
