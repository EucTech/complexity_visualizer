from flask import Blueprint, request, jsonify
from db import db

# Blueprint so factorial.py can register these routes
analysis_bp = Blueprint("analysis", __name__)


# Database Model
class Analysis(db.Model):
    __tablename__ = "analysis"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    algo = db.Column(db.String(100), nullable=False)
    items = db.Column(db.Integer, nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Float, nullable=False)
    end_time = db.Column(db.Float, nullable=False)
    total_time_ms = db.Column(db.Float, nullable=False)
    time_complexity = db.Column(db.String(50), nullable=False)
    path_to_graph = db.Column(db.String(500), nullable=True)  # MinIO URL to graph image


# /analyze
@analysis_bp.route("/analyze", methods=["GET"])
def analyze():
    """
    Example: GET /analyze?algo=bubble_sort&n=1000&steps=10
    """
    # import
    from factorial import algo, complexities, time_complexity_visualizer

    algo_name = request.args.get("algo", "bubble_sort").strip('"')
    n = int(request.args.get("n", 1000))
    steps = int(request.args.get("steps", 10))

    if algo_name not in algo:
        return jsonify({
            "error": f"Unknown algorithm '{algo_name}'. "
                     f"Choose from: {list(algo.keys())}"
        }), 404

    algorithm_fn = algo[algo_name]
    step_size = max(1, n // steps)

    times, input_sizes, start, end, total_ms, graph_b64 = time_complexity_visualizer(
        algorithm_fn, step_size, n, step_size
    )

    return jsonify({
        "algo": algo_name,
        "items": n,
        "steps": steps,
        "start_time": start,
        "end_time": end,
        "total_time_ms": total_ms,
        "time_complexity": complexities.get(algo_name, "unknown"),
        "path_to_graph": graph_b64,
    }), 200


# ── POST /save_analysis ───────────────────────────────────────
@analysis_bp.route("/save_analysis", methods=["POST"])
def save_analysis():
    """
    Accepts JSON payload and saves it to the analysis_results table.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required = ["algo", "items", "steps", "start_time",
                "end_time", "total_time_ms", "time_complexity"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        record = Analysis(
            algo=data["algo"],
            items=int(data["items"]),
            steps=int(data["steps"]),
            start_time=float(data["start_time"]),
            end_time=float(data["end_time"]),
            total_time_ms=float(data["total_time_ms"]),
            time_complexity=data["time_complexity"],
            path_to_graph=data.get("path_to_graph", ""),
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": "Analysis saved successfully.",
            "id": record.id,
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ── GET /retrieve_analysis ────────────────────────────────────
@analysis_bp.route("/retrieve_analysis", methods=["GET"])
def retrieve_analysis():
    """
    Retrieve a previously saved analysis by its ID.
    Example: GET /retrieve_analysis?id=1
    """
    analysis_id = request.args.get("id")
    if not analysis_id:
        return jsonify({"error": "Query parameter 'id' is required"}), 400

    record = Analysis.query.filter_by(id=int(analysis_id)).first()
    if not record:
        return jsonify({"error": f"No analysis found with id={analysis_id}"}), 404

    return jsonify({
        "id": record.id,
        "algo": record.algo,
        "items": record.items,
        "steps": record.steps,
        "start_time": record.start_time,
        "end_time": record.end_time,
        "total_time_ms": record.total_time_ms,
        "time_complexity": record.time_complexity,
        "path_to_graph": record.path_to_graph,
    }), 200
