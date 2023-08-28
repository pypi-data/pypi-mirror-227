from RiskSimp.Objects.distributions import Distribution
from typing import Union


class Constant(Distribution):
    def __init__(self, value: Union[int, float]):
        super().__init__()
        self.kind = "Deterministic"
        self.name = "Constant"
        self.base_value = value
        self.params = {"value": value}
        self.generator = lambda: self.params["value"]
        self.domain = [value, value]
