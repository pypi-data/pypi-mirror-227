import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.0'
PACKAGE_NAME = 'manuelharo'
AUTHOR = 'manuel'
AUTHOR_EMAIL = 'manuel.haro@amplia.es'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'DESCRIPCIÓN CORTA EXPLICANDO LA LIBRERÍA'

INSTALL_REQUIRES = [
    'pandas',
    'requests'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)