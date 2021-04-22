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

    @classmethod
    def from_float(cls, value, p, data_range):
        """
        Takes a float number in [data_range[0], data_range[1]) and outputs a Torus object representing it
        using log2(p) bits of precision
        """
        if not isinstance(data_range, (list, tuple)):
            raise TypeError("data_range must be a tuple or list")
        if len(data_range) != 2:
            raise ValueError("data_range must be a tuple or list of length 2")
        if data_range[0] >= data_range[1]:
            raise ValueError("data_range[0] must be lower than data_range[1]")
        low = data_range[0]
        high = data_range[1]
        delta = high - low
        offset = low
        if value < low or value >= high:
            print(
                f"Warning: value {value} is not in the range [{low}, {high}), it will be converted into a float in that range => {(value - offset) % delta + offset}"
            )
        # convert to int in [0, p)
        value = float((value - offset) % delta)
        step = delta / p
        int_value = round(value / step) % p
        return Torus(int_value * (cls.q / p) % cls.q)

    def to_float(self, p, data_range):
        """
        Takes a Torus element and outputs its float representation in [data_range[0], data_range[1]) using
        log2(p) bits of precision
        """
        if not isinstance(data_range, (list, tuple)):
            raise TypeError("data_range must be a tuple or list")
        if len(data_range) != 2:
            raise ValueError("data_range must be a tuple or list of length 2")
        if data_range[0] >= data_range[1]:
            raise ValueError("data_range[0] must be lower than data_range[1]")
        low = data_range[0]
        high = data_range[1]
        delta = high - low
        offset = low
        step = delta / p
        int_value = np.uint64(np.round(self.data / (self.q / p))) % np.uint64(p)
        return int_value * step + offset

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
