import pytest
import numpy as np
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


@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32])
def test_torus_int_encoding(log2_p):
    p = 2 ** log2_p
    for i in np.random.randint(0, p, size=10, dtype=np.uint64):
        u = Torus.from_int(i, p)
        result = u.to_int(p)
        assert result == i


@pytest.mark.parametrize("r", np.arange(0, 1, 0.1).tolist())
@pytest.mark.parametrize("log2_p", [3, 5, 8, 16, 32, 64])
def test_torus_encoding(r, log2_p):
    p = 2 ** log2_p
    u = Torus.from_real(r)
    result = u.to_real(p)
    assert equal_torus_elem(result, r)


# TODO:
# test add/sub/mul with different encodings
