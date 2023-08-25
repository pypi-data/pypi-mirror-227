from __future__ import annotations

import pygame.sprite
from abc import ABCMeta
from .group import EauGroup

class EauSprite(metaclass=ABCMeta):
  __slots__ = [
    "__g",
    "rect"
  ]

  def __init__(self) -> None:
    self.__g = {}

  def add(self, *groups: pygame.sprite.Group) -> None:
    for g in groups:
      if (hasattr(g, '_spritegroup') or isinstance(g, EauGroup)) and g not in self.__g:
        g.add_internal(self)
        self.add_internal(g)
  
  def remove(self, *groups: pygame.sprite.Group) -> None:
    for g in groups:
      if (hasattr(g, '_spritegroup') or isinstance(g, EauGroup)) and g in self.__g:
        g.remove_internal(self)
        self.remove_internal(g)

  def add_internal(self, group: pygame.sprite.Group):
    self.__g[group] = 0

  def remove_internal(self, group: pygame.sprite.Group) -> None:
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
