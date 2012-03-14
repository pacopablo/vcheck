# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

from distutils.core import setup

setup(
    name='vCheck',
    version='1.0.0',
    packages=['vmware'],
    author='John Hampton',
    description='Dustbowl',
    scripts=['scripts/vcheck'],
    url='http://pacopablo.github.com/vcheck',
    license='MIT',
)
