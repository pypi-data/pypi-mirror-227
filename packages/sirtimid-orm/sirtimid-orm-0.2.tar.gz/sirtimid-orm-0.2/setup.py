from setuptools import setup, find_packages

setup(
    name='sirtimid-orm',
    version='0.2',
    packages=find_packages(),
    install_requires=['psycopg2'],
)