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

# Third Party imports
from configobj import ConfigObj
from validate import Validator, ValidateError

# Local imports
from ipgetpass import getpass

__all__ = ['load_config', 'get_value']

configspec = """
[vswitch]
[[__many__]]
___many___ = voption('string')
Spec.Policy.NicTeaming.Policy = voption('string(default="loadbalance_srcid")')
Spec.Policy.Security.MacChanges = voption('boolean(default=None)')
Spec.NumPorts = voption('integer(default=None)')
Spec.Mtu = voption('integer(default=None)')
Name = voption('string')
Spec.Policy.NicTeaming.NicOrder.StandbyNic = voption('string(default=None)')
Spec.Policy.NicTeaming.NicOrder.ActiveNic = voption('string_list')
Spec.Policy.Security.AllowPromiscuous = voption('boolean(default=None)')
Spec.Policy.Security.ForgedTransmits = voption('boolean(default=None)')

[portgroup]
[[__many__]]
___many___ = voption('string')
Spec.VswitchName = voption('string')
Spec.Policy.Security.MacChanges = voption('boolean(default=None)')
Spec.VlanId = voption('integer')
Spec.Policy.Security.AllowPromiscuous = voption('boolean(default=None)')
Spec.Policy.Security.ForgedTransmits = voption('boolean(default=None)')
Spec.Name = voption('string')
_vnic._type.faultToleranceLogging = voption('boolean(default=False)')
_vnic._type.vmotion = voption('boolean(default=False)')
_vnic._type.management = voption('boolean(default=False)')
_vnic.Spec.Mtu = voption('integer(default=None)')
_vnic.Spec.TsoEnabled = voption('boolean(default=False)')
_vnic.Spec.Ip.Dhcp = voption('boolean(default=False)')

"""

validator = Validator()

def voption(value, options):
    if value == 'None':
        return None
    return validator.check(options, value)

validator.functions['voption'] = voption

def load_config(config_file, config_mode='r'):
    """ Read the config file from disk using ConfigObj. """

    create_empty = (config_mode == 'w')
    file_error = not create_empty
    config = ConfigObj(infile=config_file,  list_values=True,
                       create_empty=create_empty, file_error=file_error,
                       configspec=configspec.split('\n'), stringify=True)

    config.validate(validator)
    return config


def get_value(opts, config, valkey, secret=False, prompt=True):
    """ Return the value of the given configuration key

    The config value can be specified one of 3 ways:

    - On the command line via use of the ``<value>`` option.
    - In the config file via ``<value>`` key in the ``[global]`` section
    - Via prompt in the shell.  If ``<value>`` can not be found in the config or
      or on the command line, the program will prompt for input.

    :param opts: argparse.Namespace instance holding the command line parameters
    :param config: configobj.ConfigObj instance holding the parsed config file
    :param valkey: the name of the configuration key for which a value should be
                   found
    :type valkey: str
    :param secret: if True, input typed at the prompt will not be echoed.
    :type secret: boolean
    :param prompt: if False, the user will not be prompted for the value if it is
                   not specified otherwise.
    :type prompt: boolean
    :rtype str:

    """

    gconfig = config['global']
    value = (valkey in gconfig) and gconfig[valkey] or None
    value = getattr(opts, valkey, None) or value
    if prompt:
        getinput = secret and getpass or raw_input
        value = value or getinput('Enter %s: ' % valkey)

    return value
