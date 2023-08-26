from __future__ import annotations
from itertools import cycle
from ..utils.loader import load_image

class EauSprite:
  __slots__ = [
    "__g"
  ]

  def __init__(self) -> None:
    self.__g = {}

  def add(self, *groups) -> None:
    for g in groups:
      if g not in self.__g:
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
    self.image, self.rect = load_image(*paths, **rectargs)


# class EauAnimation:
#   __slots__ = [
#     ""
#   ]

#   def __init__(self, frame_order)


class AnimatedSprite(EauSprite):
  __slots__ = [
    "frames",
    "rect"
  ]

  def __init__(self, *paths: str, size: int, order: tuple | None = None) -> None:
    super().__init__()
    for i in range(size):
      self.frames, _ = load_image(*paths[:-1], f"{paths[-1]}_{i}")
    
