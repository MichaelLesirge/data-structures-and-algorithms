import importlib
from itertools import zip_longest

import pygame

from config import Config
from util import make_random
from tracking_array import TrackingArray

def load_sorting_algorithms():
    return [getattr(importlib.import_module('algorithms'), algo) for algo in Config.SORTING_ALGORITHMS]

def main():
    pygame.init()

    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption("Sorting Visualizer")
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(Config.FONT_PATH, Config.FONT_SIZE)

    print("""
        Controls
        Speed Up: Up Arrow
        Slow Down: Down Arrow
        Skip: Space
    """)
    
    sorting_algorithms = load_sorting_algorithms()
    
    for length, fps_adjuster_default in zip_longest(Config.DEMO_LIST_LENGTHS, Config.SPEEDS):

        if (length is None): break
        if (fps_adjuster_default is None): fps_adjuster_default = 1 if len(Config.SPEEDS) < 1 else Config.SPEEDS[-1]

        fps_adjuster_default_text = f" Default speed is {round(fps_adjuster_default, 2)}x."
        print(f"Sorting demo for {length} element array.{'' if fps_adjuster_default == 1 else fps_adjuster_default_text}")
                
        for sorter in sorting_algorithms:
            fps_adjuster = fps_adjuster_default
                                
            def update_screen(display_array: TrackingArray):
                nonlocal fps_adjuster
                                                                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            fps_adjuster = round(max(fps_adjuster - Config.FPS_CHANGE, 0), 2)
                        if event.key == pygame.K_UP:
                            fps_adjuster = round(min(fps_adjuster + Config.FPS_CHANGE, 20), 2)
                        if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                            fps_adjuster = float("inf")
                        
                if fps_adjuster == float("inf"):
                    return

                
                fps = int(Config.BASE_FPS * fps_adjuster) if fps_adjuster else 1
                                
                fps_data = (f"{fps} FPS" +
                            ("" if fps_adjuster in (0, 1) else f" ({fps_adjuster}x speed)") +
                            ("" if fps - clock.get_fps() < 100 else f". Real FPS {int(round(clock.get_fps(), -2))}") +
                            ".")
                text = font.render(f"{sorter.__name__} - {display_array.reads} reads, {display_array.writes} writes. {fps_data}",
                                   True, Config.TEXT_COLOR)
                
                screen.fill(Config.BACKGROUND_COLOR)

                display_array.draw()
                screen.blit(text, text.get_rect())
                
                pygame.display.flip()
                clock.tick(fps)
                            
            array = make_random(length, Config.DEMO_LIST_NUM_RANGE) 
            display_array = TrackingArray(
                array, screen, update_screen,
                default_color = Config.DEFAULT_BLOCK_COLOR,
                read_color = Config.READ_BLOCK_COLOR,
                past_write_color = Config.PAST_WRITE_BLOCK_COLOR,
                write_color = Config.WRITE_BLOCK_COLOR,
            )
                    
            sorter(display_array)
                            
            update_screen(display_array)
            
            print(f"{sorter.__name__}:\t{display_array.reads} reads,\t{display_array.writes} writes.")
            
            if fps_adjuster != float("inf"):
                pygame.time.delay(int(Config.WAIT_AT_END * 1000)) 
        
        print()
        
    pygame.quit()

if __name__ == "__main__":
    main()