from setuptools import setup, find_packages

setup(
    name='pg_ready_engine',
    version='0.1',
    packages=find_packages(),
    install_requires=['psycopg2'],
)
