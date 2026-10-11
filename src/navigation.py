
import heapq
import math
import time


def astar(start, goal, cols, rows, obstacles):
    """
    Find a shortest-cost path on a grid using A*.

    Coordinates use (x, y).
    Movement supports four straight and four diagonal directions.
    Diagonal corner cutting is prevented.

    Returns:
        path: list of (x, y) cells, including start and goal
              or [] if no path exists.
        expanded: number of nodes expanded.
        elapsed: planning time in seconds.
    """
    started = time.perf_counter()
    obstacles = set(obstacles)

    def in_bounds(cell):
        x, y = cell
        return 0 <= x < cols and 0 <= y < rows

    def heuristic(a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

    if (
        cols <= 0
        or rows <= 0
        or not in_bounds(start)
        or not in_bounds(goal)
        or start in obstacles
        or goal in obstacles
    ):
        return [], 0, time.perf_counter() - started

    if start == goal:
        return [start], 0, time.perf_counter() - started

    moves = [
        (-1, 0, 1.0),
        (1, 0, 1.0),
        (0, -1, 1.0),
        (0, 1, 1.0),
        (-1, -1, math.sqrt(2)),
        (1, -1, math.sqrt(2)),
        (-1, 1, math.sqrt(2)),
        (1, 1, math.sqrt(2)),
    ]

    # Heap entries: estimated total cost, actual cost, cell.
    frontier = [(heuristic(start, goal), 0.0, start)]
    came_from = {}
    g_score = {start: 0.0}
    closed = set()
    expanded = 0

    while frontier:
        _, cost, current = heapq.heappop(frontier)

        # Ignore outdated queue entries.
        if cost > g_score.get(current, float("inf")):
            continue

        if current in closed:
            continue

        if current == goal:
            path = [goal]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()

            return path, expanded, time.perf_counter() - started

        closed.add(current)
        expanded += 1

        x, y = current

        for dx, dy, move_cost in moves:
            nxt = (x + dx, y + dy)

            if not in_bounds(nxt) or nxt in obstacles:
                continue

            # A diagonal move cannot pass through an obstacle corner.
            if dx != 0 and dy != 0:
                if (x + dx, y) in obstacles:
                    continue
                if (x, y + dy) in obstacles:
                    continue

            if nxt in closed:
                continue

            new_cost = cost + move_cost

            if new_cost < g_score.get(nxt, float("inf")):
                g_score[nxt] = new_cost
                came_from[nxt] = current

                priority = new_cost + heuristic(nxt, goal)
                heapq.heappush(
                    frontier, (priority, new_cost, nxt)
                )

    return [], expanded, time.perf_counter() - started


def calculate_path_cost(path):
    """Calculate route cost, including diagonal movements."""
    if len(path) < 2:
        return 0.0

    total = 0.0

    for a, b in zip(path, path[1:]):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])

        if max(dx, dy) != 1:
            raise ValueError("Path contains a non-adjacent move.")

        total += math.sqrt(2) if dx == 1 and dy == 1 else 1.0

    return total
