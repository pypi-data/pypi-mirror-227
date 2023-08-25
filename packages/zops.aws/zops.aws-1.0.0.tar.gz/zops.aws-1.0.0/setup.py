#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="zops.aws",
    use_scm_version=True,
    author="Alexandre Andrade",
    author_email="kaniabi@gmail.com",
    url="https://github.com/zerotk/zops.aws",
    description="Customized commands for AWS.",
    long_description="Customized commands for AWS.",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="development environment, shell, operations, aws",
    include_package_data=True,
    packages=["zops", "zops.aws"],
    entry_points="""
        [zops.plugins]
        main=zops.aws.cli:main
    """,
    install_requires=[
        "zerotk.lib",
        "zerotk.zops",
    ],
    dependency_links=[],
    setup_requires=["setuptools_scm"],
    tests_require=[
        "pytest",
        "datadiff",
    ],
    license="MIT license",
)
