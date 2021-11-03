from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="snek_paginator",
    version="1.0.0",
    description="Paginator for Dis-Snek Python Discord API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Toricane/snek-paginator",
    author="Toricane",
    author_email="prjwl028@gmail.com",
    license="GNU",
    packages=["snek_paginator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "dis-snek",
    ],
)
