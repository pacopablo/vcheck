# -*- coding: utf-8 -*-
#
# Copyright (C) 2011, John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Standard library imports
from pprint import pprint as pretyprint

# Third Party imports

# Local imports

__all__ = ['print_config_host_types', 'pprint']

pprint = pretyprint

def print_config_host_types(config, host):
    """ Given two objects, prints the value and type.

    Example output:

    c: False (<type 'bool'>) -- h: True (<type 'bool'>)

    """

    print('c: %s (%s) -- h: %s (%s)' % (str(val), str(type(val)), str(mo_val),
          str(type(mo_val))))

