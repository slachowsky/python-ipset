#!/usr/bin/env python

"""python-ipset setup script"""

from distutils.core import setup, Extension

# build/install python-iptables
setup(
    name="python-ipset",
    version="0.0.1-dev",
    description="Python bindings for ipset",
    author="Stephan Lachowsky",
    author_email="stephan.lachowsky@gmail.com",
    url="https://github.com/slachowsky/python-ipset",
    packages=["ipset"],
)
