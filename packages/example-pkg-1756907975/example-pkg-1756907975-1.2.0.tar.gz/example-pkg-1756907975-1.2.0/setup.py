#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: ChenBaoyu
# Mail: 1756907975@qq.com
# Created Time:  2023-08-25 12:27:34
# I just want to test
#############################################

import setuptools

setuptools.setup(
    name="example-pkg-1756907975",
    version="1.2.0",
    author="Example Author",
    author_email="1756907975@qq.com",
    description="A small example package",
    long_description='None',
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),

    package_data={'': [r'D:\pycod\pythonProject1\pg_message\libffi_test.dll']},


    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

