from itertools import cycle as _cycle
from typing import Iterator as _Iterator

__all__ = [
  "EauAnimation"
]

class EauAnimation(_Iterator):
  __slots__ = [
    "__frame_order",
    "sequence",
    "_value_"
  ]

  def __init__(self, frame_order: tuple[tuple[int, int]]):
    self.__frame_order = frame_order
    self._start()

  def __iter__(self) -> _Iterator:
    return self
  
  def __next__(self) -> int:
    self._value_ = next(self.sequence)
    return self._value_
  
  def _start(self) -> None:
    self.sequence = _cycle(
      (frame_idx for frame_info in self.__frame_order for frame_idx in (frame_info[0],) * frame_info[1])
    )
    self._value_ = next(self.sequence)

  @property
  def current(self) -> int:
    return self._value_
  
  def reset(self) -> None:
    self._start()