from nbag import construct
import scipy.stats 
from typing import Optional
import numpy as np
from dataclasses import dataclass


def normal_params_from_eti(credence: float, low: float, high: float) -> tuple[float, float]:
    mean = (low+high)/2
    assert low < high
    assert 0 < credence < 1, 'credence must be strictly between 0 and 1'
    
    stdnorm = scipy.stats.norm(0,1)
    z = stdnorm.ppf(0.5 + credence/2)
    stdev = (high - low) / (2 * z)
    return mean, stdev


@dataclass
class EqualTailIntervals:
    backend: object

    def normal(self, credence: float, bounds: list[float], name:Optional[str]=None): 
        """
        Returns a normal RandomSymbol that falls within <bounds> at probability <credence>, and has
        equal probability of being higher than bounds[1] as it does of being lower than bounds[0].
        """
        low, high = bounds
        mean, stdev = normal_params_from_eti(credence, low, high)
        return construct(self.backend.Normal, name, mean, stdev)


    def log_normal(self, credence: float, bounds: list[float], name:Optional[str]=None): 
        """
        Returns a log-normal RandomSymbol that falls within <bounds> at probability <credence>, and has
        equal probability of being higher than bounds[1] as it does of being lower than bounds[0].
        """
        low, high = bounds
        mean, stdev = normal_params_from_eti(credence, np.log(low), np.log(high)) 
        return construct(self.backend.LogNormal, name, mean, stdev)


