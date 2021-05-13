import numpy as np
from numpy.polynomial import polynomial as poly


def _get_pmod_from_big_n(big_n=1024):
    poly_mod = [1] + [0] * (big_n - 1) + [1]
    return np.uint64(poly_mod)


def polymod(p, big_n, q=2 ** 64):
    # TODO: compute polymod using rotate and negate
    poly_mod = _get_pmod_from_big_n(big_n)
    return np.uint64(poly.polydiv(np.int64(p), poly_mod)[1])


def polymul(p1, p2, q=2 ** 64):
    # TODO: use old polu API of numpy to compute polymul with uint64
    return np.uint64([s * a for s, a in zip(p1, p2)])