from pathlib import Path
from setuptools import setup, find_packages
setup(
    name="MATES",
    version="0.1",
    packages=find_packages(),
    description='A Deep Learning-Based Model for Quantifying Transposable Elements in Single-Cell Sequencing Data.',
    author='Ruohan Wang',
    author_email='ruohan.wang4@mail.mcgill.ca',
    url='https://github.com/mcgilldinglab/MATES',
    install_requires=[l.strip() for l in
        Path('requirements.txt').read_text('utf-8').splitlines()]
)