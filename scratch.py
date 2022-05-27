from __future__ import annotations
from dataclasses import dataclass, field
import pygame
import random
from math import radians, sin, cos
from os.path import split, splitext
from abc import ABC, abstractmethod
from typing import Any, Callable, Collection, Literal, Sequence, Union


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
        self._sound = pygame.mixer.Sound(filepath)


class Target(ABC):
    def __init__(self,
                 name: str = "Sprite1", costumes: Collection[Costume] = None,
                 volume: float = 100
    ) -> None:
        self._name = name
        self._costumes = costumes if costumes is not None else []
        self._volume = volume
        self._costume_number = 0

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass


class Sprite(Target):
    def __init__(self, x: float = 0, y: float = 0, size: float = 100, direction: float = 90, shown: bool = True, name: str = "Sprite1", costumes: Collection[Costume] = None, volume: float = 100) -> None:
        super().__init__(name, costumes, volume)
        self._x = x
        self._y = y
        self._size = size
        self._direction = direction  # Direction in radians, although displayed value should be in degrees
        self._shown = shown
        self._glide_to_pos = (0, 0)
        self._gliding = False

    def draw(self):
        self.__apply_effects()
        try:
            screen.blit(self._costumes[self._costume_number], (self._x, self._y))
        except IndexError:
            pass

    def __apply_effects(self):
        pass

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

    def goto_xy(self, x: float, y: float):
        self._x = constrain(x, -240, 240)
        self._y = constrain(y, -180, 180)

    def glide_to(self, x: float, y: float):
        pass

@dataclass(repr=True, order=False, frozen=True)
class PriorityItem:
        priority: int
        item: Any

class ExclusivityException(Exception):
    pass

class PriorityList:
    def __init__(self, exclusive=False) -> None:
        self.__contents: list[PriorityItem] = []
        self.__is_exclusive = exclusive
    
    def append(self, item, priority) -> None:
        index = self.__find_index(priority)
        try:
            # The item being appended shares a priority with an existing item
            if self.__contents[index] == priority and self.__is_exclusive:
                raise ExclusivityException("Object cannot have the same priority as another: "
                    f"Item {index} ({self.__contents[index]}) has the same priority as the item "
                    f"being appended: {priority}."
                )
        except:
            pass

        self.__contents.insert(index, PriorityItem(priority, item))

    @property
    def highest_priority(self):
        return min(self.__contents, key=lambda i: i.priority).priority

    @property
    def lowest_priority(self):
        return max(self.__contents, key=lambda i: i.priority).priority

    def __find_index(self, priority):
        i = 0
        while (i < len(self.__contents) and (self.__contents[i].priority < priority)):
            i += 1
        
        while (i < len(self.__contents) and (self.__contents[i].priority == priority)):
            i += 1
        
        return i

    def __getitem__(self, index):
        return self.__contents[index].item

    def __iter__(self):
        return iter([item.item for item in self.__contents])

class Stage(Target):
    def __init__(self, name: str = "Sprite1", costumes: Collection[Costume] = None, volume: float = 100) -> None:
        super().__init__(name="Stage", costumes=costumes, volume=volume)

    def update(self):
        pass

    def draw(self):
        try:
            screen.blit(self._costumes[self._costume_number], (0, 0))
        except IndexError:
            pass

class Project:
    def __init__(self) -> None:
        self.stage = Stage()
        self.sprites = PriorityList(exclusive=True)
    
    def update(self) -> None:
        self.stage.update()
        self.stage.draw()
        for sprite in self.sprites:
            sprite.update()
            sprite.draw()

    def add_sprite(self, sprite: Sprite) -> None:
        if check_type(sprite, (Sprite,)):
            self.sprites.append(sprite, self.sprites.lowest_priority)

Number = Union[int, float]
def constrain(value: Number, min_value: Number, max_value: Number) -> Number:
    if value < min_value: return min_value
    if value > max_value: return max_value
    return value


def check_type(value, expected_types: Collection, error: bool = False,
               error_msg = None) -> bool | Exception:
    if type(value) in expected_types:
        if error:
            raise TypeError(error_msg if error_msg is not None else (
                f"Expected type from: {', '.join(expected_types)} but {value}"
                f"of type {type(value)} was received.")
            )
        else:
            return False
    return True


def main():
    running = True
    project = Project()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        project.update()

    pygame.quit()


if __name__ == "__main__":
    main()
    
    