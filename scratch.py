from __future__ import annotations
import pygame
import random
from math import radians, sin, cos
from os.path import split, splitext
from abc import ABC, abstractmethod
from typing import Callable, Collection, Literal, Union


pygame.init()
screen = pygame.display.set_mode((480, 360))

class Asset:
    def __init__(self, filepath: str, name: str = None) -> None:
        self._name = name if name is not None else splitext(split(filepath)[-1])[0]
        
class Costume(Asset):
    def __init__(self,  filepath: str, name: str = None) -> None:
        super().__init__(filepath, name)
        self._image = pygame.image.load(filepath)
        self._width = self._image.get_width()
        self._height = self._image.get_height()


class Sound(Asset):
    def __init__(self,  filepath: str, name: str = None) -> None:
        super().__init__(filepath, name)
        self._sound = pygame.image.load(filepath)


class Target(ABC):
    def __init__(self,
                 name: str = "Sprite1", costumes: Collection[Costume] = None,
                 volume: float = 100
    ) -> None:
        self._name = name
        self._costumes = costumes if costumes is not None else []
        self._volume = volume
        self._costume_number = 0


class Sprite(Target):
    def __init__(self, x: float = 0, y: float = 0, size: float = 100, direction: float = 90, shown: bool = True, name: str = "Sprite1", costumes: Collection[Costume] = None, volume: float = 100) -> None:
        super().__init__(name, costumes, volume)
        self._x = x
        self._y = y
        self._size = size
        self._direction = direction  # Direction in radians, although displayed value should be in degrees
        self._shown = shown

    def move_steps(self, steps):
        self._x = constrain(self._x + steps * cos(self._direction), -240, 240)
        self._y = constrain(self._y + steps * sin(self._direction), -180, 180)
    
    def turn_right(self, degrees):
        self._direction += radians(degrees)
    
    def turn_left(self, degrees):
        self._direction += radians(degrees)

    def go_to(self, target: Union[Sprite, Literal["__random__"], Literal["__mouse__"]]):
        if target == "__random__":
            self._x = random.randint(-240, 240)
            self._y = random.randint(-180, 180)
        elif target == "__mouse__":
            self._x, self._y = pygame.mouse.get_pos()
        elif isinstance(target, Sprite):
            self._x = target._x
            self._y = target._y
        


class Stage(Target):
    def __init__(self, name: str = "Sprite1", costumes: Collection[Costume] = None, volume: float = 100) -> None:
        super().__init__(name="Stage", costumes=costumes, volume=volume)


Number = Union[int, float]
def constrain(value: Number, min_value: Number, max_value: Number) -> Number:
    if value < min_value: return min_value
    if value > max_value: return max_value
    return value


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()