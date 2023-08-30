from setuptools import setup, find_packages

setup(
    name='plasmaz',
    version='0.2.0',
    description='Plasmaz is a Python GitHub API wrapper which interacts with the GitHub Python API and creates a smoother experience for developing in Python.',
    packages=find_packages(),
    license='MIT',
    author='TuberAsk',
    install_requires=['Python >=3.11', 'requests'],
)
