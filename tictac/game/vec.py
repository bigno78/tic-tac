from __future__ import annotations # to be able to use Vec type in Vec itself

class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __add__(self, other: Vec) -> Vec:
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec) -> Vec:
        return self.__add__(-other)

    def __iadd__(self, other: Vec) -> Vec:
        self.x += other.x
        self.y += other.y
        return self

    def __str__(self):
        return f'({self.x}, {self.y})'
