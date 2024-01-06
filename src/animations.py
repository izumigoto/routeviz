from typing import Callable, Optional, DefaultDict
from enum import Enum
import math
import pygame
from collections import defaultdict

from .constants import (
    DARK,
    FONT_14,
    GOAL,
    GRAY,
    GREEN,
    START,
    WEIGHT,
    MIN_SIZE,
    MAX_SIZE,
    CELL_SIZE
)


class Animation(Enum):
    WALL_ANIMATION = "WALL_ANIMATION"
    WEIGHT_ANIMATION = "WEIGHT_ANIMATION"
    PATH_ANIMATION = "PATH_ANIMATION"


AnimationCallback = Callable[[], None]


class AnimatingNode:
    def __init__(
        self,
        rect: pygame.Rect,
        value: str,
        ticks: int,
        center: tuple[int, int],
        color: tuple[int, int, int],
        after_animation: Optional[AnimationCallback] = None,
        colors: list[tuple[int, int, int]] = [],
        animation: Animation = Animation.WALL_ANIMATION,
        duration: int = 300,
    ) -> None:
        self.rect = rect
        self.value = value
        self.ticks = ticks
        self.center = center
        self.color = color
        self.colors = colors
        self.animation = animation
        self.duration = duration
        self.after_animation = after_animation
        self.progress = 0
        self.start = self.ticks
        self.time_updated = False

    def __repr__(self) -> str:
        return f"AnimatingNode{tuple(vars(self).values())}"

    def __str__(self) -> str:
        return f"AnimatingNode: Value: {self.value}, " \
            + f"Progress: {self.progress}/{self.duration}"


