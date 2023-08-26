from setuptools import setup

setup(
    name='piprinter',
    version='0.2',
    description='A package to print the value of pi with high precision',
    author='Omar',
    packages=['piprinter'],
    install_requires=[
        'mpmath',
    ],
)