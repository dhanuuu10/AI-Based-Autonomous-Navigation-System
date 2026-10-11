
from src.navigation import astar, calculate_path_cost


def test_open_map_finds_direct_diagonal_route():
    path, expanded, elapsed = astar(
        (0, 0), (5, 5), 6, 6, set()
    )

    assert path
    assert path[0] == (0, 0)
    assert path[-1] == (5, 5)
    assert len(path) == 6
    assert expanded >= 0
    assert elapsed >= 0


def test_wall_with_gap_is_navigable():
    # A wall blocks the middle column except for one opening.
    obstacles = {
        (2, 0), (2, 1), (2, 2),
        (2, 4), (2, 5),
    }

    path, _, _ = astar(
        (0, 0), (4, 0), 5, 6, obstacles
    )

    assert path
    assert path[0] == (0, 0)
    assert path[-1] == (4, 0)
    assert all(cell not in obstacles for cell in path)


def test_completely_blocked_map_has_no_route():
    # A vertical barrier separates the left and right sides.
    obstacles = {
        (2, 0), (2, 1), (2, 2),
        (2, 3), (2, 4),
    }

    path, _, _ = astar(
        (0, 2), (4, 2), 5, 5, obstacles
    )

    assert path == []


def test_longer_route_avoids_a_barrier():
    obstacles = {
        (2, 0), (2, 1), (2, 2), (2, 3)
    }

    path, _, _ = astar(
        (0, 0), (4, 0), 5, 5, obstacles
    )

    assert path
    assert all(cell not in obstacles for cell in path)
    assert calculate_path_cost(path) > 4


def test_planner_handles_a_single_cell_map():
    path, expanded, elapsed = astar(
        (0, 0), (0, 0), 1, 1, set()
    )

    assert path == [(0, 0)]
    assert expanded == 0
    assert elapsed >= 0


def test_invalid_dimensions_return_no_path():
    path, _, _ = astar(
        (0, 0), (1, 1), 0, 5, set()
    )

    assert path == []
