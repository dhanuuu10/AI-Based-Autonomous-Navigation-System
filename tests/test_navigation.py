
import math

from src.navigation import astar, calculate_path_cost


def test_path_reaches_goal():
    path, expanded, elapsed = astar(
        (0, 0), (4, 4), 5, 5, set()
    )

    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
    assert expanded >= 0
    assert elapsed >= 0


def test_diagonal_path_cost():
    path, _, _ = astar(
        (0, 0), (3, 3), 5, 5, set()
    )

    assert math.isclose(
        calculate_path_cost(path), 3 * math.sqrt(2)
    )


def test_path_avoids_obstacles():
    obstacles = {(2, 0), (2, 1), (2, 2), (2, 3)}

    path, _, _ = astar(
        (0, 0), (4, 0), 5, 5, obstacles
    )

    assert path
    assert all(cell not in obstacles for cell in path)
    assert path[0] == (0, 0)
    assert path[-1] == (4, 0)


def test_unreachable_goal():
    # Every neighboring cell around the start is blocked.
    obstacles = {(0, 1), (1, 0), (1, 1)}

    path, _, _ = astar(
        (0, 0), (3, 3), 4, 4, obstacles
    )

    assert path == []


def test_blocked_goal():
    path, _, _ = astar(
        (0, 0), (2, 2), 5, 5, {(2, 2)}
    )

    assert path == []


def test_start_equals_goal():
    path, _, _ = astar(
        (2, 2), (2, 2), 5, 5, set()
    )

    assert path == [(2, 2)]


def test_invalid_start():
    path, _, _ = astar(
        (-1, 0), (2, 2), 5, 5, set()
    )

    assert path == []


def test_path_contains_adjacent_cells():
    path, _, _ = astar(
        (0, 0), (5, 4), 6, 5, {(2, 1), (3, 2)}
    )

    assert path

    for a, b in zip(path, path[1:]):
        assert max(
            abs(a[0] - b[0]),
            abs(a[1] - b[1]),
        ) == 1


def test_diagonal_corner_cutting_is_prevented():
    obstacles = {(1, 0), (0, 1)}

    path, _, _ = astar(
        (0, 0), (1, 1), 2, 2, obstacles
    )

    assert path == []
