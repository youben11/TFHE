import pytest
import numpy as np
from tfhe.torus_polynomial import TorusPolynomial


def equal_torus_elem(t1, t2, atol=0.1, min=0, max=1):
    assert min <= t1 < max
    assert min <= t2 < max
    iatol = 1 - atol
    dist = abs(t1 - t2)
    if dist < atol or dist > iatol:
        return True
    else:
        return False


@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32])
def test_torus_polynomial_int_encoding(log2_p):
    p = 2 ** log2_p
    for i in np.random.randint(0, p, size=10, dtype=np.uint64):
        u = TorusPolynomial.from_int(i, p)
        result = u.to_int(p)[0]
        assert result == i


@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32])
@pytest.mark.parametrize("big_n", [2 ** 10, 2 ** 9, 2 ** 12])
def test_torus_polynomial_int_encoding_batched(log2_p, big_n):
    p = 2 ** log2_p
    for i in np.random.randint(0, p, size=10, dtype=np.uint64):
        u = TorusPolynomial.from_int([i] * big_n, p, big_n)
        result = u.to_int(p)
        assert len(result) == big_n
        for j in range(big_n):
            assert result[j] == i


@pytest.mark.parametrize("r", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32, 64])
def test_torus_polynomial_encoding(r, log2_p):
    p = 2 ** log2_p
    u = TorusPolynomial.from_real(r)
    result = u.to_real(p)[0]
    assert equal_torus_elem(result, r)


@pytest.mark.parametrize("r", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32, 64])
@pytest.mark.parametrize("big_n", [2 ** 10, 2 ** 9, 2 ** 12])
def test_torus_polynomial_encoding_batched(r, log2_p, big_n):
    p = 2 ** log2_p
    u = TorusPolynomial.from_real([r] * big_n, big_n)
    result = u.to_real(p)
    assert len(result) == big_n
    for i in range(big_n):
        assert equal_torus_elem(result[i], r)


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
@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32, 63])
def test_torus_polynomial_float_encoding(data_range, log2_p):
    p = 2 ** log2_p
    r = np.random.uniform(*data_range, size=(1)).item()
    u = TorusPolynomial.from_float(r, p, data_range)
    result = u.to_float(p, data_range)[0]
    precision = (data_range[1] - data_range[0]) / p
    assert np.allclose(result, r, atol=precision)


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
@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32, 63])
@pytest.mark.parametrize("big_n", [2 ** 10, 2 ** 9, 2 ** 12])
def test_torus_polynomial_float_encoding_batched(data_range, log2_p, big_n):
    p = 2 ** log2_p
    r = np.random.uniform(*data_range, size=(1)).item()
    u = TorusPolynomial.from_float([r] * big_n, p, data_range, big_n)
    result = u.to_float(p, data_range)
    precision = (data_range[1] - data_range[0]) / p
    assert len(result) == big_n
    for i in range(big_n):
        assert equal_torus_elem(result[i], r, atol=precision, min=data_range[0], max=data_range[1])


# TODO:
# test add/sub/mul with different encodings
