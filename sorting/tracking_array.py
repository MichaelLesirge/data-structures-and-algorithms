from typing import Callable, Self

import pygame

def to_rgba(color: pygame.Color): return (color.r, color.g, color.b, color.a)

class TrackingArray(list):
    def __init__(
            self,
            array: list[int],
            screen: pygame.Surface,
            update_func: Callable[[Self], None],

            gap = 0,

            default_color = pygame.Color(255, 255, 255),            
            read_color = pygame.Color("grey"),
            past_write_color = pygame.Color("aquamarine2"),
            write_color = pygame.Color("green"),
        ):
        super().__init__(array)

        self.screen = screen
        self.update_func = update_func

        self.default_color = to_rgba(default_color)
        self.read_color = to_rgba(read_color or default_color)
        self.past_write_color = to_rgba(past_write_color or default_color)
        self.write_color = to_rgba(write_color or default_color)

        self.margin = gap
        
        self.reads = 0
        self.writes = 0

        self.max = max(self)
        
        self.marks = {}
    
    def get_rect(self, index, value):
        width = self.screen.get_width() / len(self)
        height = self.screen.get_height()
        return pygame.Rect(
            (width * index), height - (height / self.max) * value,
            width - self.margin, height
        )
    
    def draw(self) -> None:
        highlighted_indexes = {value: key for key, value in self.marks.items()}
        for index, value in enumerate(self):
            color = highlighted_indexes.get(index, self.default_color)
            pygame.draw.rect(self.screen, color, self.get_rect(index, value))
        
        pygame.display.flip()
    
    def __getitem__(self, index):
        self.reads += 1
        self.marks[self.read_color] = index
        self.update_func(self)
        return super().__getitem__(index)

    def __setitem__(self, index, value): 
        if isinstance(index, slice):
            for i, slice_i in enumerate(range(index.start or 0, index.stop or len(self), index.step or 1)):
                self[slice_i] = value[i]
        else:
            self.writes += 1

            self.marks[self.past_write_color] = self.marks.get(self.write_color, self.default_color)
            self.marks[self.write_color] = index

            self.update_func(self)
            return super().__setitem__(index, value)
    
    def __str__(self) -> str:
        return f"<{super().__str__()}, reads={self.reads}, writes={self.writes}>"