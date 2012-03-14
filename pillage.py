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


__all__ = ['do_pillage',]

def pillage_vswitch_config(hconfig, config):
    """ Pull the Vswitch configuration """

    vswitch_section = {}
    for vswitch in hconfig.Network.Vswitch:
        section = {}
        vswitch_section.setdefault(vswitch.Name, {})
        section['Name'] = vswitch.Name
        section['Spec.Mtu'] = vswitch.Spec.Mtu
        section['Spec.NumPorts'] = vswitch.Spec.NumPorts
        section['Spec.Policy.NicTeaming.NicOrder.ActiveNic'] = \
                [nic for nic in
                    vswitch.Spec.Policy.NicTeaming.NicOrder.ActiveNic]
        section['Spec.Policy.NicTeaming.NicOrder.StandbyNic'] = \
                vswitch.Spec.Policy.NicTeaming.NicOrder.StandbyNic
        section['Spec.Policy.NicTeaming.Policy'] = \
                vswitch.Spec.Policy.NicTeaming.Policy
        section['Spec.Policy.Security.AllowPromiscuous'] = \
                vswitch.Spec.Policy.Security.AllowPromiscuous
        section['Spec.Policy.Security.ForgedTransmits'] = \
                vswitch.Spec.Policy.Security.ForgedTransmits
        section['Spec.Policy.Security.MacChanges'] = \
               vswitch.Spec.Policy.Security.MacChanges
        vswitch_section[vswitch.Name] = section
        continue
    config.setdefault('vswitch', {})
    config['vswitch'] = vswitch_section
    pass


def pillage_vnic_types(hconfig):
    """ Pull the vnic type information.

    Returns a dictionary containing information on the ``management``,
    ``faultToleranceLogging`` and ``vmotion`` nics.
    """
    nic_types = {}
    for ntype in hconfig.VirtualNicManagerInfo.NetConfig:
        nic_types[ntype.NicType] = []
        for candidate in ntype.CandidateVnic:
            if not ntype.SelectedVnic:
                nic_types[ntype.NicType] = []
            else:
                for selected_nic in ntype.SelectedVnic:
                    if candidate.Key == selected_nic:
                        nic_types[ntype.NicType].append(candidate.Device)
                    continue
            continue
    return nic_types


def pillage_vnics(hconfig, config):
    """ Pull the vnic configuration. """

    nic_types = pillage_vnic_types(hconfig)
    vnics = {}
    pgconf = config['portgroup']
    for vnic in hconfig.Network.Vnic:
        pg = vnic.Portgroup
        pgconf[pg]['_vnic.Portgroup'] = pg
        pgconf[pg]['_vnic._type.faultToleranceLogging'] = \
               vnic.Device in nic_types['faultToleranceLogging']
        pgconf[pg]['_vnic._type.vmotion'] = \
               vnic.Device in nic_types['vmotion']
        pgconf[pg]['_vnic._type.management'] = \
               vnic.Device in nic_types['management']
        pgconf[pg]['_vnic.Spec.Mtu'] = vnic.Spec.Mtu
        pgconf[pg]['_vnic.Spec.Portgroup'] = vnic.Spec.Portgroup
        pgconf[pg]['_vnic.Spec.TsoEnabled'] = vnic.Spec.TsoEnabled
        pgconf[pg]['_vnic.Spec.Ip.Dhcp'] = vnic.Spec.Ip.Dhcp
        pgconf[pg]['_vnic.Spec.Ip.IpAddress'] = vnic.Spec.Ip.IpAddress
        pgconf[pg]['_vnic.Spec.Ip.IpV6Config'] = vnic.Spec.Ip.IpV6Config
        pgconf[pg]['_vnic.Spec.Ip.SubnetMask'] = vnic.Spec.Ip.SubnetMask
        continue
    pass


def pillage_portgroup_config(hconfig, config):
    """ Pull the Portgroup configuration """

    pg_section = {}
    for pg in hconfig.Network.Portgroup:
        section = {}
        pg_section.setdefault(pg.Spec.Name, {})
        section['Spec.Name'] = pg.Spec.Name
        section['Spec.VlanId'] = pg.Spec.VlanId
        section['Spec.VswitchName'] = pg.Spec.VswitchName
        section['Spec.Policy.Security.AllowPromiscuous'] = \
                pg.Spec.Policy.Security.AllowPromiscuous
        section['Spec.Policy.Security.ForgedTransmits'] = \
                pg.Spec.Policy.Security.ForgedTransmits
        section['Spec.Policy.Security.MacChanges'] = \
                pg.Spec.Policy.Security.MacChanges
        pg_section[pg.Spec.Name] = section
        continue
    config.setdefault('portgroup', {})
    config['portgroup'] = pg_section
    pillage_vnics(hconfig, config)
    pass


def do_pillage(config, opts, client):
    """ Pull the config from the specified VMware host and save it in the
    config.

    If no VMware host server was specified, it will pull the config from the
    first host returned from FindEntityView.

    """
    vhost = conf.get_value(opts, config, 'vhost', prompt=False)
    host = api.get_host(client, vhost)

    pillage_vswitch_config(host.Config, config)
    pillage_portgroup_config(host.Config, config)

    config.write()
