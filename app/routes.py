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
