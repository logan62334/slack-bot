#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################
# File Name: setup.py
# Author: mafei
# Mail: logan62334@gmail.com
# Created Time:  2017-06-26 01:25:34 AM
#############################################

from setuptools import setup, find_packages

import jarvis

setup(
    name="jarvis",
    version=jarvis.__version__,
    description="jarvis",
    long_description=open("README.rst").read(),
    license="MIT Licence",

    author="mafei",
    author_email="logan62334@gmail.com",
    url="https://github.com/logan62334/slack-bot.git",

    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    platforms="any",
    install_requires=["click", "shutit", "slackclient"],
    entry_points={
        'console_scripts': [
            'jarvis = jarvis.cli:main'
        ]
    },
)
