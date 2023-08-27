from setuptools import setup, find_packages

setup(
    name='deepc_hunt',
    version='0.0.3',
    author='Michael Cummins',
    author_email='micummin@tcd.ie',
    url='https://github.com/michael-cummins/DeePC-HUNT',
    description='PyTorch module for DeePC',
    packages=['deepc_hunt'],
    install_requires=[
        'cvxpylayers==0.1.6',
        'torch==2.0.1',
        'matplotlib',
        'tqdm'
    ]
)