# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 John Hampton <pacopablo@pacopablo.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# Author: John Hampton <pacopablo@pacopablo.com>

# Stdlib Imports
import clr
clr.AddReference('VMware.Vim')
from System.Collections.Specialized import NameValueCollection
from System import Array
import VMware.Vim

# 3rd Party Imports

# Local Imports

__all__ = [
    'VimConnection',
]

class VimConnection(object):
    """vCenter connection object

    VimConnection takes a url, username, and password.  The URL is generally
    in the form of::

      https://<vcenter_or_esxi_host/sdk

    It will connect to and log into the given server with the specified
    credentials.  The password is passed in plain text so SSL should be
    used.  By default vCenter and ESXi use SSL.

    Once connected, the :py:class:`vmware.VimConnection` will populate
    the :py:attr:`vmware.VimConnection.connection` attribute.  If the
    connection fails, :py:attr:`vmware.VimConnection.connection` will be
    ``None``.

    :py:attr:`vmware.VimConnection.connection` is an instance of 
    ``VMWare.Vim.VimClient`` :term:`managed object`.  It is also an instance
    variable, so creating multiple :py:class:`vmware.VimConnection` objects
    will create multiple connections to the given vCenter or ESXi host.
    
    A :py:class:`vmware.VimConnection` object is a required parameter for
    other :py:mod:`vmware` objects.
     
    """

    def __init__(url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.connection = VMware.Vim.VimClient()
        self.connection.Connect(url)
        self.connection.Login(username, password)

    def reconnect():
        """ Reconnects the ``VMWare.Vim.VimClient`` """

        self.connection.Login(usrname, password)

    