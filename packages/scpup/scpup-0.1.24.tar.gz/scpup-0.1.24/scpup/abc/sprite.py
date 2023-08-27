from __future__ import annotations as ___
from ..utils.loader import load_image as _li
from .animation import EauAnimation as _EauAnimation
import pygame as _pygame

__all__ = [
  "EauSprite",
  "StaticSprite",
  "AnimatedSprite"
]

class EauSprite:
  __slots__ = [
    "__g"
  ]

  def __init__(self) -> None:
    self.__g = {}

  def add(self, *groups) -> None:
    for g in groups:
      if hasattr(g, "_spritegroup") and g not in self.__g:
        g.add_internal(self)
        self.add_internal(g)
  
  def remove(self, *groups) -> None:
    for g in groups:
      if g in self.__g:
        g.remove_internal(self)
        self.remove_internal(g)

  def add_internal(self, group):
    self.__g[group] = 0

  def remove_internal(self, group) -> None:
    del self.__g[group]
  
  def update(self, *_, **__) -> None:
    pass

  def kill(self) -> None:
    for g in self.__g:
      g.remove_internal(self)
    self.__g.clear()

  def groups(self) -> list:
    return list(self.__g)
  
  def alive(self) -> bool:
    return bool(self.__g)


class StaticSprite(EauSprite):
  __slots__ = [
    "image",
    "rect"
  ]

  def __init__(self, *paths: str, **rectargs) -> None:
    super().__init__()
    self.image, self.rect = _li(*paths, **rectargs)


class AnimatedSprite(EauSprite):
  __slots__ = [
    "images",
    "animations",
    "action"
  ]

  def __init__(self, *paths: str, size: int, animations: dict[str, _EauAnimation]) -> None:
    super().__init__()
    self.images: list[tuple[_pygame.Surface, _pygame.Rect]] = []
    for i in range(size):
      image, rect = _li(*paths[:-1], f"{paths[-1]}_{i}")
      self.images.append((image, rect))
    self.animations = animations
    self.action = self.animations.keys()[0]

  @property
  def animation(self) -> _EauAnimation:
    return self.animations[self.action]
    
  @property
  def image(self):
    return self.images[self.animation.current][0]

  @property
  def rect(self):
    return self.images[self.animation.current][1]


  # @overload()
  # def __init__(self, image: str, *, copy: bool) -> None: ...
  # @overload()
  # def __init__(self, image: pygame.Surface) -> None: ...
  # def __init__(self, image: str|pygame.Surface=None, *, copy: bool=True) -> None:
  #   pygame.sprite.Sprite.__init__(self)
  #   if image is not None:
  #     if isinstance(image, str):
  #       self.image = load_image(image, copy=copy)
  #     elif isinstance(image, pygame.Surface):
  #       self.image = image
  #     else:
  #       raise TypeError(f"Can't create sprite with argument image of type {type(image)!r}")
  #     self.rect = self.image.get_rect()
