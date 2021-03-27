import numpy as np


class Torus:
    """
    Torus elements are real numbers in the range [0, 1).
    The number of real numbers we can represent in that range is limited by log2(q).
    We can represent integers mod p in the torus as far as p < q.
    """
    q = 2 ** 64

    def __init__(self, value=0):
        self.data = np.uint64(value)

    def copy(self):
        new = Torus(self.data.item())
        new.q = self.q
        return new

    @classmethod
    def from_real(cls, value):
        """
        Takes a real number from [0, 1) and outputs a Torus object representing it
        """
        if value < 0 or value >= 1:
            print(
                f"Warning: value {value} is not in the range [0, 1), it will be converted into a real modulo 1 = {value % 1}"
            )
        value = value % 1
        return Torus((value * cls.q) % cls.q)

    def to_real(self, p):
        """
        Takes a Torus element and outputs its real representation in [0, 1) using
        log2(p) bits of precision
        """
        # this mask any bits not included in the left most log2(p) bits
        rounded = np.uint64(np.round(self.data / (self.q / p)))
        return rounded / p

    @classmethod
    def from_int(cls, value, p):
        """
        Takes an integer number in [0, p) and outputs a Torus object representing it
        using log2(p) bits of precision
        """
        if value < 0 or value >= p:
            print(
                f"Warning: value {value} is not in the range [0, p), it will be converted into an integer modulo p = {value % p}"
            )
        value = int(value % p)
        return Torus(value * (cls.q / p) % cls.q)

    def to_int(self, p):
        """
        Takes a Torus element and outputs its integer representation in [0, p) using
        log2(p) bits of precision
        """
        return np.uint64(np.round(self.data / (self.q / p))) % np.uint64(p)

    def __add__(self, other):
        if isinstance(other, Torus):
            return Torus(self.data + other.data)
        else:
            raise TypeError(
                f"doesn't support addition of torus elements with {type(other)}"
            )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Torus):
            return Torus(self.data - other.data)
        else:
            raise TypeError(
                f"doesn't support subtraction of torus elements with {type(other)}"
            )

    def __rsub__(self, other):
        if isinstance(other, Torus):
            return Torus(other.data - self.data)
        else:
            raise TypeError(
                f"doesn't support subtraction of torus elements with {type(other)}"
            )

    def __mul__(self, other):
        if isinstance(other, int):
            other = np.uint64(other)
        if isinstance(other, np.uint64):
            return Torus(self.data * other)
        else:
            raise TypeError(
                f"doesn't support multiplication of torus elements with {type(other)}"
            )

    def __rmul__(self, other):
        return self.__mul__(other)
