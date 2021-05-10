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


@pytest.mark.parametrize("r1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("r2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_trlwe_add_encrypted(r1, r2, big_n, k, sigma):
    p = 2 ** 16
    u1 = TorusPolynomial.from_real([r1] * big_n, big_n)
    u2 = TorusPolynomial.from_real([r2] * big_n, big_n)
    expected = (u1 + u2).to_real(p)
    sk = RLWESecretKey(big_n, k)
    c1 = TRLWE(big_n, sigma, p, k)
    c2 = TRLWE(big_n, sigma, p, k)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 + c2
    result = c_add.decrypt(sk).to_real(p)
    assert len(result) == len(expected) == big_n
    for r, e in zip(result, expected):
        assert equal_torus_elem(r, e, atol=0.1)


@pytest.mark.parametrize("r1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("r2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_trlwe_add_plain(r1, r2, big_n, k, sigma):
    p = 2 ** 16
    u1 = TorusPolynomial.from_real([r1] * big_n, big_n)
    u2 = TorusPolynomial.from_real([r2] * big_n, big_n)
    expected = (u1 + u2).to_real(p)
    sk = RLWESecretKey(big_n, k)
    c1 = TRLWE(big_n, sigma, p, k)
    c1.encrypt(sk, u1)
    c_add = c1 + u2
    result = c_add.decrypt(sk).to_real(p)
    assert len(result) == len(expected) == big_n
    for r, e in zip(result, expected):
        assert equal_torus_elem(r, e, atol=0.1)


@pytest.mark.parametrize("r1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("r2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_trlwe_sub_encrypted(r1, r2, big_n, k, sigma):
    p = 2 ** 16
    u1 = TorusPolynomial.from_real([r1] * big_n, big_n)
    u2 = TorusPolynomial.from_real([r2] * big_n, big_n)
    expected = (u1 - u2).to_real(p)
    sk = RLWESecretKey(big_n, k)
    c1 = TRLWE(big_n, sigma, p, k)
    c2 = TRLWE(big_n, sigma, p, k)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_sub = c1 - c2
    result = c_sub.decrypt(sk).to_real(p)
    assert len(result) == len(expected) == big_n
    for r, e in zip(result, expected):
        assert equal_torus_elem(r, e, atol=0.1)


@pytest.mark.parametrize("r1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("r2", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_trlwe_sub_plain(r1, r2, big_n, k, sigma):
    p = 2 ** 16
    u1 = TorusPolynomial.from_real([r1] * big_n, big_n)
    u2 = TorusPolynomial.from_real([r2] * big_n, big_n)
    expected = (u1 - u2).to_real(p)
    sk = RLWESecretKey(big_n, k)
    c1 = TRLWE(big_n, sigma, p, k)
    c1.encrypt(sk, u1)
    c_sub = c1 - u2
    result = c_sub.decrypt(sk).to_real(p)
    assert len(result) == len(expected) == big_n
    for r, e in zip(result, expected):
        assert equal_torus_elem(r, e, atol=0.1)


@pytest.mark.parametrize("r1", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("i2", [0, 1, 2, 3, 10])
@pytest.mark.parametrize("big_n", [1024, 2048])
@pytest.mark.parametrize("k", [1, 2, 3])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_trlwe_mul_int(r1, i2, big_n, k, sigma):
    p = 2 ** 16
    u1 = TorusPolynomial.from_real([r1] * big_n, big_n)
    expected = (u1 * i2).to_real(p)
    sk = RLWESecretKey(big_n, k)
    c1 = TRLWE(big_n, sigma, p, k)
    c1.encrypt(sk, u1)
    c_mul = c1 * i2
    result = c_mul.decrypt(sk).to_real(p)
    assert len(result) == len(expected) == big_n
    for r, e in zip(result, expected):
        assert equal_torus_elem(r, e, atol=0.1)