# IMPORTS #

from __future__ import annotations
import unittest

# GALOIS FIELD ELEMENT CLASS #

class GaloisFieldElement:

    def __init__(self, value: int = 0, galois_field: GaloisField = None):
        """Initialise a GaloisFieldElement object with a given value, prime, size and generator.

        Args:
            value (int): Value of the Galois Field element.
            galois_field (GaloisField): GaloisField object.
        """

        self.value = value
        self.galois_field = galois_field

        if galois_field is not None:
            self.prime = self.galois_field.prime
            self.size = self.galois_field.size
            self.n = self.galois_field.n

    def __add__(self, other: GaloisFieldElement | int) -> GaloisFieldElement:
        """Add two numbers in GF(prime).

        Returns:
            GaloisFieldElement Result of adding two numbers in GF(prime).
        """

        return GaloisFieldElement((self.value + (other.value if isinstance(other, GaloisFieldElement) else other)) % self.galois_field.size, self.galois_field)

    __sub__ = __add__
    __radd__ = __add__

    def __mul__(self, other: GaloisFieldElement | int) -> GaloisFieldElement:
        """Multiply two numbers in GF(prime).

        Returns:
            GaloisFieldElement: Result of multiplying two numbers in GF(prime).
        """

        b = other.value if isinstance(other, GaloisFieldElement) else other
        value = self.value

        if hasattr(self, 'galois_field') and hasattr(self.galois_field, 'antilog_table'):
            return (self.value * other.value) % self.galois_field.size

        result = 0

        if b == -1:
            pass

        while b:
            if b & 1:
                result ^= value
            value <<= 1
            if value.bit_length() > self.n:
                value ^= self.prime
            b >>= 1

        if result.bit_length() > self.n:
            result ^= self.prime

        result &= (1 << self.n) - 1

        return GaloisFieldElement(result, self.galois_field)

    __rmul__ = __mul__

    def __abs__(self) -> int:
        """Return the absolute value of a number in GF(prime).

        Returns:
            int: Absolute value of a number in GF(prime).
        """

        return abs(self.value)

    def __eq__(self, other: GaloisFieldElement | int) -> bool:
        """Check if two numbers are equal in GF(prime).

        Returns:
            bool: True if two numbers are equal in GF(prime), False otherwise.
        """

        return self.value == (other.value if isinstance(other, GaloisFieldElement) else other)

    def __ne__(self, other: GaloisFieldElement | int) -> bool:
        """Check if two numbers are not equal in GF(prime).

        Returns:
            bool: True if two numbers are not equal in GF(prime), False otherwise.
        """

        return self.value != (other.value if isinstance(other, GaloisFieldElement) else other)

    def __lt__(self, other: GaloisFieldElement | int) -> bool:
        """Check if less than other in GF(prime).

        Returns:
            bool: True if less than other in GF(prime), False otherwise.
        """

        return self.value < (other.value if isinstance(other, GaloisFieldElement) else other)

    def __le__(self, other: GaloisFieldElement | int) -> bool:
        """Check if less than or equal to other in GF(prime).

        Returns:
            bool: True if less than or equal to other in GF(prime), False otherwise.
        """

        return self.value <= (other.value if isinstance(other, GaloisFieldElement) else other)

    def __gt__(self, other: GaloisFieldElement | int) -> bool:
        """Check if greater than other in GF(prime).

        Returns:
            bool: True if greater than other in GF(prime), False otherwise.
        """

        return self.value > (other.value if isinstance(other, GaloisFieldElement) else other)

    def __ge__(self, other: GaloisFieldElement | int) -> bool:
        """Check if greater than or equal to other in GF(prime).

        Returns:
            bool: True if greater than or equal to other in GF(prime), False otherwise.
        """

        return self.value >= (other.value if isinstance(other, GaloisFieldElement) else other)

    def inv(self) -> GaloisFieldElement:
        """Find multiplicative inverse using exponentiation: a^(size-2).

        Returns:
            GaloisFieldElement: Multiplicative inverse of a in GF(prime).
        """

        if self.value == 0:
            raise ZeroDivisionError("Zero has no inverse in a field!")

        base = self.value

        if hasattr(self, 'galois_field') and hasattr(self.galois_field, 'antilog_table'):
            return self.galois_field.antilog_table[(self.size - 1 - self.galois_field.log_table[base]) % (self.size - 1)]

        result = 1
        power = self.size - 2

        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1

        return result

    def __str__(self) -> str:
        """Return a string representation of the GaloisFieldElement object.

        Returns:
            str: A string representation of the GaloisFieldElement object.
        """

        return str(self.value)

