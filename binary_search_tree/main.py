from typing import Iterator, Self

import pygame
from pygame import Vector2, Color
import colorsys

import time

from config import Config

pygame.init()

WIDTH, HEIGHT = 800, 600

COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

# Node class
class Node:

    NODE_RADIUS = 25
    SPRINGINESS = 0.7
    DAMPING = 0.75
    CHILD_MOVE_FACTOR = 0.5

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

        text_color = "white" if luminance < 128 else "black"

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
        self.flying_nodes: list[Node] = []

        for value in (values or []):
            self.insert(value, with_bounce=False)

    def insert(self, value: int, with_bounce: bool = True) -> None:

        new_node = Node(value, WIDTH // 2, HEIGHT - 50)
        self.root = self._insert_recursively(self.root, new_node)
        
        self._update_node_positions(self.root, Vector2(WIDTH // 2, 50), WIDTH // 4, with_bounce = with_bounce)

        for node in self._in_order():
            node.update_color_bounds(self.first() or 0, self.last() or 0)
    
    def clear(self) -> None:
        if self.root:
            self.flying_nodes = list(self._in_order())
            for node in self.flying_nodes:
                node.velocity = Vector2((node.position.x - (WIDTH / 2)) * 0.1, -30).clamp_magnitude(30)
        self.root = None


    def balance(self) -> None:
        nodes = list(self._in_order())
        self.root = self._build_balanced_tree(nodes)
        self._update_node_positions(self.root, Vector2(WIDTH // 2, 50), WIDTH // 4)

    def _build_balanced_tree(self, nodes: list[Node]) -> Node | None:
        if not nodes:
            return None
        mid = len(nodes) // 2
        root = nodes[mid]
        root.left = self._build_balanced_tree(nodes[:mid])
        root.right = self._build_balanced_tree(nodes[mid+1:])
        return root

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
        if self.root:
            for node in self._in_order():
                node.update_position()
            for node in self._in_order():
                if node.left:
                    pygame.draw.line(screen, COLOR, (node.position.x, node.position.y), (node.left.position.x, node.left.position.y), 2)
                if node.right:
                    pygame.draw.line(screen, COLOR, (node.position.x, node.position.y), (node.right.position.x, node.right.position.y), 2)
            for node in self._in_order():
                node.draw(screen)
        
        for node in self.flying_nodes:
            node.position += node.velocity
            node.draw(screen)
        
        self.flying_nodes = [node for node in self.flying_nodes if node.position.y + Node.NODE_RADIUS >= 0]
    
    def _in_order(self) -> Iterator[Node]:
        if self.root is None:
            return
        yield from self.root
        
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

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

def main(config: Config = Config()):
    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Binary Search Tree Visualizer")

    clock = pygame.time.Clock()

    Node.NODE_RADIUS = config.NODE_RADIUS
    Node.SPRINGINESS = config.SPRINGINESS
    Node.DAMPING = config.DAMPING
    Node.CHILD_MOVE_FACTOR = config.CHILD_MOVE_FACTOR
    
    BinarySearchTree.LEVEL_SPACING = config.LEVEL_SPACING

    print("""
        Type a number to add node
        Click 'Clear' button or press C to clear tree
        Click 'Balance' button or press B to balance tree
          """)

    tree = BinarySearchTree(config.STARTING_NODES)
    input_value = ''
    selected_node = None
    running = True

    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)

    hide_instructions_at = time.time() + 3
    show_instructions = True

    # Create Clear button
    clear_button = Button(10, HEIGHT - 60, 100, 50, "Clear", GRAY, LIGHT_GRAY, COLOR, button_font)
    # Create Balance button
    balance_button = Button(WIDTH - 10 - 100, HEIGHT - 60, 100, 50, "Balance", GRAY, LIGHT_GRAY, COLOR, button_font)
    
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clear_button.is_clicked(event.pos):
                        tree.clear()
                    elif balance_button.is_clicked(event.pos):
                        tree.balance()
                    else:
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
                clear_button.update_hover(event.pos)
                balance_button.update_hover(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    tree.clear()
                elif event.key == pygame.K_b:
                    tree.balance()
                elif event.key == pygame.K_RETURN and input_value:
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
            text = font.render("Enter a number: ___", True, COLOR)
        else:
            text = font.render(input_value, True, COLOR)

        tree.draw(screen)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))
        
        # Draw the Clear and Balance buttons
        clear_button.draw(screen)
        balance_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()