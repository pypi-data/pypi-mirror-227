from setuptools import setup, find_packages
from RiskSimp import __version__

print(find_packages())

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

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
