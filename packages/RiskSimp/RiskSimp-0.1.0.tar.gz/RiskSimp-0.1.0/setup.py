from setuptools import setup, find_packages
from RiskSimp import __version__


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='RiskSimp',
    version=__version__,
    packages=find_packages(),
    description='RiskSimp is a versatile Python library designed to streamline the management and manipulation of '
                'random variables to empower analysts to effortlessly integrate random '
                'distributions into their processes, facilitating non-deterministic analysis ',
    author='Fabio Sol',
    author_email='fabioso2231@gmail.com',
    url='https://github.com/FabioSol/RiskSimp.git',
    license='MIT',
    install_requires=requirements,
)