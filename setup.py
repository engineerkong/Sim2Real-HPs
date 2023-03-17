from __future__ import with_statement
from __future__ import absolute_import
import os

import setuptools

from Sim2Real_py2 import (
    author,
    author_email,
    description,
    package_name,
    project_urls,
    url,
    version,
)
from io import open

HERE = os.path.dirname(os.path.realpath(__file__))


def read_file(filepath):
    with open(filepath, u"r", encoding=u"utf-8") as fh:
        return fh.read()


extras_require = {
    u"dev": [
        # Test
        u"pytest>=4.6",
        u"pytest-cov",
        u"pytest-xdist",
        u"pytest-timeout",
        # Others
        u"isort",
        # u"black", # black requires py3.6+
        u"pydocstyle",
        u"flake8",
        ]
}

setuptools.setup(
    name=package_name,
    author=author,
    author_email=author_email,
    description=description,
    long_description=read_file(os.path.join(HERE, u"README.md")),
    long_description_content_type=u"text/markdown",
    url=url,
    project_urls=project_urls,
    version=version,
    packages=setuptools.find_packages(exclude=[u"tests"]),
    python_requires=u">=2.7",
    install_requires=[
        u"numpy"
    ],
    extras_require=extras_require,
    test_suite=u"pytest",
    platforms=[u"Linux"],
    classifiers=[
        u"Programming Language :: Python :: 2.7",
        u"Natural Language :: English",
        u"Intended Audience :: Developers",
        u"Intended Audience :: Education",
        u"Intended Audience :: Science/Research",
        u"Topic :: Scientific/Engineering",
        u"Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
