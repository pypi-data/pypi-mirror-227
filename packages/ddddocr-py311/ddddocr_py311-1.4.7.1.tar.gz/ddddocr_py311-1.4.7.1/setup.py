#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/2 15:41
# @Author  : sml2h3
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ddddocr_py311",
    version="1.4.7.1",
    author="dragons96",
    description="带带弟弟OCR py3.11版本",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dragons96/ddddocr",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'onnxruntime', 'Pillow', 'opencv-python-headless'],
    python_requires='<3.12',
    include_package_data=True,
    install_package_data=True,
)