# GALOIS FIELD CLASS #

class GaloisField:

    def __init__(self, prime: int = 0x11B, size: int = 0x100, generator: int = 2):
        """Initialise a GaloisField object with a given prime, size and generator.

        Args:
            prime (int): Prime number of the Galois Field.
            size (int): Size of the Galois Field.
            generator (int): primitive element (commonly 2).
        """

        self.prime = prime
        self.size = size
        self.generator = generator

        self.n = self.size.bit_length() - 1

        self.log_table, self.antilog_table = self._generate_log_antilog_tables()

    def _generate_log_antilog_tables(self) -> (list[int], list[int]):
        """Generate log and antilog tables for arithmetic in GF(prime).

        Returns:
            (list, list): (log_table, antilog_table)
                - log_table[x] gives log_base_generator(x) in GF
                - antilog_table[n] gives generator^n in GF
        """

        log_table = [GaloisFieldElement(0, self)] * self.size
        antilog_table = [GaloisFieldElement(0, self)] * self.size

        value = GaloisFieldElement(1, self)
        visited = set()

        for i in range(1, self.size):
            if value.value in visited:
                raise ValueError(f"Generator {self.generator} is NOT primitive for field of size {self.size}, "
                                 f"repeats after {i} iterations. Use a primitive generator.")
            visited.add(value.value)

            log_table[i - 1] = value
            antilog_table[value.value - 1] = GaloisFieldElement(i - 1, self)

            value *= self.generator

        antilog_table *= 2
        log_table[-1] = GaloisFieldElement(1, self)

        return log_table, antilog_table

# QUICK GALOIS FIELD #

class QuickGaloisField(GaloisField):

    def __init__(self, prime: int = 0x11B, size: int = 0x100, generator: int = 2):
        """Initialise a QuickGaloisField object with a given prime, size and generator.

        Args:
            prime (int): Prime number of the Galois Field.
            size (int): Size of the Galois Field.
            generator (int): primitive element (commonly 2).
        """

        super().__init__(prime, size, generator)

    def mul(self, a: int, b: int) -> int:
        """Multiply two numbers in GF(prime) using log and antilog tables.

        Returns:
            int: Result of multiplying two numbers in GF(prime).
        """

        if a == 0 or b == 0:
            return 0

        return self.antilog_table[(self.log_table[a] + self.log_table[b]) % (self.size - 1)]

    def inv(self, a: int) -> int:
        """Find multiplicative inverse using log and antilog tables.

        Returns:
            int: Multiplicative inverse of a in GF(prime).
        """

        if a == 0:
            raise ZeroDivisionError("Zero has no inverse in a field!")

        return self.antilog_table[(self.size - 1 - self.log_table[a]) % (self.size - 1)]

# TEST GALOIS FIELD CLASS #

class TestGaloisField(unittest.TestCase):

    def setUp(self):
        self.gf8 = QuickGaloisField(0x11D, 0x100, 2)

    def test_8bit(self):
        self.assertEqual(self.gf8.mul(0x53, 0xCA), 0x01)
        self.assertEqual(self.gf8.mul(0xFF, 0x00), 0x00)
        self.assertEqual(self.gf8.mul(0x01, 0x01), 0x01)
        self.assertEqual(self.gf8.mul(0xFF, self.gf8.inv(0xFF)), 0x01)

    def test_exceptions(self):
        with self.assertRaises(ZeroDivisionError):
            self.gf8.inv(0x00)


if __name__ == '__main__':
    unittest.main()