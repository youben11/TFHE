import pytest
import numpy as np
from tfhe.ciphertexts.trlwe import *
from tfhe.torus_polynomial import TorusPolynomial


def equal_torus_elem(t1, t2, atol=0.1):
    assert 0 <= t1 < 1
    assert 0 <= t2 < 1
    iatol = 1 - atol
    dist = abs(t1 - t2)
    if dist < atol or dist > iatol:
        return True
    else:
        return False


@pytest.mark.parametrize("r", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_trlwe_enc_dec_torus(r, big_n, sigma, k):
    p = 2 ** 16
    u = TorusPolynomial.from_real([r] * big_n, big_n)
    sk = RLWESecretKey(big_n, k)
    c = TRLWE(big_n, sigma, p, k)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_real(p)
    expected = u.to_real(p)
    assert len(result) == len(expected) == big_n
    for res, e in zip(result, expected):
        assert equal_torus_elem(res, e, atol=0.1)


@pytest.mark.parametrize("i", [0, 10, 13, 2 ** 8 - 1])
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_trlwe_enc_dec_int(i, big_n, sigma, k):
    p = 2 ** 8
    u = TorusPolynomial.from_int([i] * big_n, p, big_n)
    sk = RLWESecretKey(big_n, k)
    c = TRLWE(big_n, sigma, p, k)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_int(p)
    expected = u.to_int(p)
    assert len(result) == len(expected) == big_n
    for res, e in zip(result, expected):
        assert res == e


@pytest.mark.parametrize(
    "data_range",
    [
        (0, 2),
        (-2, 1),
        (-5.5, -4),
        (-3.1, 3.5),
        (0.2, 1.4),
    ],
)
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_tlwe_enc_dec_float(data_range, big_n, sigma, k):
    p = 2 ** 8
    f = np.random.uniform(*data_range, size=(big_n)).tolist()
    u = TorusPolynomial.from_float(f, p, data_range, big_n)
    sk = RLWESecretKey(big_n, k)
    c = TRLWE(big_n, sigma, p, k)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_float(p, data_range)
    expected = u.to_float(p, data_range)
    assert len(result) == len(expected) == big_n
    assert np.allclose(result, expected, atol=0.1)
