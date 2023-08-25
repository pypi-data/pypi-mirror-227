from __future__ import annotations

from abc import ABCMeta

class EauSprite(metaclass=ABCMeta):
  __slots__ = [
    "__g",
    "rect"
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
