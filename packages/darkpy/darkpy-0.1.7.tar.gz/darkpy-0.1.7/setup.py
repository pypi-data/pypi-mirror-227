from setuptools import setup
import os

# Carregar o conteúdo do arquivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='darkpy',
    version='0.1.7',
    description='DarkPy is a Python library which brings some useful calculations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['darkpy', 'darkpy.date', 'darkpy.math'],
    install_requires=[],
)
