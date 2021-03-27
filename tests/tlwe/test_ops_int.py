import pytest
import numpy as np
from tfhe.ciphertexts.tlwe import *
from tfhe.torus import Torus


P = 2 ** 8


@pytest.mark.parametrize("i1", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("i2", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_add_encrypted(i1, i2, n, sigma):
    p = P
    u1 = Torus.from_int(i1, p)
    u2 = Torus.from_int(i2, p)
    expected = (i1 + i2) % p
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 + c2
    result = c_add.decrypt(sk).to_int(p)
    assert result == expected


@pytest.mark.parametrize("i1", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("i2", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_add_plain(i1, i2, n, sigma):
    p = P
    u1 = Torus.from_int(i1, p)
    u2 = Torus.from_int(i2, p)
    expected = (i1 + i2) % p
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_add = c1 + u2
    result = c_add.decrypt(sk).to_int(p)
    assert result == expected


@pytest.mark.parametrize("i1", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("i2", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_sub_encrypted(i1, i2, n, sigma):
    p = P
    u1 = Torus.from_int(i1, p)
    u2 = Torus.from_int(i2, p)
    expected = (i1 - i2) % p
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c2 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c2.encrypt(sk, u2)
    c_add = c1 - c2
    result = c_add.decrypt(sk).to_int(p)
    assert result == expected


@pytest.mark.parametrize("i1", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("i2", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -50])
def test_tlwe_sub_plain(i1, i2, n, sigma):
    p = P
    u1 = Torus.from_int(i1, p)
    u2 = Torus.from_int(i2, p)
    expected = (i1 - i2) % p
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, p)
    c1.encrypt(sk, u1)
    c_add = c1 - u2
    result = c_add.decrypt(sk).to_int(p)
    assert result == expected


@pytest.mark.parametrize("i1", [0, 3, 5, 8, 13, 17, P - 1])
@pytest.mark.parametrize("i2", [0, 1, 2, 3, 10])
@pytest.mark.parametrize("n", [600, 800, 1024, 2048])
@pytest.mark.parametrize("sigma", [2 ** -15, 2 ** -30])
def test_tlwe_mul_int(i1, i2, n, sigma):
    u1 = Torus.from_int(i1, P)
    expected = (i1 * i2) % P
    sk = LWESecretKey(n)
    c1 = TLWE(n, sigma, P)
    c1.encrypt(sk, u1)
    c_mul = c1 * i2
    result = c_mul.decrypt(sk).to_int(P)
    assert result == expected