from setuptools import setup, find_packages

setup(
    name='kgf-azure-ml-model',
    version='1.0',
    author='Naresh khuriwal',
    packages=find_packages(),
    install_requires=[
        'azureml',
        'tensorflow',
    ],
)
