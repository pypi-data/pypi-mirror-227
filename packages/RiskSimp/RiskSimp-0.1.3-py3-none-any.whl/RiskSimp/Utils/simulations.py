from RiskSimp.Objects.distributions import Distribution
import inspect
from typing import Callable
import matplotlib.ticker as mticker
import pandas as pd
import matplotlib.pyplot as plt


class Simulation(Distribution):
    def __init__(self, function: Callable, n_sim: int = 10_000):
        super().__init__()
        self.kind = "Simulation"
        self.name = function.__name__
        self.function = function
        self.n_sim = n_sim
        self.inputs = []

    def _build_generator(self):
        if len(self.inputs) > 0:
            return self.function(*tuple([x.generator() for x in self.inputs]))
        else:
            raise ValueError("Inputs must be set before running")

    def set_inputs(self, *args: Distribution):
        function_inputs = len(inspect.signature(self.function).parameters)
        inputs_recieved = len(args)
        if all(isinstance(arg, Distribution) for arg in args):
            if function_inputs == inputs_recieved:
                self.domain = args[0].domain
                for variable in args:
                    self.inputs += [variable]
                    self.params[f"param{len(self.params) + 1}"] = (str(variable))
                    if variable.domain[0] < self.domain[0]:
                        self.domain[0] = variable.domain[0]
                    if variable.domain[1] > self.domain[1]:
                        self.domain[1] = variable.domain[1]

                self.generator = self._build_generator
            else:
                raise TypeError(
                    f"{self.function.__name__}() takes exactly {function_inputs} arguments ({inputs_recieved} given) ")
        else:
            raise ValueError("Input must be an instance of the Distribution class or its subclass")

    def run(self):
        self.data = [self.generator() for _ in range(self.n_sim)]
        return self.data

    def variations_analysis(self, variation: float = 0.1, steps: int = 5):
        if len(self.data) == 0:
            self.run()

        base_values = [variable.base_value for variable in self.inputs]

        variations = [variation * i / steps - variation for i in range(steps * 2 + 1)]

        range_list = [[val * (1 + var) for var in variations] for val in base_values]

        results_matrix = []
        for i in range(len(range_list)):
            results_list = []
            for val in range_list[i]:
                params = base_values.copy()
                params[i] = val
                result = self.function(*params)
                results_list += [result]
            results_matrix += [results_list]

        if isinstance(results_matrix[0][0], tuple):
            num_outputs = len(results_matrix[0][0])

            results_per_input = [[[tup[i] for tup in tuples_list] for tuples_list in results_matrix] for i in
                                 range(num_outputs)]

        else:
            num_outputs = 1
            results_per_input = [results_matrix]

        labels = [f"{i.name}" for i in self.inputs]

        for e in range(num_outputs):
            y = results_per_input[e]
            for i in range(len(y)):
                plt.plot(variations, y[i], marker='o', label=labels[i])
                plt.legend()

            plt.title(f"Spider plot on Output {e + 1}")
            plt.xlabel("Variation")
            plt.ylabel("Output")
            plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))

            plt.grid(True)
            plt.show()

        input_table = pd.DataFrame([[lst[0], lst[-1], lst[len(lst) // 2]] for lst in range_list],
                                   columns=['Input Downside', 'Input Upside', 'Base Case Value'], index=labels)

        output_tables = [pd.DataFrame([[lst[0], lst[-1], max(lst) - min(lst)] for lst in matrix],
                                      columns=['Output Downside', 'Output Upside', 'Effective Range'], index=labels) for
                         matrix in results_per_input]

        base_case_values = self.function(*base_values)
        counter = 0

        for table in output_tables:
            df = pd.concat([table, input_table], axis=1).sort_values('Effective Range')
            print(df)
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots()

            if isinstance(base_case_values, tuple):
                base_case_value = base_case_values[counter]
            else:
                base_case_value = base_case_values

            counter += 1

            # Calculate size_dws and left_d values
            size_dws = abs((base_case_value) - (df['Output Downside']))
            left_d = df['Output Downside'].where(df['Output Downside'] <= df['Output Upside'], other=base_case_value)

            # Calculate size_ups and left_u values
            size_ups = abs((base_case_value) - (df['Output Upside']))
            left_u = df['Output Upside'].where(df['Output Downside'] > df['Output Upside'], other=base_case_value)

            bars_d = ax.barh(list(df.index), size_dws, left=left_d, color='red')

            bars_u = ax.barh(list(df.index), size_ups, left=left_u, color='blue')

            x_limits = ax.get_xlim()
            x_range = abs(x_limits[1] - x_limits[0])
            x_mid = (x_limits[1] + x_limits[0]) / 2
            x1 = x_mid - x_range / 4
            x2 = x_mid + x_range / 4

            for i, (bar_d, bar_u) in enumerate(zip(bars_d, bars_u)):
                x_d = x1 if bar_d.get_x() < base_case_value else x2
                x_u = x2 if x_d == x1 else x1
                ax.text(x_d, bar_d.get_y() + bar_d.get_height() / 2,
                        round(df['Input Downside'][i], 6),
                        va='center', ha='center', color='black', fontsize=10)

                ax.text(x_u, bar_u.get_y() + bar_u.get_height() / 2,
                        round(df['Input Upside'][i], 6),
                        va='center', ha='center', color='black', fontsize=10)

            ax.set_xlabel('Value')
            ax.set_title(f'Tornado Chart Output {counter}')
            plt.grid(True)
            plt.show()

    def complete_analisys(self, confidence:float =0.90):
        self.hist(params_show=False)
        self.variations_analysis()
        lower=.5-confidence/2
        upper = lower+confidence

        n_outputs = len(self.data[0])
        if n_outputs>1:
            rnge=self.q_range(tuple([lower]*n_outputs),tuple([upper]*n_outputs))
            l_tail=self.q(tuple([confidence]*n_outputs))
            u_tail=self.q(tuple([1-confidence]*n_outputs))
        else:
            rnge=self.q_range(lower,upper)
            l_tail=self.q(confidence)
            u_tail=self.q(1-confidence)



        print(f"With a {confidence*100}% confidence interval the output will be on this range{rnge}")
        print(f"With a {confidence * 100}% confidence interval the output will be lower than {l_tail}")
        print(f"With a {confidence * 100}% confidence interval the output will be higher than {u_tail}")
