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
import sys
import os
import traceback
import argparse

# Third Party imports
from configobj import ConfigObj

# Local imports
import api
import conf
import pillage
import repair
import verify

VERSION = '1.0'

ACTIONS = ['repair', 'verify', 'pillage',]

def doArgs(argv):
    """ Configure ArgumentParser and parse command line arguments """

    global VERSION
    description = "Validate VMware configuration against a config file."
    usage = "%(prog)s [options] <config file>"

    parser = argparse.ArgumentParser(prog='vcheck.py', description=description,
                                     usage=usage)
    parser.add_argument('config', #type=file, 
                        help="Config file containing the VMware configuration")
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--username', default=None,
                        help="Username used to authenticate with vCenter")
    parser.add_argument('--password', default=None,
                        help="Password used for authentication")
    parser.add_argument('--server', default=None,
                        help="hostname or IP of vCenter or ESXi server")
    parser.add_argument('--vhost', default=None,
                        help="name of VMware host server")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--repair', '--ammend', action='store_const',
                        const="repair", dest='action', help="Correct any "
                        "discrepencies between the given condifg file and the "
                        "current config.")
    group.add_argument('--verify', action='store_const', const="verify",
                        dest='action', help="Verify the VMware config matches "
                        "that in the given config file.  Print out changes to "
                        "be made if discrepencies are found")
    group.add_argument('--retrieve', '--pillage', action='store_const',
                        const='pillage', dest='action', help="Retrieve the "
                        "current config and save it in the given config file. "
                        "If an existing file is given, it will be "
                        "overwritten,")

    opts = parser.parse_args(argv)

    #TODO: Need logic in here validating opts.config.  If option is --pillage,
    #      need to make sure we can write the file.  Otherwise, need to be
    #      verify read of file.
    return opts


def main(opts):
    config_mode = (opts.action in ACTIONS[:2]) and 'r' or 'w'
    config = conf.load_config(opts.config, config_mode)
    serviceURL = api.get_service_url(opts, config)
    username = conf.get_value(opts, config, 'username')
    password = conf.get_value(opts, config, 'password', secret=True)

    try:
        vim_client = api.connect(serviceURL, username, password)
   
        if opts.action == 'verify':
            verify.do_verify(config, opts, vim_client)
        elif opts.action == 'pillage':
            pillage.do_pillage(config, opts, vim_client)
        elif opts.action == 'repair':
            repair.do_repair(config, opts, vim_client)
        vim_client.Disconnect()
        rc = 0
    except SystemError, e:
        print(str(e.args))
        rc = 1
   
    return rc

if __name__ == '__main__':
    opts = doArgs(sys.argv[1:])
    sys.exit(main(opts))
