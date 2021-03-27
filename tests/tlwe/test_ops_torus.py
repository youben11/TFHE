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


@pytest.mark.parametrize("u1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("u2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_add_encrypted(u1, u2, n, sigma):
    u1 = Torus.from_real(u1)
    u2 = Torus.from_real(u2)
    expected = u1 + u2
    sk = LWESecretKey(n)
    p = 2 ** 16
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 + c2
    result = c_add.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, expected.to_real(p), atol=0.1)


@pytest.mark.parametrize("u1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("u2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_add_plain(u1, u2, n, sigma):
    u1 = Torus.from_real(u1)
    u2 = Torus.from_real(u2)
    expected = u1 + u2
    sk = LWESecretKey(n)
    p = 2 ** 16
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_add = c1 + u2
    result = c_add.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, expected.to_real(p), atol=0.1)


@pytest.mark.parametrize("u1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("u2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_sub_encrypted(u1, u2, n, sigma):
    u1 = Torus.from_real(u1)
    u2 = Torus.from_real(u2)
    expected = u1 - u2
    sk = LWESecretKey(n)
    p = 2 ** 16
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_sub = c1 - c2
    result = c_sub.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, expected.to_real(p), atol=0.1)


@pytest.mark.parametrize("u1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("u2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_sub_plain(u1, u2, n, sigma):
    u1 = Torus.from_real(u1)
    u2 = Torus.from_real(u2)
    expected = u1 - u2
    sk = LWESecretKey(n)
    p = 2 ** 16
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_sub = c1 - u2
    result = c_sub.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, expected.to_real(p), atol=0.1)


@pytest.mark.parametrize("u1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("i2", [0, 1, 2, 3, 10])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_mul_int(u1, i2, n, sigma):
    p = 2 ** 16
    u1 = Torus.from_real(u1)
    expected = u1 * i2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_mul = c1 * i2
    result = c_mul.decrypt(sk).to_real(p)
    assert equal_torus_elem(result, expected.to_real(p), atol=0.1)