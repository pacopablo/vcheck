.. _mor:

****************
Crusing Altitude
****************

Managed Object References
=========================

|MOR|\s allow us to get objects that can be used to modify the state of the
vCenter server.  With a |mor| one can use the ``VimClient.GetView`` and
``VimClient.GetViews`` methods to get object for updating configuration.  The
two |mor|\s that we will be using most are ``NetworkSystem`` and
``VirtualNicManager``.

::

  cm = hosts[0].ConfigManger
  ns = client.GetView(cm.NetworkSystem, None)
  vnm = client.GetView(cm.VirtualNicManger, None)

A filter can also be passed as the second parameter to ``GetView``.

Once we have the *view*, we can modify state on the server.  The following
example changes the VLAN ID of the specified portgroup::

  ns.NetworkConfig.Portgroup[0].Spec.VlanId = 460
  ns.UpdatePortGroup(ns.NetworkConfig.Portgroup[0].Spec.Name, ns.NetworkConfig.Portgroup[0].Spec)


