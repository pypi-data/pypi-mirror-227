from setuptools import find_packages, setup

setup(
    name='bdp-contracts',
    packages=find_packages(include=["bdp_contracts"]),
    install_requires=[
        "dagster_pandas",
        "dagster",
    ],
    version='0.1.1',
    description='blef data platform data contracts manager',
    author='Christophe Blefari <hi@blef.fr>',
    license='MIT',
)
