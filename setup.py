#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

# VARS
version = '0.1'

# Get the long description from the README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Get requirements
with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

setup(
    name="mermaid_reshuffle",
    author="DeadLockStarve",
    author_email="deadlockstarve@disroot.org",
    url="https://github.com/DeadLockStarve/mermaid_reshuffle",
    version="0.1",
    description="Mermaid simple reshuffler",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    license="CreativeCommons",
    python_requires=">=3.5, <4",
    scripts=['mermaid_reshuffle.py'],
    install_requires=requires
)
