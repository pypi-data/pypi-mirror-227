# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
# codecs is part of the standard library
from codecs import open
from os import path

# ------------------- till this line ------------------- #
# We need to do necessary imports

# The directory containing this file
HERE = path.abspath(path.dirname(__file__)) 

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="alextest-medium-multiply",
    version="0.1.0",
    description="Demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alextest-medium-multiply.readthedocs.io/",
    author="Alex Chen",
    author_email="weichen199707@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["medium_multiply"],
    include_package_data=True,
    install_requires=["numpy"]
)