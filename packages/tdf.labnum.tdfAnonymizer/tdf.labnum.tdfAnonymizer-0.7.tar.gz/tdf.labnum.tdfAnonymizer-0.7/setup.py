from setuptools import setup, find_packages

setup(
    name='tdf.labnum.tdfAnonymizer',
    version='0.7',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'pydantic',
        'faker',
        'pandas',
        'requests',
        'random'
    ],
)
