# IMPORTS #

from __future__ import annotations

import unittest

# GALOIS FIELD ELEMENT CLASS #

class GaloisFieldElement:

    EXPONENTIAL_STRINGS = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
    }

    def __init__(self, real_value: int = 0, log_value: int = 0, field: GaloisField = None):

        self.real_value = real_value
        self.log_value = log_value

        self.field = field

    def __add__(self, other: GaloisFieldElement) -> GaloisFieldElement:

        return GaloisFieldElement(self.real_value + other.real_value, self.log_value ^ other.log_value, self.field)

    __sub__ = __add__
    __radd__ = __add__

    def __mul__(self, other: GaloisFieldElement) -> GaloisFieldElement:

        return GaloisFieldElement(self.real_value * other.real_value, (self.log_value + other.log_value) % self.field.size, self.field)

    __rmul__ = __mul__

    def __abs__(self) -> int:

        return abs(self.real_value)

    def __eq__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value == (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __ne__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value != (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __lt__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value < (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __le__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value <= (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __gt__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value > (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __ge__(self, other: GaloisFieldElement | float | int) -> bool:

        return self.real_value >= (other.real_value if isinstance(other, GaloisFieldElement) else other)

    def __str__(self) -> str:

        return 'a' + ''.join([self.EXPONENTIAL_STRINGS[n] for n in str(self.log_value - 1)])

# GALOIS FIELD CLASS #

class GaloisField:

    def __init__(self, prime: int = 0x11B, size: int = 0x100, generator: int = 2):

        self.prime = prime
        self.size = size
        self.generator = generator

        self.n = self.size.bit_length()

        self.log_table = self._generate_log_table()
        print([(v.real_value, v.log_value) for v in self.log_table])

