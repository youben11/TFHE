import pytest
import numpy as np
from tfhe.ciphertexts.tlwe import *
from tfhe.torus import Torus


P = 2 ** 8
DATA_RANGE = (-5, 5)


@pytest.mark.parametrize("f1", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("f2", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_add_encrypted(f1, f2, n, sigma):
    off = DATA_RANGE[0]
    delta = DATA_RANGE[1] - DATA_RANGE[0]
    p = P
    u1 = Torus.from_float(f1, p, DATA_RANGE)
    u2 = Torus.from_float(f2, p, DATA_RANGE)
    correction = Torus.from_real(off / delta)
    expected = f1 + f2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 + c2 - correction
    result = c_add.decrypt(sk).to_float(p, DATA_RANGE)
    precision = (DATA_RANGE[1] - DATA_RANGE[0]) / p
    assert np.allclose(result, expected, atol=precision)


@pytest.mark.parametrize("f1", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("f2", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_add_plain(f1, f2, n, sigma):
    off = DATA_RANGE[0]
    delta = DATA_RANGE[1] - DATA_RANGE[0]
    p = P
    u1 = Torus.from_float(f1, p, DATA_RANGE)
    u2 = Torus.from_float(f2, p, DATA_RANGE)
    correction = Torus.from_real(off / delta)
    expected = f1 + f2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_add = c1 + u2 - correction
    result = c_add.decrypt(sk).to_float(p, DATA_RANGE)
    precision = (DATA_RANGE[1] - DATA_RANGE[0]) / p
    assert np.allclose(result, expected, atol=precision)


@pytest.mark.parametrize("f1", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("f2", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_sub_encrypted(f1, f2, n, sigma):
    off = DATA_RANGE[0]
    delta = DATA_RANGE[1] - DATA_RANGE[0]
    p = P
    u1 = Torus.from_float(f1, p, DATA_RANGE)
    u2 = Torus.from_float(f2, p, DATA_RANGE)
    correction = Torus.from_real(off / delta)
    expected = f1 - f2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 - c2 + correction
    result = c_add.decrypt(sk).to_float(p, DATA_RANGE)
    precision = (DATA_RANGE[1] - DATA_RANGE[0]) / p
    assert np.allclose(result, expected, atol=precision)


@pytest.mark.parametrize("f1", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("f2", [-0.5, 0.5, 0, 1, 2.2, 0.3, -0.7])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_sub_plain(f1, f2, n, sigma):
    off = DATA_RANGE[0]
    delta = DATA_RANGE[1] - DATA_RANGE[0]
    p = P
    u1 = Torus.from_float(f1, p, DATA_RANGE)
    u2 = Torus.from_float(f2, p, DATA_RANGE)
    correction = Torus.from_real(off / delta)
    expected = f1 - f2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_add = c1 - u2 + correction
    result = c_add.decrypt(sk).to_float(p, DATA_RANGE)
    precision = (DATA_RANGE[1] - DATA_RANGE[0]) / p
    assert np.allclose(result, expected, atol=precision)


@pytest.mark.parametrize("f1", [0.1, 0.3, 0.7, 1.2, -0.1, -0.3, -0.7, -1.2])
@pytest.mark.parametrize("i2", [0, 1, 2, 3])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_mul_int(f1, i2, n, sigma):
    off = DATA_RANGE[0]
    delta = DATA_RANGE[1] - DATA_RANGE[0]
    u1 = Torus.from_float(f1, P, DATA_RANGE)
    correction = Torus.from_real(off / delta)
    expected = f1 * i2
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, P)
    c1.encrypt(sk, u1)
    c_mul = c1 * i2 + correction * (i2 - 1)
    result = c_mul.decrypt(sk).to_float(P, DATA_RANGE)
    precision = (DATA_RANGE[1] - DATA_RANGE[0]) / P * i2
    assert np.allclose(result, expected, atol=precision)