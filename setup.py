#!/usr/bin/env python
# coding=utf-8

from distutils.core import setup

setup(
    name='Indeedy',
    version='0.0.1',
    author='Pete Bachant',
    author_email='petebachant@gmail.com',
    packages=['indeedy'],
    scripts=[],
    url='https://github.com/petebachant/Indeedy.git',
    license='LICENSE',
    description='Module for automating Indeed.com job searches.',
    long_description=open('README.md').read(),
    install_requires=[]
)