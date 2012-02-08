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
import clr
clr.AddReference('VMware.Vim')
from System.Collections.Specialized import NameValueCollection
from System import Array
import VMware.Vim

# Third Party imports

# Local imports
import conf

__all__ = ['connect', 'create_filter', 'get_host', 'get_hosts',
           'get_service_url',]

def connect(serviceURL, username, password):
    """ Connect and login to VMware vCenter or ESXi server

    :param serviceURL: serviceURL for vCenter or ESXi server.  Generally this
                       is: https://hostname/sdk
    :param username: username for authentication
    :param password: password for authentication
    :return: Returns a ``VimClient`` object that is connected and logged into
             the specified server.
    :rtype VimCLient:

    """

    client = VMware.Vim.VimClient()
    client.Connect(serviceURL)
    client.Login(username, password)
    return client


def create_filter(key, value):
    """ Return a NameValueCollection with the given key/value pair.

    If value is None, then return None

    """

    collection = NameValueCollection()
    collection.Add(key, value)
    if value:
        return collection
    else:
        return None

def get_host(client, vhost):
    """ Get the managed entity pertaining to the given host.

    If ``vhost`` is None, get the first host returned by FindEntityView.

    """

    f = create_filter('Name', vhost)
    return client.FindEntityView(VMware.Vim.HostSystem, None, f, None)


def get_hosts(client, vhost):
    """ Get the managed entity pertaining to the given hosts.

    If ``vhost`` is None, return all hosts from FindEntityViews

    """

    f = create_filter('Name', vhost)
    return client.FindEntityViews(VMware.Vim.HostSystem, None, f, None)


def get_service_url(opts, config):
    """ Return the service url for the vSphere SDK """

    protocol  = path = ''
    server = conf.get_value(opts, config, 'server')
    if not server.startswith('http'):
        protocol = 'https://'
    if server.split('/')[-1] != 'sdk':
        path = '/sdk'
    return ''.join([protocol, server, path])


def get_network_system(host, client):
    """ Return the ``NetworkSystem`` managed object """

    return client.GetView(host.ConfigManager.NetworkSystem, None)


def get_vnic_manager(host, client):
    """ Return the ``VirtualNicManger`` managed object """

    return client.GetView(host.ConfigManager.VirtualNicManager, None)

def get_mo_attr(mo, attr):
    """ Retreive the specified attribute from the managed object

    The method will convert a .NET Array object to a python list

    """

    attr_list = attr.split('.')
    m = mo
    for a in attr_list:
        m = getattr(m, a)
        continue
    if isinstance(m, Array):
        m = [n for n in m]
    return m

