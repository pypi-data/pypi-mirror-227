from setuptools import setup, find_packages

setup(
    name='plasmaz',
    version='0.1.0',
    description='Plasmaz is a Python API wrapper which interacts with the Python API and creates a smoother experience.',
    packages=find_packages(),
    license='MIT',
    author='TuberAsk',
    install_requires=['Python >=3.11', 'requests'],
)
