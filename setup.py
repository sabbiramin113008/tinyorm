

# -*- coding: utf-8 -*-

"""
author: S.M. Sabbir Amin
date: 21 Jan 2023
email: sabbir.amin@goava.com, sabbiramin.cse11ruet@gmail.com
"""
import setuptools
from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='lightorm',
    version='0.0.4',
    author='Sabbir Amin',
    author_email='sabbiramin.cse11ruet@gmail.com',
    description='Yet another, super lightweight MySQL ORM in Python.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/sabbiramin113008/tinyorm',
    packages=setuptools.find_packages(),
    install_requires=['pymysql'],
    license='MIT',
    keywords=['python', 'Database', 'ORM', 'MySQL'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ],
    zip_safe=False
)