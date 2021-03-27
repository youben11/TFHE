import numpy as np
from tfhe.ciphertexts.ciphertext import Ciphertext
from tfhe.torus import Torus


class LWESecretKey:
    """
    Learning with error secret key. It's a vector of bits of size `n`. This same key will be used
    for encryption and decryption.
    """
    def __init__(self, n):
        self.n = n
        self.data = [np.random.randint(0, 2, dtype=np.uint64) for _ in range(n)]

    def bits(self):
        return self.data


class TLWE:
    def __init__(self, n, sigma, p):
        # we always use float64
        self.q = 2 ** 64
        self.n = n
        self.sigma = sigma
        self.p = p
        self.mask = None
        self.b = None

    @staticmethod
    def randn(sigma):
        """
        Generate a random torus element based on a normal distribution N(0, sigma ^ 2).
        """
        return Torus.from_real(np.random.randn() * sigma)

    def copy(self):
        new = TLWE(self.n, self.sigma, self.p)
        new.mask = self.mask.copy()
        new.b = self.b.copy()
        return new

    def random_mask(self):
        """
        Random mask used to encrypt a torus element. It's a vector of size `n` of random torus
        elements (uniform distribution).
        """
        return [
            Torus(t) for t in np.random.randint(0, self.q, size=self.n, dtype=np.uint64)
        ]

    def encrypt(self, sk, u):
        """
        Encrypt a torus message `u` with a secret key `sk`
        """
        self.mask = self.random_mask()
        sk_bits = sk.bits()
        assert len(self.mask) == len(sk_bits) == self.n

        encrypted_mask = sum(
            [si * ai for si, ai in zip(sk_bits, self.mask)], start=Torus(0)
        )
        e = self.randn(self.sigma)
        self.b = encrypted_mask + u + e

    def decrypt(self, sk):
        """
        Decrypt a TLWE ciphertext into a torus element
        """
        if self.mask is None:
            raise RuntimeError("nothing is encrypted")
        sk_bits = sk.bits()
        assert len(sk_bits) == len(self.mask) == self.n
        encrypted_mask = sum(
            [si * ai for si, ai in zip(sk_bits, self.mask)], start=Torus(0)
        )
        u_noisy = self.b - encrypted_mask
        # unwrapping/wrapping in Torus will just remove noise
        return Torus.from_real(u_noisy.to_real(self.p))

    def have_same_param(self, other):
        """
        Check if `self` and `other` TLWE ciphertexts have the same parameters
        """
        if not isinstance(other, TLWE):
            raise TypeError(f"can't check parameters with object of type {type(other)}")
        if self.q != other.q:
            return False
        if self.p != other.p:
            return False
        if self.n != other.n:
            return False
        return True

    def __add__(self, other):
        if isinstance(other, TLWE):
            if not self.have_same_param(other):
                raise ValueError("addition need to be done on TLWE of same parameters")
            res = self.copy()
            for i in range(len(res.mask)):
                res.mask[i] += other.mask[i]
            res.b += other.b
            return res
        elif isinstance(other, Torus):
            res = self.copy()
            res.b += other
            return res
        else:
            raise TypeError(f"don't support addition of TLWE with {type(other)}")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, TLWE):
            if not self.have_same_param(other):
                raise ValueError(
                    "subtraction need to be done on TLWE of same parameters"
                )
            res = self.copy()
            for i in range(len(res.mask)):
                res.mask[i] -= other.mask[i]
            res.b -= other.b
            return res
        elif isinstance(other, Torus):
            res = self.copy()
            res.b -= other
            return res
        else:
            raise TypeError(f"don't support addition of TLWE with {type(other)}")

    def __rsub__(self, other):
        # TODO: negate first maybe?
        pass

    def __mul__(self, other):
        if isinstance(other, int):
            res = self.copy()
            res.b = self.b * other
            for i in range(len(res.mask)):
                res.mask[i] *= other
            return res
        else:
            raise TypeError(f"don't support multiplication of TLWE with {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)
