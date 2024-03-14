from setuptools import find_packages, setup

requirements = [
    'user_identity_cqrs_contract',
]

setup(
    name='user_identity',
    version='0.0.0',
    packages=find_packages(),
    include_package_data=True,
)
