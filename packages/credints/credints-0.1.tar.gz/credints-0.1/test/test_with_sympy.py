from credints import EqualTailIntervals
from numpy.testing import assert_almost_equal, assert_approx_equal
import nba_sympy.stats
import numpy as np


def test_sympy_normal_eti():
    ci = EqualTailIntervals(nba_sympy.stats)
    try:
        ci.normal(0.9, [2, 4])
    except:
        pass
    else:
        assert False, "calling equal_tail_intervals.normal() outside of an assignment should fail"
    credence = 0.9
    low, high = 2, 4
    x = ci.normal(credence, [low, high])
    from sympy.stats import P
    tail_weight = (1-credence)/2
    assert_almost_equal(tail_weight, P(x<low).evalf())
    assert_almost_equal(tail_weight, P(x>high).evalf())


def test_sympy_log_normal_eti():
    ci = EqualTailIntervals(nba_sympy.stats)
    try:
        ci.log_normal(0.9, [2, 4])
    except:
        pass
    else:
        assert False, "calling equal_tail_intervals.log_normal() outside of an assignment should fail"
    credence = 0.9
    low, high = 2, 4
    x = ci.log_normal(credence, [low, high])
    from sympy.stats import P
    tail_weight = 0.5*(1-credence)
    n = 100000
    from sympy.stats import sample
    xs = sample(x, size=n, seed=0)
    assert_approx_equal(tail_weight, (xs < low).mean(), significant=2)
    assert_approx_equal(tail_weight, (xs > high).mean(), significant=2)


if __name__ == "__main__":
    import pytest
    pytest.main()

