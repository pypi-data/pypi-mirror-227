# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 20:04:21 2023

@author: JL
"""

from setuptools import setup, find_packages

setup(
    name="HMC_pypi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
    ],

    author="Durant_Johnson57",
    author_email="zjbj2030@163.com",
    description="A short description of your awesome package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/yourusername/my-awesome-package",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)