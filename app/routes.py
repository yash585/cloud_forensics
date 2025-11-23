from flask import Blueprint, render_template, request, jsonify
from .controllers.snapshot_controller import handle_snapshot
from .controllers.volatility_controller import run_volatility_analysis
from .controllers.report_controller import fetch_report

routes = Blueprint("routes", __name__)

# ─────────────────────────────────────────
# Dashboard Home
# ─────────────────────────────────────────
@routes.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────
# 1. Start Snapshot + Memory Dump
# ─────────────────────────────────────────
@routes.route("/api/snapshot", methods=["POST"])
def snapshot():
    instance_id = request.json.get("instance_id")
    if not instance_id:
        return jsonify({"error": "instance_id is required"}), 400

    result = handle_snapshot(instance_id)
    return jsonify(result)


# ─────────────────────────────────────────
# 2. Run Volatility Plugins
# ─────────────────────────────────────────
@routes.route("/api/analyze", methods=["POST"])
def analyze():
    dump_path = request.json.get("dump_path")
    if not dump_path:
        return jsonify({"error": "dump_path is required"}), 400

    result = run_volatility_analysis(dump_path)
    return jsonify(result)


# ─────────────────────────────────────────
# 3. Get Parsed / Final Report Data
# ─────────────────────────────────────────
@routes.route("/api/report", methods=["GET"])
def report():
    report_data = fetch_report()
    return jsonify(report_data)


# ─────────────────────────────────────────
# UI Page for Results
# ─────────────────────────────────────────
@routes.route("/results")
def results():
    return render_template("results.html")


@routes.route("/run-analysis", methods=["POST"])
def run_analysis():
    print("\n\n\n\n\nHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n\n\n\nHeLLLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO\n\n\n\n")
    instance_id = request.form.get("instance_id")

    print("\n\n",instance_id,"\n\n")
    # Step 1: Take snapshot
    snapshot_result = handle_snapshot(instance_id)
    snapshot_id = snapshot_result.get("snapshot_id")
    print(snapshot_id,"\n\n\n\n\n")

    # Step 2: Extract memory dump path (your extractor service will generate it)
    dump_path = snapshot_result.get("dump_path")

    print(dump_path,"\n\n\n\n\n")

    # Step 3: Run volatility plugin
    analysis_result = run_volatility_analysis(dump_path)

    # Step 4: Render results page
    return render_template(
        "results.html",
        snapshot_id=snapshot_id,
        results=analysis_result.get("output", "")
    )
