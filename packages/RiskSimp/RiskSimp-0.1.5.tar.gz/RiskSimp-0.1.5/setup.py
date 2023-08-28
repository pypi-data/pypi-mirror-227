from setuptools import setup, find_packages
from RiskSimp import __version__

print(find_packages())

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description ='''
# RiskSimp: Simplifying Random Variables and Simulation in Python

**Version: 0.1.5**

RiskSimp is a versatile Python library designed to streamline the management and manipulation of random variables, empowering analysts to effortlessly integrate random distributions into their processes and facilitate non-deterministic analysis.

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Modules](#modules)
    -   [Objects](#objects)
    -   [Utils](#utils)
    -   [Variables](#variables)
        -   [Continuous](#continuous)
        -   [Discrete](#discrete)
        -   [Constant](#constant)
-   [Example](#example)
-   [License](#license)

## Installation {#installation}

You can install RiskSimp using pip:

``` bash
pip install RiskSimp
```

## Usage {#usage}

Import the required modules and classes from RiskSimp:

``` python
from RiskSimp import Continuous, Discrete, Constant, Simulation
```

## Modules {#modules}

### Objects {#objects}

In the "objects" module, you'll find the base classes used throughout the library.

### Utils {#utils}

The "utils" module contains classes to simulate processes with random variables.

### Variables {#variables}

The "variables" module houses various classes for different types of random variables.

#### Continuous {#continuous}

-   Uniform(cls, a: Union[int, float], b: Union[int, float])
-   Triangular(cls, min_val: Union[int, float], mode: Union[int, float], max_val: Union[int, float])
-   Normal(cls, mean: Union[int, float], std_dev: Union[int, float])
-   Exponential(cls, scale: Union[int, float])
-   Beta(cls, alpha: Union[int, float], beta: Union[int, float])
-   Gamma(cls, shape: Union[int, float], scale: Union[int, float])
-   Weibull(cls, alpha: Union[int, float], beta: Union[int, float])
-   LogNormal(cls, mean: Union[int, float], std_dev: Union[int, float])

#### Discrete {#discrete}

-   Poisson(cls, lam: Union[int, float])
-   Uniform(cls, a: int, b: int)
-   Triangular(cls, min_val: int, mode: int, max_val: int)
-   Binomial(cls, n: int, p: float)
-   Bernoulli(cls, p: float, v_occurrence: Union[int, float] = 1, v_non_occurrence: Union[int, float] = 0)

#### Constant {#constant}

-   Constant(subclass of Distribution): Represents a non-random constant value.

## Example {#example}

``` python
from RiskSimp import *
import numpy_financial as npf


def restaurante(adecuacion,
                costo_fijo,
                costo_variable,
                inflacion,
                precio_cerveza,
                precio_alitas,
                afluencia_anual,
                variacion_demanda,
                tasa_de_comparacion,
                tasa_descuento):
    years = 11
    adec = [0] * years
    adec[0] = adecuacion
    c_fijo = [costo_fijo * (1 + inflacion) ** i for i in range(years)]
    demanda = [0] + [round(afluencia_anual * (1 + variacion_demanda) ** i) for i in range(years - 1)]
    p_cerveza = [0] + [precio_cerveza * (1 + inflacion) ** i for i in range(years - 1)]
    p_alitas = [0] + [precio_alitas * (1 + inflacion) ** i for i in range(years - 1)]
    ingreso_cerveza = [p * d for p, d in zip(p_cerveza, demanda)]
    ingreso_alitas = [p * d for p, d in zip(p_alitas, demanda)]
    ingreso = [c + a for c, a in zip(ingreso_cerveza, ingreso_alitas)]
    c_variable = [i * costo_variable for i in ingreso]

    flujo = [ing - fij - var - inv for ing, fij, var, inv in zip(ingreso, c_fijo, c_variable, adec)]
    return npf.npv(tasa_descuento, [0] + flujo), npf.irr(flujo)



adecuacion = Constant(1_500_000_000)
adecuacion.change_name("adecuacion")
costo_fijo = Constant(5_000_000)
costo_fijo.change_name("costo_fijo")
costo_variable = Continuous.Uniform(.01, .04)
costo_variable.change_name("costo_variable")
inflacion = Continuous.Normal(.047, 0.002)
inflacion.change_name("inflacion")
precio_cerveza = Continuous.Triangular(12_000, 13_500, 15_000)
precio_cerveza.change_name("precio_cerveza")
precio_alitas = Continuous.Uniform(25_000, 30_000)
precio_alitas.change_name("precio_alitas")
afluencia_anual = Continuous.Triangular(4000, 6000, 8000)
afluencia_anual.change_name("afluencia_anual")
variacion_demanda = Continuous.Uniform(0.02, 0.04)
variacion_demanda.change_name("variacion_demanda")
tasa_de_comparacion = Constant(0.14)
tasa_de_comparacion.change_name("tasa_de_comparacion")
tasa_descuento = Constant(0.1522)
tasa_descuento.change_name("tasa_descuento")

sim = Simulation(restaurante)
sim.set_inputs(adecuacion,
               costo_fijo,
               costo_variable,
               inflacion,
               precio_cerveza,
               precio_alitas,
               afluencia_anual,
               variacion_demanda,
               tasa_de_comparacion,
               tasa_descuento)

sim.complete_analisys()
```

Output:

-   histogram for output 1
-   histogram for output 2

-   spider plot for output 1
-   spider plot for output 2

-   inputs table for output 1
-   outputs table for output 1
-   Tornado chart for output 1

-   inputs table for output 2
-   outputs table for output 2
-   Tornado chart for output 2

-   range of 90% confidence
-   lower tail 90% confidence
-   upper tail 90% confidence

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

'''

setup(
    name='RiskSimp',
    version=__version__,
    packages=find_packages(),
    description='RiskSimp is a versatile Python library designed to streamline the management and manipulation of '
                'random variables to empower analysts to effortlessly integrate random '
                'distributions into their processes, facilitating non-deterministic analysis ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fabio Sol',
    author_email='fabioso2231@gmail.com',
    url='https://github.com/FabioSol/RiskSimp.git',
    license='MIT',
    install_requires=requirements,
)
