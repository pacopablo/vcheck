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

# Local imports
import api
import conf
import pillage

__all__ = ['do_verify']


def compare_attribute(mo, attrib, val, indent=''):
    """ Compare the attribute on the ``mo`` to the ``val`` given.

    If ``val`` and the mo attribute are lists, sort the lsit and then compare.
    Print out difference if found and return False.  Return True otherwise
    """
    line = ''
    mo_val = api.get_mo_attr(mo, attrib)
    if isinstance(mo_val, list) and isinstance(val, list):
        mo_val.sort()
        val.sort()
    if mo_val != val:
        line = "%s%s %s: %s (config: %s)" % \
                        (indent, indent, attrib, str(mo_val), str(val))
    return line


def verify_vswitches(hconfig, config, indent='  '):
    """ Check the vCenter / ESXi server against the config file.

    If any discrepencies are found, they will be printed to the console.

    """
    print("Checking Vswitches ... ")
    host_vswitches = {}
    for vswitch in hconfig.Network.Vswitch:
        host_vswitches[vswitch.Name] = vswitch
        continue
    host_keys = set(host_vswitches.keys())
    conf_keys = set(config['vswitch'].keys())
    missing_from_host = conf_keys.difference(host_keys)
    missing_from_conf = host_keys.difference(conf_keys)
    for v in missing_from_host:
        print(indent + 'Vwsitches existing in the config, but not on the host:')
        print(indent + indent + v)
        continue
    for v in missing_from_conf:
        print(indent + 'Vwsitches existing on the host, but not in the config:')
        print(indent + indent + v)
        continue

    for vkey in conf_keys.intersection(host_keys):
        section = indent + '[' + vkey + ']'
        lines = []
        for k, v in config['vswitch'][vkey].items():
            if not k.startswith('_'):
                l = compare_attribute(host_vswitches[vkey], k, v, indent)
                if l:
                    lines.append(l)
            continue
        if lines:
            print(section)
            print('\n'.join(lines))
        continue


def verify_portgroups(hconfig, config, indent='  '):
    """ Check the vCenter / ESXi server against the config file.

    If any discrepencies are found, they will be printed to the console.

    """
    print("Checking Portgroups ... ")
    # Find portgroup differences between host and config
    host_portgroups = {}
    for portgroup in hconfig.Network.Portgroup:
        host_portgroups[portgroup.Spec.Name] = portgroup
        continue
    host_vs_keys = set(host_portgroups.keys())
    conf_keys = set(config['portgroup'].keys())
    missing_from_host = conf_keys.difference(host_vs_keys)
    missing_from_conf = host_vs_keys.difference(conf_keys)
    for v in missing_from_host:
        print(indent + 'Portgroups existing in the config, but not on the '
              'host:')
        print(indent + indent + v)
        continue
    for v in missing_from_conf:
        print(indent + 'Portgroups existing on the host, but not in the '
              'config:')
        print(indent + indent + v)
        continue

    # Find vnic differences between host and config
    host_vnics = {}
    for vnic in hconfig.Network.Vnic:
        host_vnics[vnic.Portgroup] = vnic
        continue
    vnic_keys = []
    for pg in conf_keys:
        for k in config['portgroup'][pg].keys():
            if k.startswith('_vnic.'):
                vnic_keys.append(pg)
                break
            continue
        continue
    host_vnic_keys = set(host_vnics.keys())
    conf_vnic_keys = set(vnic_keys)
    missing_vnic_from_host = conf_vnic_keys.difference(host_vnic_keys)
    missing_vnic_from_conf = host_vnic_keys.difference(conf_vnic_keys)
    for v in missing_vnic_from_host:
        print(indent + 'Portgroups with Vnics existing in the config, but not '
              'on the host:')
        print(indent + indent + v)
        continue
    for v in missing_vnic_from_conf:
        print(indent + 'Portgroups with Vnics existing on the host, but not '
              'in the config:')
        print(indent + indent + v)
        continue

    vnic_intersection = conf_keys.intersection(host_vnic_keys)
    vnic_types = pillage.pillage_vnic_types(hconfig)
    for vkey in conf_keys.intersection(host_vs_keys):
        section = indent + '[' + vkey + ']'
        lines = []
        for k, v in config['portgroup'][vkey].items():
            # Keys beginning with an underscroe are special.
            # If the keys is a _vnic, compare the values if needed.
            l = ''
            special = k.startswith('_')
            if special:
                if vkey in vnic_intersection:
                    if k.startswith('_vnic._type.'):
                        nic_type = k[len('_vnic._type.'):]
                        pg_dev = host_vnics[vkey].Device
                        htype_value = pg_dev in vnic_types[nic_type]
                        if htype_value != v:
                            l = "%s%s %s: %s (config: %s)" % \
                                (indent, indent, k, str(htype_value), str(v))
                    elif k.startswith('_vnic.'):
                        l = compare_attribute(host_vnics[vkey],
                                              k[len('_vnic.'):], v, indent)
                    pass
                if l:
                    lines.append(l)
                continue
            l = compare_attribute(host_portgroups[vkey], k, v, indent)
            if l:
                lines.append(l)
            continue
        if lines:
            print(section)
            print('\n'.join(lines))
        continue


def do_verify(config, opts, client):
    """ Verify running config against config file. """
    vhost = conf.get_value(opts, config, 'vhost', prompt=False)
    hosts = api.get_hosts(client, vhost)

    print('')
    vswitches = config['vswitch']
    portgroups = config['portgroup']
    for host in hosts:
        print("Verifying config on %s ... " % host.Name)
        verify_vswitches(host.Config, config)
        verify_portgroups(host.Config, config)
        continue


