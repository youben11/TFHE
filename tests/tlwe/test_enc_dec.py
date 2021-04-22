import pytest
import numpy as np
from tfhe.ciphertexts.tlwe import *
from tfhe.torus import Torus


def equal_torus_elem(t1, t2, atol=0.1):
    assert 0 <= t1 < 1
    assert 0 <= t2 < 1
    iatol = 1 - atol
    dist = abs(t1 - t2)
    if dist < atol or dist > iatol:
        return True
    else:
        return False


@pytest.mark.parametrize("u", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_enc_dec_torus(u, n, sigma):
    p = 2 ** 16
    u = Torus.from_real(u)
    sk = LWESecretKey(n)
    c = TLWE(n, sigma, p)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, u.to_real(p), atol=0.1)


@pytest.mark.parametrize("i", [0, 10, 13, 2 ** 8 - 1])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_enc_dec_int(i, n, sigma):
    p = 2 ** 8
    u = Torus.from_int(i, p)
    sk = LWESecretKey(n)
    c = TLWE(n, sigma, p)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_int(p)
    assert result == i


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
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_enc_dec_float(data_range, n, sigma):
    p = 2 ** 8
    f = np.random.uniform(*data_range, size=(1)).item()
    u = Torus.from_float(f, p, data_range)
    sk = LWESecretKey(n)
    c = TLWE(n, sigma, p)
    c.encrypt(sk, u)
    result = c.decrypt(sk).to_float(p, data_range)
    precision = (data_range[1] - data_range[0]) / p
    assert np.allclose(result, f, atol=precision)
