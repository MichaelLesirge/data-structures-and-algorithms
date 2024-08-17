import importlib
from itertools import zip_longest

import pygame

from config import Config
from util import make_random
from tracking_array import TrackingArray

def load_sorting_algorithms(names: list[str]):
    return [getattr(importlib.import_module('algorithms'), algo) for algo in names]

def main(config: Config = Config()):
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption("Sorting Visualizer")
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)

    print("""
        Controls
        Speed Up: Up Arrow
        Slow Down: Down Arrow
        Skip: Space
    """)

    sorting_algorithms = load_sorting_algorithms(config.DEMO_SORTING_ALGORITHMS)
    
    for length, fps_adjuster_default in zip_longest(config.DEMO_LIST_LENGTHS, config.SPEEDS):

        if (length is None): break
        if (fps_adjuster_default is None): fps_adjuster_default = 1 if len(config.SPEEDS) < 1 else config.SPEEDS[-1]

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
                            fps_adjuster = round(max(fps_adjuster - config.FPS_CHANGE, 0), 2)
                        if event.key == pygame.K_UP:
                            fps_adjuster = round(min(fps_adjuster + config.FPS_CHANGE, 20), 2)
                        if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                            raise InterruptedError("Ended by user")
                        
                fps = int(config.BASE_FPS * fps_adjuster) if fps_adjuster else 1
                                                                
                fps_data = (""
                    # f"{fps} FPS" +
                    + ("" if fps_adjuster in (0, 1) else f" ({fps_adjuster}x speed)")
                    # + ("" if fps - clock.get_fps() < 100 else f". Real FPS {int(round(clock.get_fps(), -2))}")
                    # + "."
                )
                text = font.render(f"{sorter.__name__} - {display_array.reads} reads, {display_array.writes} writes. {fps_data}",
                                   True, config.TEXT_COLOR)
                
                screen.fill(config.BACKGROUND_COLOR)

                screen.blit(text, (0, 0))
                display_array.draw()
                screen.blit(text, (0, 0))
                
                pygame.display.flip()
                clock.tick(fps)
                            
            array = make_random(length, config.DEMO_LIST_NUM_RANGE) 

            display_array = TrackingArray(
                array, screen, update_screen,

                default_color = config.DEFAULT_BLOCK_COLOR,
                read_color = config.READ_BLOCK_COLOR,
                past_write_color = config.PAST_WRITE_BLOCK_COLOR,
                write_color = config.WRITE_BLOCK_COLOR,
                gap = config.BLOCK_GAP_PX
            )

            try:
                sorter(display_array)
            except InterruptedError:
                print(f"Skipping {sorter.__name__}")
            else:
                print(f"{sorter.__name__}:\t{display_array.reads} reads,\t{display_array.writes} writes.")
                update_screen(display_array)

            pygame.time.delay(int(config.DELAY_AFTER_COMPLETION * 1000)) 
        
        print()
        
    pygame.quit()

if __name__ == "__main__":
    main()