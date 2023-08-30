from credints import EqualTailIntervals
from numpy.testing import assert_almost_equal, assert_approx_equal
import nba_pymc
import numpy as np


def check_tails(model, var_name, credence, low, high, n=1000000):
    tail_weight = 0.5*(1-credence)
    data = nba_pymc.sample_prior_predictive(samples=n, model=model, var_names=[var_name], random_seed=0)
    xs = getattr(data.prior, var_name).values
    assert_approx_equal((xs < low).mean() / tail_weight, 1, significant=2)
    assert_approx_equal((xs > high).mean() / tail_weight, 1, significant=2)


def test_pymc_normal_eti():
    with nba_pymc.Model() as model:
        ci = EqualTailIntervals(nba_pymc)
        credence = 0.9
        low, high = 2, 4
        try:
            ci.normal(credence, [low, high])
        except:
            pass
        else:
            assert False, "calling equal_tail_intervals.normal() outside of an assignment should fail"
        x = ci.normal(credence, [low, high])
    check_tails(model, 'x', credence, low, high)


def test_pymc_log_normal_eti():
    with nba_pymc.Model() as model:
        ci = EqualTailIntervals(nba_pymc)
        credence = 0.9
        low, high = 2, 4
        try:
            ci.log_normal(credence, [low, high])
        except:
            pass
        else:
            assert False, "calling equal_tail_intervals.log_normal() outside of an assignment should fail"
        x = ci.log_normal(credence, [low, high])
    check_tails(model, 'x', credence, low, high)


if __name__ == "__main__":
    import pytest
    pytest.main()

