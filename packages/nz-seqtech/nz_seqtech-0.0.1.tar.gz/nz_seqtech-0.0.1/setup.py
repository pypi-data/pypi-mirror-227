
import setuptools
from setuptools import setup, find_packages

with open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='nz_seqtech',
    version='0.0.1',
    license='Apache',
    description='A library for DNA sequence encoding in quantum machine learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url ='https://nz-seqtech.com/',
    author='Nouhaila Innan and Muhammad Al-Zafar Khan',
    author_email='nouhaila.innan@zaiku.com, muhammad.khan@zaikugroup.com',
    packages=find_packages(),
    install_requires=[
    'wheel',    
    'numpy',
    'pandas',
    'scikit-learn',
    'qiskit',
    'matplotlib'      
    ],
)
