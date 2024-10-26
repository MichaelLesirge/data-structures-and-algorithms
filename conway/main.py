import pygame
import numpy as np
from config import Config

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, default_value, color, handle_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value
        self.color = color
        self.handle_color = handle_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        handle_pos = self.rect.left + (self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width
        pygame.draw.circle(screen, self.handle_color, (int(handle_pos), self.rect.centery), self.rect.height // 2)

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.value = (pos[0] - self.rect.left) / self.rect.width * (self.max_value - self.min_value) + self.min_value
            self.value = max(self.min_value, min(self.max_value, self.value))

def main(config: Config = Config()):
    pygame.init()
    Config.init_fonts()

    print("""
        Drag to draw alive cells
        Ctrl+Drag to draw dead cells
          
        Hit Space To Start/Pause
          
        R to randomly generate alive cells
        C to clear screen
          """)

    SCREEN_WIDTH = config.GRID_WIDTH * config.CELL_SIZE
    SCREEN_HEIGHT = config.GRID_HEIGHT * config.CELL_SIZE + config.BUTTON_HEIGHT + 20
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    clock = pygame.time.Clock()

    grid = np.zeros((config.GRID_HEIGHT, config.GRID_WIDTH), dtype=int)

    running = True
    paused = True
    update_count = 0
    drawing = False
    erasing = False
    last_update_time = pygame.time.get_ticks()
    last_draw_pos = None

    toggle_button = Button(10, SCREEN_HEIGHT - config.BUTTON_HEIGHT - 10, config.BUTTON_WIDTH, config.BUTTON_HEIGHT, "Start", config.BUTTON_COLOR, config.BUTTON_HOVER_COLOR, config.BUTTON_TEXT_COLOR, Config.FONT)
    speed_slider = Slider(120, SCREEN_HEIGHT - config.SLIDER_HEIGHT - 10, config.SLIDER_WIDTH, config.SLIDER_HEIGHT, config.FPS_MIN, config.FPS_MAX, config.FPS_DEFAULT, config.SLIDER_COLOR, config.SLIDER_HANDLE_COLOR)

    def toggle_cell(pos):
        col, row = pos[0] // config.CELL_SIZE, pos[1] // config.CELL_SIZE
        if 0 <= row < config.GRID_HEIGHT and 0 <= col < config.GRID_WIDTH:
            if drawing:
                grid[row, col] = 1
            if erasing:
                grid[row, col] = 0

    def draw_line(start, end):
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            toggle_cell((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    while running:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        toggle_button.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    toggle_button.text = "Pause" if not paused else "Start"
                elif event.key == pygame.K_r:
                    grid = np.random.choice([0, 1], size=(config.GRID_HEIGHT, config.GRID_WIDTH), p=[0.9, 0.1])
                    update_count = 0
                elif event.key == pygame.K_c:
                    grid.fill(0)
                    update_count = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if toggle_button.is_clicked(mouse_pos):
                        paused = not paused
                        toggle_button.text = "Pause" if not paused else "Start"
                    elif speed_slider.rect.collidepoint(mouse_pos):
                        speed_slider.update(mouse_pos)
                    else:
                        drawing = True
                        last_draw_pos = mouse_pos
                        toggle_cell(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    erasing = False
                last_draw_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if drawing or erasing:
                    if last_draw_pos:
                        draw_line(last_draw_pos, mouse_pos)
                    last_draw_pos = mouse_pos
                if speed_slider.rect.collidepoint(mouse_pos) and event.buttons[0]:
                    speed_slider.update(mouse_pos)

        keyboard = pygame.key.get_pressed()
        erasing = drawing and (keyboard[pygame.K_e] or keyboard[pygame.K_LCTRL] or keyboard[pygame.K_RCTRL])

        update_interval = 1000 / speed_slider.value  # Convert FPS to milliseconds
        if not paused and current_time - last_update_time >= update_interval:
            grid = update_grid(grid, config)
            update_count += 1
            last_update_time = current_time

        draw_grid(screen, grid, config)
        toggle_button.draw(screen)
        speed_slider.draw(screen)

        # Draw timer
        timer_text = Config.TIMER_FONT.render(f"Updates: {update_count}", True, config.TIMER_COLOR)
        screen.blit(timer_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)  # Keep the game loop running at 60 FPS

    pygame.quit()

def update_grid(grid, config):
    new_grid = grid.copy()
    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            neighbors = count_neighbors(grid, row, col)
            if grid[row, col] == 1:
                if neighbors not in config.SURVIVE:
                    new_grid[row, col] = 0
            else:
                if neighbors in config.BORN:
                    new_grid[row, col] = 1
    return new_grid

def count_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = (row + i) % len(grid), (col + j) % len(grid[0])
            count += grid[r, c]
    return count

def draw_grid(screen, grid, config):
    screen.fill(config.BACKGROUND)
    for row in range(config.GRID_HEIGHT):
        for col in range(config.GRID_WIDTH):
            color = config.CELL_ALIVE if grid[row, col] else config.CELL_DEAD
            pygame.draw.rect(screen, color, (col * config.CELL_SIZE, row * config.CELL_SIZE, config.CELL_SIZE - 1, config.CELL_SIZE - 1))

if __name__ == "__main__":
    main()