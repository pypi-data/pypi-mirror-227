import random
from RiskSimp.Objects.distributions import Distribution
from typing import Union
import math


class Discrete(Distribution):
    def __init__(self):
        super().__init__()
        self.kind = "Discrete"

    @classmethod
    def Poisson(cls, lam: Union[int, float]):
        instance = cls()
        instance.name = "Poisson"
        instance.params = {'lambda': lam}

        def poisson(lam):
            L = math.exp(-lam)
            k = 0
            p = 1
            while p > L:
                k += 1
                p *= random.random()
            return k - 1

        instance.base_value = lam
        instance.generator = lambda: poisson(lam)
        instance.domain = [0, float("inf")]
        return instance

    @classmethod
    def Uniform(cls, a: int, b: int):
        instance = cls()
        instance.name = "Uniform"
        instance.base_value = int((a + b) / 2)
        instance.params = {'min': a, 'max': b}
        instance.generator = lambda: (random.randint(a=a, b=b))
        instance.domain = [a, b]
        return instance

    @classmethod
    def Triangular(cls, min_val: int, mode: int, max_val: int):
        instance = cls()
        instance.name = "Triangular"
        instance.params = {'min': min_val, 'mode': mode, 'max': max_val}
        instance.base_value = mode
        instance.generator = lambda: int(round(random.triangular(low=min_val, high=max_val, mode=mode)))
        instance.domain = [min_val, max_val]
        return instance

    @classmethod
    def Binomial(cls, n: int, p: float):
        instance = cls()
        instance.name = "Binomial"
        instance.base_value = n * p
        instance.params = {'number of trials': n, 'success probability': p}
        instance.generator = lambda: sum(1 for _ in range(n) if random.random() < p)
        instance.domain = [0, n]
        return instance

    @classmethod
    def Bernoulli(cls, p: float, v_occurrence: Union[int, float] = 1, v_non_occurrence: Union[int, float] = 0):
        instance = cls()
        instance.name = "Bernoulli"
        instance.base_value = p
        instance.params = {'success probability': p}
        instance.generator = lambda: v_occurrence if random.random() < p else v_non_occurrence
        instance.domain = [min(v_occurrence, v_non_occurrence), max(v_occurrence, v_non_occurrence)]
        return instance

