from setuptools import find_packages, setup

requirements = [
    'user_identity_cqrs_contract',
    'bakset_cqrs_contract',
]

setup(
    name='api_gateway',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
)
