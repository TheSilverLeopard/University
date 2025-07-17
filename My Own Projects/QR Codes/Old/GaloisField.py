# IMPORTS #

from __future__ import annotations
import unittest

# GALOIS FIELD ELEMENT CLASS #

class GaloisFieldElement:

    EXPONENTIAL_STRINGS = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
    }

    def __init__(self, value: int = 0, galois_field: GaloisField = None):
        """Initialise a GaloisFieldElement object with a given value, prime, size and generator.

        Args:
            value (int): Value of the Galois Field element.
            galois_field (GaloisField): GaloisField object.
        """

        self.value = value
        self.galois_field = galois_field

    def __add__(self, other: GaloisFieldElement | int) -> GaloisFieldElement:
        """Add two numbers in GF(prime).

        Returns:
            GaloisFieldElement Result of adding two numbers in GF(prime).
        """

        return self.galois_field.add(self, other)

    __sub__ = __add__
    __radd__ = __add__

    def __mul__(self, other: GaloisFieldElement | int) -> GaloisFieldElement:
        """Multiply two numbers in GF(prime).

        Returns:
            GaloisFieldElement: Result of multiplying two numbers in GF(prime).
        """

        return self.galois_field.mul(self, other)

    __rmul__ = __mul__

    def __abs__(self) -> GaloisFieldElement:
        """Return the absolute value of a number in GF(prime).

        Returns:
            int: Absolute value of a number in GF(prime).
        """

        return self

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

        return self.galois_field.inv(self)

    def __str__(self) -> str:
        """Return a string representation of the GaloisFieldElement object.

        Returns:
            str: A string representation of the GaloisFieldElement object.
        """

        return 'a' + ''.join([self.EXPONENTIAL_STRINGS[n] for n in str(self.value - 1)])


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

    def _galois_field_multiplication(self, a: int, b: int) -> int:
        """Multiply two numbers in GF(prime)."""

        result = 0

        if b == -1:
            pass

        while b:
            if b & 1:
                result ^= a
            a <<= 1
            if a.bit_length() > self.n:
                a ^= self.prime
            b >>= 1

        if result.bit_length() > self.n:
            result ^= self.prime

        result &= (1 << self.n) - 1

        return result

    def add(self, a: GaloisFieldElement, b: GaloisFieldElement | int) -> GaloisFieldElement:
        """Add two numbers in GF(prime)."""
        # Convert integer to GaloisFieldElement if needed
        if isinstance(b, int):
            b = GaloisFieldElement(b, self)
        
        # Handle zeros
        if a.value == 0:
            return b
        if b.value == 0:
            return a
        
        # Get field values
        a_field = self.antilog_table[a.value].value
        b_field = self.antilog_table[b.value].value
        
        # XOR the field values
        result_field = a_field ^ b_field
        
        # If result is 0, return 0
        if result_field == 0:
            return GaloisFieldElement(0, self)
        
        # Special case: if field value is 1, this represents a⁰
        if result_field == 1:
            return GaloisFieldElement(1, self)  # representing a¹
        
        # Look up the result in the antilog table
        for i, elem in enumerate(self.antilog_table):
            if elem.value == result_field:
                return GaloisFieldElement(i, self)
            
        # If not in antilog table, try log table
        if result_field < len(self.log_table):
            return self.log_table[result_field]
        
        return GaloisFieldElement(0, self)

    def _generate_log_antilog_tables(self) -> tuple[list[GaloisFieldElement], list[GaloisFieldElement]]:
        """Generate log and antilog tables for arithmetic in GF(prime)."""
        raw_log_table = [0] * self.size
        raw_antilog_table = [0] * self.size
        
        # Generate tables
        current = 1
        for power in range(self.size - 1):
            raw_antilog_table[power] = current
            raw_log_table[current] = power
            current = self._galois_field_multiplication(current, self.generator)
            if current >= self.size:
                current ^= self.prime
    
        # Handle special cases
        raw_antilog_table[self.size - 1] = raw_antilog_table[0]
        raw_log_table[1] = 1  # Explicitly set log(1) = 1 to represent a¹
        
        # Convert to GaloisFieldElement
        log_table = [GaloisFieldElement(v, self) for v in raw_log_table]
        antilog_table = [GaloisFieldElement(v, self) for v in raw_antilog_table]
        
        return log_table, antilog_table

    def mul(self, a: GaloisFieldElement, b: GaloisFieldElement | int) -> GaloisFieldElement:
        """Multiply two numbers in GF(prime)."""
        # Convert integer to GaloisFieldElement if needed
        if isinstance(b, int):
            b = GaloisFieldElement(b, self)
        
        # Handle zeros
        if a.value == 0 or b.value == 0:
            return GaloisFieldElement(0, self)
        
        # Add exponents modulo (size-1)
        sum_exp = (a.value + b.value) % (self.size - 1)
        return GaloisFieldElement(sum_exp, self)

    def inv(self, a: GaloisFieldElement) -> GaloisFieldElement:
        """Return multiplicative inverse of a in GF(prime)."""
        if a.value == 0:
            raise ValueError("Cannot find multiplicative inverse of 0")

        # Using Fermat's little theorem: a^(p-1) = 1
        # Therefore, a^(p-2) is the multiplicative inverse of a
        # In our case, we're working with powers of a, so we need to find
        # the proper exponent that gives us the inverse

        # For element a^n, its inverse will be a^(size-1-n)
        inverse_power = self.size - 1 - a.value
        return GaloisFieldElement(inverse_power, self)
