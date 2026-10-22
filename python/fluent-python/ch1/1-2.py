"""
vector2d.py: a simplistic class demostrating some special methods

It is simplistic for didactic reasons. It locks proper erro handling,
especially in the __add__ and __mul__ methods.

This example is greatly expanded later.

Addtion
Absolut value
Scalar multiplication
"""

import math


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x!r}, {self.y!r})"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        x = self.x * scalar
        y = self.y * scalar
        return Vector(x, y)

    def __bool__(self):
        return bool(self.x or self.y)
