from typing import Iterator as _Iterator

__all__ = [
  "EauGroup"
]

class EauGroup:
  _spritegroup = True

  __slots__ = [
    "__s",
    "_lostsprites"
  ]

  def __init__(self) -> None:
    self.__s = {}
    self._lostsprites = []

  def __bool__(self) -> bool:
      return len(self) > 0

  def __len__(self) -> int:
      return len(self.__s)

  def __iter__(self) -> _Iterator:
      return iter(self.sprites())

  def __contains__(self, sprite) -> bool:
      return self.has(sprite)

  def add_internal(self, sprite) -> None:
    self.__s[sprite] = 0

  def remove_internal(self, sprite) -> None:
    lost_rect = self.__s[sprite]
    if lost_rect:
      self._lostsprites.append(lost_rect)
    del self.__s[sprite]
  
  def sprites(self) -> list:
    return list(self.__s)

  def add(self, *sprites) -> None:
    for sprite in sprites:
      if not sprite in self.__s:
        self.add_internal(sprite)
        sprite.add_internal(self)

  def remove(self, *sprites) -> None:
    for sprite in sprites:
      if sprite in self.__s:
        self.remove_internal(sprite)
        sprite.remove_internal(self)

  def update(self, *args, **kwargs) -> None:
    for sprite in self.sprites():
      sprite.update(*args, **kwargs)

  def draw(self, surface) -> None:
    sprites = self.sprites()
    if hasattr(surface, "blits"):
      self.__s.update(
        zip(sprites, surface.blits((spr.image, spr.rect) for spr in sprites))
      )
    else:
      for spr in sprites:
        self.__s[spr] = surface.blit(spr.image, spr.rect)
    self._lostsprites = []

  def clear(self, surface, bg):
    for lost_clear_rect in self._lostsprites:
      surface.blit(bg, lost_clear_rect, lost_clear_rect)
    for clear_rect in self.__s.values():
      if clear_rect:
        surface.blit(bg, clear_rect, clear_rect)

  def empty(self) -> None:
    for sprite in self.__s:
      self.remove_internal(sprite)
      sprite.remove_internal(self)



