import os
import pygame

BASE_PATH = os.path.join(__file__.split("src", 1).pop(0), "assets")

def load_image(*paths: str, alpha: bool = True, **rectargs) -> tuple[pygame.Surface, pygame.Rect]:
  path = os.path.join(BASE_PATH, *paths)
  image = pygame.image.load(path)
  if alpha:
    image = image.convert_alpha()
  else:
    image = image.convert()
  rect = image.get_rect(**rectargs)
  return image, rect

def load_sound(*paths: str):
  path = os.path.join(BASE_PATH, *paths)
  sound = pygame.mixer.Sound(path)
  return sound

"""
@Image('sprites', 'mini.png')
def mini(self, image):
  
  return image

load_image('sprites', 'mini.png', center=(0, 0))
"""