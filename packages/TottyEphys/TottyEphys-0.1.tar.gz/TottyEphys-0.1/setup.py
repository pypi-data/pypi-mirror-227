from setuptools import setup, find_packages

setup(
    name="TottyEphys",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        'quantities',
        'xarray',
        'elephant',
        'tqdm',
        'pynapple',
        'pyprojroot'
        ],
    author="Michael Totty",
    author_email="mictott@gmail.com",
    description="A package containing helper functions for in vivo ephys data analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mictott/TottyEphys",
)
