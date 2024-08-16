from typing import Generator
import numpy as np
import pygame
from pygame import Color, Vector2
import random

pygame.init()

GRID_WIDTH = 80 + 1
GRID_HEIGHT = int(GRID_WIDTH / 1.618) + 1

CORRIDOR_WIDTH = 5

GRID_SQUARE_PX_WIDTH = 10
GRID_SQUARE_PX_HEIGHT = 10

SCREEN_PX_WIDTH = GRID_WIDTH * GRID_SQUARE_PX_WIDTH
SCREEN_PX_HEIGHT = GRID_HEIGHT * GRID_SQUARE_PX_HEIGHT

WALL = "black"
EMPTY = "white"

START = "aquamarine4"
END = "brown1"

def main():
    screen = pygame.display.set_mode((SCREEN_PX_WIDTH, SCREEN_PX_HEIGHT))
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Maze Generator")

    clock = pygame.time.Clock()

    grid = np.empty((GRID_HEIGHT, GRID_WIDTH), dtype=Color)
    
    # offsets = create_offset_array(DRAWING_PAINT_BRUSH_SIZE)
    
    easer = pygame.Surface((10,10))
    easer.fill("grey")
    pygame.draw.rect(easer, "black", easer.get_rect(), width=1)
    easer_cursor = pygame.cursors.Cursor(easer.get_rect().center, easer)

    draw_cursor = pygame.SYSTEM_CURSOR_CROSSHAIR

    generate_maze(grid, CORRIDOR_WIDTH)

    running = True
    last_mouse_position = None

    start_position = None
    end_position = None

    while running:

        do_cursor_reset = True

        mouse_position = pygame.mouse.get_pos()
        mouse_grid_position = (mouse_position[0] // GRID_SQUARE_PX_WIDTH, mouse_position[1] // GRID_SQUARE_PX_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a:
                    generate_maze(grid, CORRIDOR_WIDTH)

                if event.key == pygame.K_r:
                    grid.fill(EMPTY)

                if event.key == pygame.K_SPACE:
                    if start_position is None:
                        start_position = (mouse_grid_position[1], mouse_grid_position[0])
                        grid[start_position] = START 
                    else:
                        if end_position is not None:
                            grid[end_position] = EMPTY
                        end_position = (mouse_grid_position[1], mouse_grid_position[0])
                        grid[end_position] = END
                    
                    print(f"Finding path from {start_position} to {end_position}")

                    # solve_maze_and_draw_path(screen, grid, start_position, end_position)

                    do_cursor_reset = False
                    pygame.mouse.set_cursor(draw_cursor)

        mouse_buttons = pygame.mouse.get_pressed(3)

        keyboard = pygame.key.get_pressed()

        if mouse_buttons[0] and screen_rect.contains(mouse_position, (1, 1)):
            erase_mode = keyboard[pygame.K_e]
            
            do_cursor_reset = False
            pygame.mouse.set_cursor(easer_cursor if erase_mode else draw_cursor)

            for grid_position in get_line_points(grid, mouse_grid_position, last_mouse_position or mouse_grid_position):
                grid[grid_position] = EMPTY if erase_mode else WALL

            last_mouse_position = mouse_grid_position
        else:
            last_mouse_position = None

        if start_position and grid[start_position] != START:
            start_position = None
        if end_position and grid[end_position] != END:
            end_position = None
        
        if do_cursor_reset:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
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

def generate_maze(grid, corridor_width=1):
    wall, empty = EMPTY, WALL

    directions = [(0, corridor_width), (corridor_width, 0), (0, -corridor_width), (-corridor_width, 0)]

    def carve_passage_from(x, y):
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny, nx] == wall:
                # Carve the corridor
                for i in range(corridor_width):
                    grid[y + i * dy // corridor_width, x + i * dx // corridor_width] = empty
                grid[ny, nx] = empty
                carve_passage_from(nx, ny)

    grid.fill(wall)

    start_x = random.randrange(0, GRID_WIDTH, corridor_width)
    start_y = random.randrange(0, GRID_HEIGHT, corridor_width)
    grid[start_y, start_x] = empty

    carve_passage_from(start_x, start_y)

def create_offset_array(side_padding: int) -> np.ndarray:
    size = 3 ** side_padding
    offset_range = np.arange(-(size // 2), (size // 2) + 1)
    x_offsets, y_offsets = np.meshgrid(offset_range, offset_range)
    offsets = np.stack((x_offsets.ravel(), y_offsets.ravel()), axis=-1)
    
    return offsets

if __name__ == "__main__":
    main()
