import os as _os
import pygame as _pygame

__all__ = [
  "load_image",
  "load_sound"
]

BASE_PATH = _os.path.join(_os.getcwd(), "assets")

def load_image(*paths: str, alpha: bool = True, **rectargs) -> tuple[_pygame.Surface, _pygame.Rect]:
  path = _os.path.join(BASE_PATH, *paths)
  image = _pygame.image.load(path)
  if alpha:
    image = image.convert_alpha()
  else:
    image = image.convert()
  rect = image.get_rect(**rectargs)
  return image, rect

def load_sound(*paths: str):
  path = _os.path.join(BASE_PATH, *paths)
  sound = _pygame.mixer.Sound(path)
  return sound
