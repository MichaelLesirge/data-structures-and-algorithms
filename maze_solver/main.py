from typing import Generator
import random
import heapq

import numpy as np
import pygame

from config import Config

Color = pygame.Color

pygame.init()

def main(config: Config = Config()):

    DESIRED_GRID_WIDTH = 80
    DESIRED_GRID_HEIGHT = int(DESIRED_GRID_WIDTH / 1.618)

    GRID_WIDTH = int(DESIRED_GRID_WIDTH // config.CORRIDOR_WIDTH * config.CORRIDOR_WIDTH) + 1
    GRID_HEIGHT = int(DESIRED_GRID_HEIGHT // config.CORRIDOR_WIDTH * config.CORRIDOR_WIDTH) + 1

    GRID_SQUARE_PX_WIDTH = 10
    GRID_SQUARE_PX_HEIGHT = 10

    SCREEN_PX_WIDTH = GRID_WIDTH * GRID_SQUARE_PX_WIDTH
    SCREEN_PX_HEIGHT = GRID_HEIGHT * GRID_SQUARE_PX_HEIGHT

    print("""
        Drag to draw walls
        Ctrl+Drag to draw walls
          
        Hit Space To Create Start/End
        Use arrows to move end
          
        R to Randomly Generate new Maze
        C to Clear Screen
        F to Fill Screen
          """)

    screen = pygame.display.set_mode((SCREEN_PX_WIDTH, SCREEN_PX_HEIGHT))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Maze Generator and Solver")

    clock = pygame.time.Clock()

    grid = np.empty((GRID_HEIGHT, GRID_WIDTH), dtype=Color)
    
    easer = pygame.Surface((10,10))
    easer.fill("grey")
    pygame.draw.rect(easer, "black", easer.get_rect(), width=1)
    easer_cursor = pygame.cursors.Cursor(easer.get_rect().center, easer)

    draw_cursor = pygame.SYSTEM_CURSOR_CROSSHAIR

    generate_maze(grid, config.CORRIDOR_WIDTH, wall=config.WALL, empty=config.EMPTY)

    running = True
    last_mouse_position = None

    start_position = None
    end_position = None

    while running:
        mouse_position = pygame.mouse.get_pos()
        mouse_grid_position = (mouse_position[0] // GRID_SQUARE_PX_WIDTH, mouse_position[1] // GRID_SQUARE_PX_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    generate_maze(grid, config.CORRIDOR_WIDTH, wall=config.WALL, empty=config.EMPTY)
                    start_position = None
                    end_position = None
                if event.key == pygame.K_c:
                    grid.fill(config.EMPTY)
                    start_position = None
                    end_position = None
                if event.key == pygame.K_f:
                    grid.fill(config.WALL)
                    start_position = None
                    end_position = None
                if event.key == pygame.K_SPACE:
                    if start_position is None:
                        start_position = (mouse_grid_position[1], mouse_grid_position[0])
                        grid[start_position] = config.START 
                    else:
                        if end_position is not None:
                            grid[end_position] = config.EMPTY
                        end_position = (mouse_grid_position[1], mouse_grid_position[0])
                    
                    pygame.mouse.set_cursor(draw_cursor)
                if (event.key == pygame.K_UP):
                    if end_position is None:
                        end_position = start_position
                    if end_position is not None:
                        grid[end_position] = config.EMPTY
                        end_position = (end_position[0] - 1, end_position[1])
                if (event.key == pygame.K_DOWN):
                    if end_position is None:
                        end_position = start_position
                    if end_position is not None:
                        grid[end_position] = config.EMPTY
                        end_position = (end_position[0] + 1, end_position[1])
                if (event.key == pygame.K_LEFT):
                    if end_position is None:
                        end_position = start_position
                    if end_position is not None:
                        grid[end_position] = config.EMPTY
                        end_position = (end_position[0], end_position[1] - 1)
                if (event.key == pygame.K_RIGHT):
                    if end_position is None:
                        end_position = start_position
                    if end_position is not None:
                        grid[end_position] = config.EMPTY
                        end_position = (end_position[0], end_position[1] + 1)

        if end_position:
            grid[end_position] = config.END
        if start_position:
            grid[start_position] = config.START

        mouse_buttons = pygame.mouse.get_pressed(3)
        keyboard = pygame.key.get_pressed()

        erase_mode = keyboard[pygame.K_e] or keyboard[pygame.K_LCTRL] or keyboard[pygame.K_RCTRL]
        
        pygame.mouse.set_cursor(easer_cursor if erase_mode else draw_cursor)

        if mouse_buttons[0] and screen_rect.contains(mouse_position, (1, 1)):
            for grid_position in get_line_points(grid, mouse_grid_position, last_mouse_position or mouse_grid_position):
                grid[grid_position] = config.EMPTY if erase_mode else config.WALL

            last_mouse_position = mouse_grid_position
        else:
            last_mouse_position = None

        if start_position and grid[start_position] != config.START:
            start_position = None
        if end_position and grid[end_position] != config.END:
            end_position = None
        
        replace(grid, config.PATH, config.EMPTY)
        if start_position and end_position:
            solve_maze_and_draw_path(grid, start_position, end_position, config=config)
            
        screen.fill("white")
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                pygame.draw.rect(screen, grid[x, y], (y * GRID_SQUARE_PX_WIDTH, x * GRID_SQUARE_PX_HEIGHT, GRID_SQUARE_PX_WIDTH, GRID_SQUARE_PX_HEIGHT))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def get_line_points(grid, pos1, pos2) -> Generator[tuple[int, int], None, None]:
    x0, y0 = pos1
    x1, y1 = pos2

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= y0 < len(grid) and 0 <= x0 < len(grid[0]):
            yield y0, x0

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def generate_maze(grid, corridor_width=1, wall=1, empty=0):
    grid.fill(wall)
    
    directions = [(0, corridor_width), (0, -corridor_width), (corridor_width, 0), (-corridor_width, 0)]

    def get_neighbor(pos, direction):
        return pos[0] + direction[0], pos[1] + direction[1]
    
    def path_tile(x, y, value):
        for dx in range(corridor_width - 1):
            for dy in range(corridor_width - 1):
                grid[x + dx, y + dy] = value
    
    def recursive_backtracking(x, y):
        directions_copy = directions[:]
        random.shuffle(directions_copy)

        for direction in directions_copy:
            nx, ny = get_neighbor((x, y), direction)
            
            if 1 <= nx < len(grid) - 1 and 1 <= ny < len(grid[0]) - 1 and grid[nx, ny] == wall:
                path_tile(x + direction[0] // 2, y + direction[1] // 2, empty)
                path_tile(nx, ny, empty)
                recursive_backtracking(nx, ny)
    
    start_x = random.randrange(1, len(grid) - 1, corridor_width)
    start_y = random.randrange(1, len(grid[0]) - 1, corridor_width)
    
    path_tile(start_x, start_y, empty)
    recursive_backtracking(start_x, start_y)


def replace(grid, old, new):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x, y] == old:
                grid[x, y] = new

def solve_maze_and_draw_path(grid, start, end, config):
    # TODO this method does to much...
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def get_neighbors(pos):
        result = []
        for direction in config.SOLVER_DIRECTIONS:
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor] != config.WALL:
                result.append(neighbor)
        return result

    def a_star(start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        if goal not in came_from:
            return None

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    path = a_star(start, end)
    if path:
        for pos in path:
            if grid[pos] not in [config.START, config.END]:
                grid[pos] = config.PATH

if __name__ == "__main__":
    main()