# IMPORTS #

from __future__ import annotations

import unittest

# POLYNOMIAL CLASS #

class Polynomial:

    EXPONENTIAL_STRINGS = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
    }

    def __init__(self, coefficients: list):
        """Initialise a Polynomial object with given coefficients.

        Args:
            coefficients (list[int]): List of coefficient values.

        Raises:
            ValueError: If coefficients None or empty
        """

        if coefficients is None or len(coefficients) == 0:
            raise ValueError("Coefficients must be provided")

        self.coefficients = coefficients
        self.degree = len(coefficients)

    def __add__(self, other: Polynomial) -> Polynomial:
        """Add two Polynomial objects together.

        Returns:
            Polynomial: Result of adding two Polynomial objects.
        """

        max_degree = max(self.degree, other.degree)
        result = [0] * max_degree

        for degree in range(max_degree):
            a = self.coefficients[degree] if degree < self.degree else 0
            b = other.coefficients[degree] if degree < other.degree else 0
            result[degree] = a + b

        return Polynomial(result)

    def __sub__(self, other: Polynomial) -> Polynomial:
        """Subtract two Polynomial objects.

        Returns:
            Polynomial: Result of subtracting two Polynomial objects.
        """

        return self + (other * -1)

    def __mul__(self, other: Polynomial | int | float) -> Polynomial:
        """Multiplies a Polynomial object by a constant value or another polynomial.
    
        Returns:
            Polynomial: Result of multiplying two polynomials or polynomial by scalar.
        """

        print(self, other, sep="  ########  ")

        if isinstance(other, Polynomial):
            result = [0] * (self.degree + other.degree - 1)
            for i in range(self.degree):
                for j in range(other.degree):
                    degree = i + j
                    if degree < len(result):
                        result[degree] += self.coefficients[i] * other.coefficients[j]
            return Polynomial(result)

        return Polynomial([coefficient * other for coefficient in self.coefficients])

    def copy(self) -> Polynomial:
        """Return a copy of the polynomial.

        Returns:
            Polynomial: A copy of the polynomial.
        """
        return Polynomial(self.coefficients.copy())

    def shift(self, degrees: int = 1) -> Polynomial:
        """Shifts the polynomial by a number of degrees.

        Returns:
            Polynomial: A copy of the polynomial shifted by a number of degrees.
        """

        return Polynomial([0] * degrees + self.coefficients)
    
    def __truediv__(self, other: Polynomial | int | float) -> (Polynomial, Polynomial):
        """Divides two Polynomial objects or by a constant value.
    
        Returns:
            Polynomial: Result of dividing two Polynomial objects or by a constant value.
            Polynomial: Remainder of the division.
        """

        if isinstance(other, (int, float)):
            return self * (1 / other), 0

        if other.degree > self.degree:
            raise ValueError("Cannot divide polynomial by a polynomial with higher degree")

        remainder = self.copy()
        quotient_coefficients = [0] * (self.degree - other.degree + 1)

        for degree in range(self.degree - other.degree, -1, -1):
            if remainder.degree < other.degree:
                break

            lead_term = remainder.coefficients[-1] / other.coefficients[-1]
            quotient_coefficients[degree] = lead_term

            subtractor = other.copy().shift(degree) * lead_term

            remainder -= subtractor
            remainder.coefficients = [c for c in remainder.coefficients if abs(c) > 1e-10]

            if not remainder.coefficients:
                remainder.coefficients = [0]

        return Polynomial(quotient_coefficients), remainder

    def __str__(self) -> str:
        """Return a string representation of the Polynomial object.

        Returns:
            str: A string representation of the Polynomial object.
        """

        out = ""
        first_term = True

        for degree, coefficient in enumerate(self.coefficients):
            if coefficient == 0:
                continue

            if not first_term:
                out += " + " if coefficient > 0 else " - "
            elif coefficient < 0:
                out += "-"

            if abs(coefficient) != 1 or degree == 0:
                out += str(abs(coefficient))

            if degree > 0:
                out += "x"
                if degree > 1:
                    out += ''.join([self.EXPONENTIAL_STRINGS[n] for n in str(degree)])

            first_term = False

        return out or "0"
    
# POLYNOMIAL CLASS TESTS #

from GaloisField import GaloisField, GaloisFieldElement

class TestPolynomial(unittest.TestCase):

    def setUp(self):
        self.gf = GaloisField(0x11D, 0x100, 2)

    def test_galois_field(self):
        print("\nTesting individual operations first:")
        a = GaloisFieldElement(25, self.gf)  # a²⁵
        b = GaloisFieldElement(1, self.gf)   # a¹

        print(f"\na²⁵ field value: {self.gf.antilog_table[25].value}")
        print(f"a¹ field value: {self.gf.antilog_table[1].value}")
        
        sum_result = self.gf.add(a, b)
        print(f"a²⁵ + a¹ = {sum_result}")
        
        mul_result = self.gf.mul(a, b)
        print(f"a²⁵ × a¹ = {mul_result}")

        print("\nNow testing polynomial addition:")
        p1 = Polynomial([
            GaloisFieldElement(25, self.gf),  # a²⁵
            GaloisFieldElement(24, self.gf),  # a²⁴x
            GaloisFieldElement(1, self.gf)    # ax²
        ])
        print(f"First polynomial: {p1}")

        p2 = Polynomial([
            GaloisFieldElement(1, self.gf),   # a¹
            GaloisFieldElement(25, self.gf),  # a²⁵x
            GaloisFieldElement(0, self.gf)    # x²
        ])
        print(f"Second polynomial: {p2}")

        result = p1 + p2
        print(f"Sum: {result}")

    def test_inverse(self):
        """Test the inverse function for correctness."""
        print("\nTesting inverse function:")
        # Test several elements
        for power in [1, 2, 25, 50]:
            a = GaloisFieldElement(power, self.gf)
            try:
                a_inv = self.gf.inv(a)
                product = self.gf.mul(a, a_inv)
                print(f"a^{power} × (a^{power})⁻¹ = a^{product.value}")
                if product.value != 0:  # Should be a⁰
                    print(f"ERROR: Expected a⁰, got a^{product.value}")
            except ValueError as e:
                print(f"Error with a^{power}: {e}")


if __name__ == '__main__':
    unittest.main()