class Animator:

    def __init__(self, surface: pygame.surface.Surface, maze) -> None:
        from .maze import Maze

        self.surface = surface
        self.maze: Maze = maze

        self.animating = False
        self.nodes_to_animate: DefaultDict[tuple[int, int], list[AnimatingNode]] = defaultdict(list)
        self.need_update = False

    def add_nodes_to_animate(
        self,
        nodes: list[AnimatingNode],
        delay: int = 0,
        gap: int = 10
    ) -> None:
        """Add nodes for animation

        Args:
            nodes (list[AnimatingNode]): List of nodes
            delay (bool, optional): Whether to wait for previous nodes to animate. Defaults to False.
        """

        # Update first node's ticks and add it to the list
        if len(self.nodes_to_animate):
            last_node = list(self.nodes_to_animate.values())[-1][0]
            nodes[0].ticks = last_node.ticks + delay

        self.nodes_to_animate[nodes[0].center].append(nodes[0])

        # Rest of the nodes
        for i in range(1, len(nodes)):
            nodes[i].ticks = nodes[i - 1].ticks + gap
            self.nodes_to_animate[nodes[i].center].append(nodes[i])

        self.need_update = True

    def animate_nodes(self):
        """Animate nodes in the nodes_to_animate list
        """
        # Update starting time for animating nodes
        if self.need_update:
            for center, nodes in self.nodes_to_animate.items():
                for node in nodes:
                    if not node.time_updated:
                        node.ticks += (pygame.time.get_ticks() - node.start)
                        node.time_updated = True

            self.need_update = False

        # Animate every node
        for center, nodes in self.nodes_to_animate.items():
            for i in range(len(nodes) - 1, -1, -1):
                node = nodes[i]
                node.progress += pygame.time.get_ticks() - node.ticks
                node.ticks = pygame.time.get_ticks()

                if node.progress > 0:
                    self.nodes_to_animate[center][:i] = []
                    break
            else:
                continue

            # Call respective functions
            if node.animation == Animation.WALL_ANIMATION:
                self._wall_animation(node)
            elif node.animation == Animation.PATH_ANIMATION:
                self._path_animation(node)
            else:
                self._weight_animation(node)

            # Handle node images
            row, col = self.maze.get_cell_pos(node.center)
            if (row, col) == self.maze.start:
                image_rect = START.get_rect(center=node.center)
                self.surface.blit(START, image_rect)

            elif (row, col) == self.maze.goal:
                image_rect = GOAL.get_rect(center=node.center)
                self.surface.blit(GOAL, image_rect)

            elif (cost := self.maze.maze[row][col].cost) > 1:
                image_rect = WEIGHT.get_rect(center=node.center)
                self.surface.blit(WEIGHT, image_rect)

                text = FONT_14.render(
                    str(cost), True, GRAY
                )
                text_rect = text.get_rect()
                text_rect.center = image_rect.center
                self.surface.blit(text, text_rect)

            # Update maze node and remove current animating node
            if node.progress >= node.duration:
                pos = self.maze.get_cell_pos(node.center)
                self.maze.set_cell(pos, node.value)

                self.nodes_to_animate[center].remove(node)
                if not self.nodes_to_animate[center]:
                    self.nodes_to_animate.pop(center)

                if node.after_animation:
                    node.after_animation()

    def _wall_animation(self, node: AnimatingNode) -> None:
        """Handle wall animation

        Args:
            node (AnimatingNode): Wall node
        """

        # Calculate size as per ease-out func
        if node.progress < node.duration / 2:
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, node.duration / 2
            )
        else:
            size = self._ease_out_sine(
                node.progress - node.duration / 2,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, node.duration / 2
            )

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, node.color, node.rect)

    def _weight_animation(self, node: AnimatingNode) -> None:
        """Handle weighted node animation

        Args:
            node (AnimatingNode): Weighted node
        """

        # Calculate size as per ease-out func
        if node.progress < node.duration / 2:
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, node.duration / 2
            )

        else:
            size = self._ease_out_sine(
                node.progress - node.duration / 2,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, node.duration / 2
            )

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, GRAY, node.rect)
        pygame.draw.rect(self.surface, DARK, node.rect, width=8)

    def _path_animation(self, node: AnimatingNode) -> None:
        """Animate solution path

        Args:
            node (AnimatingNode): Node in solution path
        """
        border_radius = 0
        if node.progress < 0.02 * node.duration:
            size = node.rect.width
        elif node.progress < 0.75 * node.duration:
            duration = 0.75 * node.duration
            size = self._ease_out_sine(
                node.progress, MIN_SIZE, MAX_SIZE - MIN_SIZE, duration
            )

            border_radius = int(0.40 * size)
            if size > CELL_SIZE:
                border_radius = int(0.12 * size)

        else:
            duration = 0.25 * node.duration
            progress = node.progress - 0.75 * node.duration
            size = self._ease_out_sine(
                progress,
                MAX_SIZE, CELL_SIZE - MAX_SIZE, duration
            )
            border_radius = 0

        if node.progress < 0.02 * node.duration:
            color = node.colors[0]
        elif node.progress < 0.50 * node.duration:
            progress = node.progress
            duration = 0.50 * node.duration

            color = self._ease_out_sine_color(node.colors[1], node.colors[2])

        elif node.progress < 0.75 * node.duration:
            progress = node.progress - 0.50 * node.duration
            duration = 0.25 * node.duration

            color = self._ease_out_sine_color(node.colors[2], node.colors[3])
        else:
            progress = node.progress - 0.75 * node.duration
            duration = 0.25 * node.duration

            color = self._ease_out_sine_color(node.colors[3], node.colors[-1])

        # Update size
        node.rect.width = node.rect.height = int(size)
        node.rect.center = node.center

        # Draw
        pygame.draw.rect(self.surface, color, node.rect,
                         border_radius=border_radius)

        if node.progress > 0.50 * node.duration:
            pygame.draw.rect(
                self.surface,
                GREEN if node.progress < 0.75 * node.duration else GRAY,
                node.rect,
                border_radius=border_radius,
                width=1
            )

    def _ease_out_sine_color(
        self,
        time: float,
        color_a: tuple[int, int, int],
        color_b: tuple[int, int, int],
        duration: float
    ) -> tuple[int, int, int]:
        """Calculate the current color

        Args:
            time (float): The current time of the animation.
            color_a (tuple[int, int, int]): The starting color of the animation.
            color_a (tuple[int, int, int]): The final color of the animation.
            duration (float): The total duration of the animation in milliseconds.

        Returns:
            tuple[int, int, int]: Color at the current time.
        """
        return (
            round(self._ease_out_sine(
                progress, old, new - old, duration
            ))
            for old, new in zip(color_a, color_b)
        )

    def _ease_out_sine(
        self,
        time: float,
        starting_value: float,
        change_in_value: float,
        duration: float
    ) -> float:
        """Calculate current size

        Args:
            time (float): The current time of the animation.
            starting_value (float): The starting value of the animation.
            change (float): The change in value of the animation.
            duration (float): The total duration of the animation in milliseconds.

        Returns:
            float: Current value
        """
        return change_in_value * math.sin(time / duration * (math.pi / 2)) \
            + starting_value

    def __repr__(self) -> str:
        return f"Animator{tuple(vars(self).values())}"