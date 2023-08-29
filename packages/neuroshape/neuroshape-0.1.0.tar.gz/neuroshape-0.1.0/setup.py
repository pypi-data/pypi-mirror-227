'''
    setup.py file for neuroshape module
'''

from setuptools import setup, find_packages
import numpy

# run the setup
setup(name='neuroshape',
      version='0.1.0',
      description="For computing connectopic and geometric Laplacian eigenmodes and performing null hypothesis testing. As implementation is ongoing, this description is subject to rapid change.",
      author='Nikitas C. Koussis, Systems Neuroscience Group Newcastle',
      author_email='nikitas.koussis@gmail.com',
      url='https://github.com/nikitas-k/neuroshape-dev',
      packages=find_packages())
