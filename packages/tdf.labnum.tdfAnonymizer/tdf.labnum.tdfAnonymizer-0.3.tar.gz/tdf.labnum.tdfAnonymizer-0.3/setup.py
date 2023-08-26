from setuptools import setup, find_packages

setup(
    name='tdf.labnum.tdfAnonymizer',
    version='0.3',
    packages=find_packages(),
    data_files=[('.', ['villes.json'])],  # Ajoutez le chemin vers votre fichier JSON
    install_requires=[
        'nltk',
        'pydantic',
        'faker',
        'pandas'
    ],
)
