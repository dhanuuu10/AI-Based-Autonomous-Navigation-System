
import pygame

from src.navigation import astar, calculate_path_cost

# ---------------- Configuration ----------------
CELL_SIZE = 30
COLS, ROWS = 24, 18
WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
PANEL_HEIGHT = 100
HEIGHT = GRID_HEIGHT + PANEL_HEIGHT
FPS = 60

START = (1, 1)
INITIAL_GOAL = (22, 16)

WHITE = (245, 247, 250)
BLACK = (30, 35, 45)
GRID = (215, 220, 228)
OBSTACLE = (65, 75, 90)
GREEN = (40, 170, 100)
RED = (220, 65, 65)
BLUE = (45, 115, 230)
GREY = (100, 110, 125)
PATH_COLOR = (190, 220, 255)
ORANGE = (240, 145, 45)

# Reproducible default obstacle layout.
def create_default_obstacles():
    obstacles = set()

    for x in range(4, 19):
        if x not in (9, 10):
            obstacles.add((x, 5))

    for y in range(5, 15):
        if y not in (10, 11):
            obstacles.add((14, y))

    for x in range(3, 12):
        if x not in (6, 7):
            obstacles.add((x, 12))

    return obstacles


def draw_cell(screen, cell, color):
    x, y = cell
    rect = pygame.Rect(
        x * CELL_SIZE + 1,
        y * CELL_SIZE + 1,
        CELL_SIZE - 2,
        CELL_SIZE - 2,
    )
    pygame.draw.rect(screen, color, rect, border_radius=4)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(
        "AI-Based Autonomous Navigation System"
    )

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 15)

    obstacles = create_default_obstacles()
    goal = INITIAL_GOAL

    path = []
    expanded = 0
    planning_time = 0.0
    path_cost = 0.0

    robot_index = 0.0
    paused = False
    finished = False
    running = True
    status = "READY"

    def replan():
        nonlocal path, expanded, planning_time
        nonlocal path_cost, robot_index, finished, status

        path, expanded, planning_time = astar(
            START, goal, COLS, ROWS, obstacles
        )

        path_cost = calculate_path_cost(path)
        robot_index = 0.0
        finished = False

        if path:
            status = "NAVIGATING"
        else:
            status = "NO PATH FOUND"

    def mouse_to_cell(position):
        mx, my = position

        if not (0 <= mx < WIDTH and 0 <= my < GRID_HEIGHT):
            return None

        return mx // CELL_SIZE, my // CELL_SIZE

    replan()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    if path and not finished:
                        paused = not paused
                        status = (
                            "PAUSED" if paused else "NAVIGATING"
                        )

                elif event.key == pygame.K_r:
                    paused = False
                    replan()

                elif event.key == pygame.K_m:
                    obstacles = create_default_obstacles()
                    goal = INITIAL_GOAL
                    paused = False
                    replan()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = mouse_to_cell(event.pos)

                if cell is None or cell == START:
                    continue

                if event.button == 1:
                    # Left-click: select a new destination.
                    goal = cell
                    obstacles.discard(goal)
                    paused = False
                    replan()

                elif event.button == 3:
                    # Right-click: add or remove an obstacle.
                    if cell == goal:
                        continue

                    if cell in obstacles:
                        obstacles.remove(cell)
                    else:
                        obstacles.add(cell)

                    # Replan from the start after every map edit.
                    paused = False
                    replan()

        # Smoothly animate the robot along the route.
        if path and not paused and not finished:
            robot_index += 0.08

            if robot_index >= len(path) - 1:
                robot_index = float(len(path) - 1)
                finished = True
                status = "GOAL REACHED"

        screen.fill(WHITE)

        # Draw grid lines.
        for x in range(COLS + 1):
            pygame.draw.line(
                screen,
                GRID,
                (x * CELL_SIZE, 0),
                (x * CELL_SIZE, GRID_HEIGHT),
            )

        for y in range(ROWS + 1):
            pygame.draw.line(
                screen,
                GRID,
                (0, y * CELL_SIZE),
                (WIDTH, y * CELL_SIZE),
            )

        # Draw obstacles and planned route.
        for obstacle in obstacles:
            draw_cell(screen, obstacle, OBSTACLE)

        for cell in path:
            draw_cell(screen, cell, PATH_COLOR)

        # Start and goal markers.
        draw_cell(screen, START, GREEN)
        draw_cell(screen, goal, RED)

        # Draw the moving robot.
        if path:
            index = min(
                int(robot_index), len(path) - 1
            )

            current = path[index]

            if index < len(path) - 1:
                nxt = path[index + 1]
                fraction = robot_index - index

                rx = current[0] + (
                    nxt[0] - current[0]
                ) * fraction

                ry = current[1] + (
                    nxt[1] - current[1]
                ) * fraction
            else:
                rx, ry = current

            center = (
                int(rx * CELL_SIZE + CELL_SIZE / 2),
                int(ry * CELL_SIZE + CELL_SIZE / 2),
            )

            pygame.draw.circle(
                screen, BLUE, center, CELL_SIZE // 3
            )

        # Status and metrics panel.
        pygame.draw.rect(
            screen,
            WHITE,
            (0, GRID_HEIGHT, WIDTH, PANEL_HEIGHT),
        )

        steps = len(path) - 1 if path else 0

        line1 = (
            f"{status} | Steps: {steps} | "
            f"Cost: {path_cost:.2f}"
        )

        line2 = (
            f"Expanded: {expanded} | "
            f"Plan: {planning_time * 1000:.2f} ms | "
            f"Obstacles: {len(obstacles)}"
        )

        line3 = (
            "LEFT CLICK: Goal | RIGHT CLICK: Obstacle"
        )

        line4 = (
            "SPACE: Pause | R: Replan | "
            "M: Reset map | ESC: Exit"
        )

        for i, line in enumerate(
            (line1, line2, line3, line4)
        ):
            color = BLACK if i < 2 else GREY
            screen.blit(
                font.render(line, True, color),
                (8, GRID_HEIGHT + 5 + i * 22),
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
