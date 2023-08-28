import random
from RiskSimp.Objects.distributions import Distribution
from typing import Union

class Continuous(Distribution):
    def __init__(self):
        super().__init__()
        self.kind = "Continuous"

    @classmethod
    def Uniform(cls, a: Union[int, float], b: Union[int, float]):
        instance = cls()
        instance.name = "Uniform"
        instance.params = {'min': a, 'max': b}
        instance.base_value = (b + a) / 2
        instance.generator = lambda: random.uniform(a=a, b=b)
        instance.domain = [a, b]
        return instance

    @classmethod
    def Triangular(cls, min_val: Union[int, float], mode: Union[int, float], max_val: Union[int, float]):
        instance = cls()
        instance.name = "Triangular"
        instance.params = {'min': min_val, 'mode': mode, 'max': max_val}
        instance.base_value = mode
        instance.generator = lambda: random.triangular(low=min_val, high=max_val, mode=mode)
        instance.domain = [min_val, max_val]
        return instance

    @classmethod
    def Normal(cls, mean: Union[int, float], std_dev: Union[int, float]):
        instance = cls()
        instance.name = "Normal"
        instance.params = {'mu': mean, 'sigma': std_dev}
        instance.base_value = mean
        instance.generator = lambda: random.normalvariate(mu=mean, sigma=std_dev)
        instance.domain = [-float("inf"), float("inf")]
        return instance

    @classmethod
    def Exponential(cls, scale: Union[int, float]):
        instance = cls()
        instance.name = "Exponential"
        instance.params = {'scale': scale}
        instance.base_value = scale
        instance.generator = lambda: random.expovariate(lambd=1 / scale)
        instance.domain = [0, float("inf")]
        return instance

    @classmethod
    def Beta(cls, alpha: Union[int, float], beta: Union[int, float]):
        instance = cls()
        instance.name = "Beta"
        instance.base_value = alpha / (alpha + beta)
        instance.params = {'alpha': alpha, 'beta': beta}
        instance.generator = lambda: random.betavariate(alpha=alpha, beta=beta)
        instance.domain = [0, 1]
        return instance

    @classmethod
    def Gamma(cls, shape: Union[int, float], scale: Union[int, float]):
        instance = cls()
        instance.name = "Gamma"
        instance.base_value = shape * scale
        instance.params = {'shape': shape, 'scale': scale}
        instance.generator = lambda: random.gammavariate(shape, scale)
        instance.domain = [0, float("inf")]
        return instance

    @classmethod
    def Weibull(cls, alpha: Union[int, float], beta: Union[int, float]):
        instance = cls()
        instance.name = "Weibull"
        instance.params = {'alpha': alpha, 'beta': beta}
        instance.generator = lambda: random.weibullvariate(alpha=alpha, beta=beta)
        instance.base_value = sum(instance.generate())/10_000
        instance.domain = [0, float("inf")]
        return instance

    @classmethod
    def LogNormal(cls, mean: Union[int, float], std_dev: Union[int, float]):
        instance = cls()
        instance.name = "LogNormal"
        instance.base_value = mean
        instance.params = {'mu': mean, 'sigma': std_dev}
        instance.generator = lambda: random.lognormvariate(mu=mean, sigma=std_dev)
        instance.domain = [0, float("inf")]
        return instance

