from app.services.report import load_report

def fetch_report():
    """
    Controller to load the final parsed analysis report.
    """
    report_data = load_report()

    if not report_data:
        return {"status": "error", "message": "No report available"}

    return {
        "status": "success",
        "report": report_data
    }
