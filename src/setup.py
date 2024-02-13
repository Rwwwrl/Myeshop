from setuptools import find_packages, setup

with open('requirements/prod.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='myeshop',
    version='0.0.0',
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
)
