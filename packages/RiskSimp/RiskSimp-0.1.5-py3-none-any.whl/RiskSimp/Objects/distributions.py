from typing import Union
import matplotlib.pyplot as plt
import statistics


class Distribution:
    def __init__(self):
        self.kind = None
        self.name = None
        self.params = {}
        self.generator = lambda: 0
        self.base_value = 0
        self.data = []
        self.domain = [0, 0]

    def __str__(self):
        return f"<Distribution.{self.kind}.{self.name} params: {self.params}>"

    def generate(self, n_sim: int = 10_000):
        self.data = [self.generator() for _ in range(n_sim)]
        return self.data

    def hist(self, save: bool = False, file_name: str = "histogram.png", params_show: bool = True):

        if len(self.data) == 0:
            self.generate()

        if isinstance(self.data[0], tuple):
            sep_data = list(zip(*self.data))
        else:
            sep_data = [self.data]

        for n, data in enumerate(sep_data):
            if all(isinstance(x, int) for x in data):
                bins = len(set(data))
            else:
                # scotts rule
                h = 3.5 * statistics.stdev(data) / len(data) ** (1 / 3)
                k = (max(data) - min(data)) / h  # You can adjust this calculation as needed
                bins = int(k)

            plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)

            if len(sep_data) == 1:
                plt.title(f"Histogram {self.kind} {self.name}")
            else:
                plt.title(f"Histogram {self.kind} {self.name} {n + 1}")

            if params_show:
                for i, (param_name, param_value) in enumerate(self.params.items()):
                    plt.text(0.1, .9 - (0.05 * i), f"{param_name}: {param_value}",
                             transform=plt.gca().transAxes,
                             verticalalignment='top',  # Align text to the top
                             horizontalalignment='left',  # Align text to the left
                             fontsize=10)

            plt.xlabel("Value")
            plt.ylabel("Frequency")
            if save:
                plt.savefig(file_name + str(n))

            plt.show()

    def change_name(self, name):
        self.name = name

    def rand(self):
        return self.generator()

    def p(self, q: Union[int, float, tuple]):
        if len(self.data) == 0:
            self.generate()

        def get_prob(data: list, threshold: Union[int, float]):
            return sum([1 if i < threshold else 0 for i in data]) / len(data)

        if isinstance(q, tuple):
            if isinstance(self.data[0], tuple):
                if len(self.data[0]) == len(q):
                    sep_data = list(zip(*self.data))
                    results = []
                    for i, numbers in enumerate(sep_data):
                        results += [get_prob(list(numbers), q[i])]
                    return tuple(results)
                else:
                    raise TypeError(f"Dimentions of parameter q must match the output of the generator")
            else:
                raise TypeError(f"Dimentions of parameter q must match the output of the generator")
        else:
            if isinstance(self.data[0], Union[int, float]):
                return get_prob(self.data, q)
            else:
                raise TypeError(f"Type of parameter q must match the output of the generator")

    def q(self, p: Union[int, float, tuple]):

        def get_quant(data: list, probability: Union[int, float]):
            if probability >= 1:
                return self.domain[1]
            elif probability <= 0:
                return self.domain[0]
            else:
                return sorted(data)[int(len(data) * probability)]

        if isinstance(p, tuple):
            if isinstance(self.data[0], tuple):
                if len(self.data[0]) == len(p):
                    sep_data = list(zip(*self.data))
                    results = []
                    for i, numbers in enumerate(sep_data):
                        results += [get_quant(list(numbers), p[i])]
                    return tuple(results)
                else:
                    raise TypeError(f"Dimentions of parameter p must match the output of the generator")
            else:
                raise TypeError(f"Dimentions of parameter p must match the output of the generator")
        else:
            if isinstance(self.data[0], Union[int, float]):
                return get_quant(self.data, p)
            else:
                raise TypeError(f"Type of parameter p must match the output of the generator")

    def p_range(self, min_q: Union[int, float, tuple], max_q: Union[int, float, tuple]):

        if type(min_q) == type(max_q) or (isinstance(min_q, (int, float)) and isinstance(max_q, (int, float))):
            lower = self.p(min_q)
            upper = self.p(max_q)
            if isinstance(min_q, tuple):
                return tuple(b - a for a, b in zip(lower, upper))
            else:
                return lower - upper
        else:
            raise TypeError("types of min_q and max_q must match")

    def q_range(self, min_p: Union[int, float, tuple], max_p: Union[int, float, tuple]):
        if type(min_p) == type(max_p):
            lower = self.q(min_p)
            upper = self.q(max_p)
            if isinstance(min_p, tuple):
                return tuple([a, b] for a, b in zip(lower, upper))
            else:
                return [lower, upper]
        else:
            raise TypeError("types of min_q and max_q must match")
