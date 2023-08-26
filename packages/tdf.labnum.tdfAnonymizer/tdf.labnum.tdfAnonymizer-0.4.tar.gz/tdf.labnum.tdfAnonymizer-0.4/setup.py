from setuptools import setup, find_packages

setup(
    name='tdf.labnum.tdfAnonymizer',
    version='0.4',
    packages=find_packages(),
    data_files=[('tdf.labnum.tdfAnonymizer', ['villes.json'])],  # Ajoutez le chemin vers votre fichier JSON
    install_requires=[
        'nltk',
        'pydantic',
        'faker',
        'pandas'
    ],
)
