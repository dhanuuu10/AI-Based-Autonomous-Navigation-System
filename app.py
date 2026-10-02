
from flask import Flask, render_template, request, jsonify
from src.navigation import astar, calculate_path_cost

app = Flask(__name__)

COLS = 20
ROWS = 14

START = (1, 1)
DEFAULT_GOAL = (18, 12)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/plan", methods=["POST"])
def plan_route():
    data = request.get_json(silent=True) or {}

    try:
        start = tuple(data.get("start", START))
        goal = tuple(data.get("goal", DEFAULT_GOAL))
        obstacles = {
            tuple(cell) for cell in data.get("obstacles", [])
        }

        if len(start) != 2 or len(goal) != 2:
            return jsonify({"error": "Invalid coordinates."}), 400

        if not all(isinstance(v, int) for v in (*start, *goal)):
            return jsonify({"error": "Coordinates must be integers."}), 400

        def in_bounds(cell):
            x, y = cell
            return 0 <= x < COLS and 0 <= y < ROWS

        if not in_bounds(start) or not in_bounds(goal):
            return jsonify({"error": "Start or goal is outside the grid."}), 400

        if any(not in_bounds(cell) for cell in obstacles):
            return jsonify({"error": "An obstacle is outside the grid."}), 400

        if start in obstacles or goal in obstacles:
            return jsonify({
                "error": "The start and goal cannot be obstacles."
            }), 400

        path, expanded, elapsed = astar(
            start, goal, COLS, ROWS, obstacles
        )

        path_cost = calculate_path_cost(path) if path else None

        return jsonify({
            "path": [list(cell) for cell in path],
            "path_cost": path_cost,
            "steps": max(0, len(path) - 1) if path else 0,
            "expanded_nodes": expanded,
            "planning_ms": round(elapsed * 1000, 3),
            "reachable": bool(path),
            "start": list(start),
            "goal": list(goal),
            "obstacles": [list(cell) for cell in sorted(obstacles)],
        })

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid navigation data."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
