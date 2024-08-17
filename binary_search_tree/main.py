from typing import Iterator, Self

import pygame
from pygame import Vector2, Color
import colorsys

import time

from config import Config

pygame.init()

WIDTH, HEIGHT = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Node class
class Node:

    NODE_RADIUS = 25
    SPRINGINESS = 0.1
    DAMPING = 0.85
    CHILD_MOVE_FACTOR = 0.2

    def __init__(self, value: int, x: int, y: int) -> None:
        self.value = value
        self.position = Vector2(x, y)
        self.target = Vector2(x, y)
        self.velocity = Vector2(0, 0)

        self.left: Node | None = None
        self.right: Node | None = None

        self.update_color_bounds(value, value)

        self.font = pygame.font.SysFont(None, 24)

    def update_position(self) -> None:
        force = (self.target - self.position) * self.SPRINGINESS

        self.velocity += force

        self.velocity *= self.DAMPING

        self.position += self.velocity

    def move_children(self, offset: Vector2) -> None:
        if self.left:
            self.left.target += offset * self.CHILD_MOVE_FACTOR
            self.left.move_children(offset)
        if self.right:
            self.right.target += offset * self.CHILD_MOVE_FACTOR
            self.right.move_children(offset)

    def draw(self, screen: pygame.Surface) -> None:
        color = self.get_color()

        luminance = (0.2126 * color[0]) + (0.7152 * color[1]) + (0.0722 * color[2])

        text_color = WHITE if luminance < 128 else BLACK

        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), self.NODE_RADIUS)

        img = self.font.render(str(self.value), True, text_color)
        img_rect = img.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(img, img_rect)

    def get_color(self) -> None:
        if self.max_value == self.min_value:
            normalized_value = 0.5
        else:
            normalized_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        
        hue = 0.7 - 0.7 * normalized_value
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

        return tuple(int(255 * c) for c in rgb)

    def update_color_bounds(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
    
    def __iter__(self) -> Iterator[Self]:
        if self.left: yield from self.left
        yield self
        if self.right: yield from self.right
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, left={self.left}, right={self.right})"

class BinarySearchTree:
    LEVEL_SPACING = 0.2

    def __init__(self, values: list[int] = None) -> None:
        self.root: Node | None = None  

        for value in (values or []):
            self.insert(value, with_bounce=False)  

    def insert(self, value: int, with_bounce: bool = True) -> None:

        new_node = Node(value, WIDTH // 2, HEIGHT - 50)
        self.root = self._insert_recursively(self.root, new_node)
        
        self._update_node_positions(self.root, Vector2(WIDTH // 2, 50), WIDTH // 4, with_bounce = with_bounce)

        for node in self._in_order():
            node.update_color_bounds(self.first() or 0, self.last() or 0)
    
    def clear(self) -> None:
        self.root = None

    def first(self) -> int:
        node = self._first(self.root)
        return node.value if node else None

    def _first(self, root: Node) -> Node:
        if root is None or root.left is None:
            return root
        return self._first(root.left)

    def last(self) -> int:
        node = self._last(self.root)
        return node.value if node else None

    def _last(self, root: Node) -> Node:
        if root is None or root.right is None:
            return root
        return self._last(root.right)

    def _insert_recursively(self, current: Node | None, new_node: Node) -> Node:
        if current is None:
            return new_node
        
        if new_node.value < current.value:
            current.left = self._insert_recursively(current.left, new_node)
        else:
            current.right = self._insert_recursively(current.right, new_node)
        
        return current

    def _update_node_positions(self, node: Node, position: Vector2, offset: Vector2, with_bounce: bool = True) -> None:
        if node is not None:
            node.target = position
            if not with_bounce:
                node.position = node.target
            if node.left:
                self._update_node_positions(node.left, position - Vector2(offset, -self.LEVEL_SPACING), offset // 2)
            if node.right:
                self._update_node_positions(node.right, position + Vector2(offset, self.LEVEL_SPACING), offset // 2)

    def draw(self, screen: pygame.Surface) -> None:
        for node in self._in_order():
            node.update_position()
        for node in self._in_order():
            if node.left:
                pygame.draw.line(screen, WHITE, (node.position.x, node.position.y), (node.left.position.x, node.left.position.y), 2)
            if node.right:
                pygame.draw.line(screen, WHITE, (node.position.x, node.position.y), (node.right.position.x, node.right.position.y), 2)
        for node in self._in_order():
            node.draw(screen)
    
    def _in_order(self) -> Iterator[Node]:
        if self.root is None:
            return
        yield from self.root

# Main loop
def main(config: Config = Config()):

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Binary Search Tree Visualizer")

    clock = pygame.time.Clock()

    Node.NODE_RADIUS = Config.NODE_RADIUS
    Node.SPRINGINESS = Config.SPRINGINESS
    Node.DAMPING = Config.DAMPING
    Node.CHILD_MOVE_FACTOR = Config.CHILD_MOVE_FACTOR
    
    BinarySearchTree.LEVEL_SPACING = Config.LEVEL_SPACING

    print("""
        Type a number to add node
          
        Press C to clear tree
          """)

    tree = BinarySearchTree(config.STARTING_NODES)
    input_value = ''
    selected_node = None
    running = True

    font = pygame.font.SysFont(None, 48)

    hide_instructions_at = time.time() + 3
    show_instructions = True
    
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if a node is clicked
                    for node in tree._in_order():
                        if node.position.distance_to(event.pos) < node.NODE_RADIUS:
                            selected_node = node
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected_node = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_node:
                    offset = Vector2(event.pos) - selected_node.target
                    selected_node.target = Vector2(event.pos)
                    selected_node.move_children(offset)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    tree.clear()
                if event.key == pygame.K_RETURN and input_value:
                    if input_value == "-":  # Prevent adding just a "-"
                        input_value = ''
                    else:
                        tree.insert(int(input_value))
                        input_value = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_value = input_value[:-1]
                elif event.unicode.isdigit() or (event.unicode == "-" and len(input_value) == 0):
                    input_value += event.unicode

        if show_instructions:
            if input_value or time.time() > hide_instructions_at:
                show_instructions = False
            text = font.render("Enter a number: ___", True, WHITE)
        else:
            text = font.render(input_value, True, WHITE)

        tree.draw(screen)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
