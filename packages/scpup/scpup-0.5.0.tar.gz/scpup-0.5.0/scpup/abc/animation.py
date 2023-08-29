from itertools import cycle
from typing import Iterator

__all__ = [
  "EauAnimation",
  "EauABCAnimation",
  "EauLoopAnimation"
]

class EauABCAnimation(Iterator):
  __slots__ = [
    "sequence",
    "_value_"
  ]

  def __init__(self, _: tuple[tuple[int, int]]) -> None:
    """ Create an infinite animation object

    frame_order: tuple[tuple[int, int]] -> tuple to determinate de order of the animation frames, where each item is equal to (index, frames)
    """

  def __iter__(self) -> Iterator:
    return self

  def __next__(self) -> int:
    self._value_ = next(self.sequence)
    return self._value_
  
  @property
  def current(self) -> int:
    return self._value_


class EauLoopAnimation(EauABCAnimation):
  __slots__ = (
    "__frame_order",
  )

  def __init__(self, frame_order: tuple[tuple[int, int]]) -> None:
    self.__frame_order = frame_order
    self.restart()

  def restart(self) -> None:
    self.sequence = cycle(
      (frame_idx for frame_info in self.__frame_order for frame_idx in (frame_info[0],) * frame_info[1])
    )
    self._value_ = next(self.sequence)


class EauAnimation(EauABCAnimation):
  __slots__ = ()

  def __init__(self, frame_order: tuple[tuple[int, int]]) -> None:
    self.sequence = iter(
      (frame_idx for frame_info in frame_order for frame_idx in (frame_info[0],) * frame_info[1])
    )
    self._value_ = next(self.sequence)
