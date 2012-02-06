**********************
Inflight Entertainment
**********************

Host Networking
===============

When dealing with the host networking config, we first start off with an
HostSystem_ :term:`managed entity`.

::

  filter = NameValueCollection()
  filter.Add('Name', 'lothlorien')
  host_system = client.FindEntityView(VMware.Vim.HostSystem, None, filter, None)

The above selected the HostSystem_ :term:`Managed Entity` which
corresponds to the host whose name contains ``lothlorien``.  The
HostSystem_ object gives us access to multiple *MOR*\s.

``host.ConfigManager.NetworkSystem``

Data Objects
============

``NetworkConfig.Vswitch``

 **Properties**

 - Name
 - Spec

   - Policy

     - NicTeaming

``NetowrkConfig.Portgroup``

 **Properties**

 - Spec

   - Name
   - VlanId
   - VswitchName
   - Policy

     - Security

       - AllowPromiscuous
       - ForgedTransmits
       - MacChanges


``NetworkConfig.Vnic``

 **Properties**

 - Device
 - Portgroup
 - Spec

   - Ip

     - Dhcp
     - IpAddress
     - IpV6Config
     - SubnetMask

   - Mtu
   - Portgroup
   - TsoEnabled

``NetworkConfig.Pnic``

VNic Stuff
==========

``host.ConfigManager.VirtualNicManager`` produces a HostVirtualNicManager_.
The HostVirtualNicManager_ contains methods for selecting the vnics used for
vMotion, Management, and Fault Tolerance.

Find the vnic used for vMotion::

  vnm = client.GetView(host.ConfigManager.VirtualNicManager, None)
  vmotion_nic = vnm.QueryNetConfig('vmotion')

This gives us a VirtualNicManagerNetConfig_ object.  The
VirtualNicManagerNetConfig_ object tells us the following information;

- ``.NicType``: The ``nicType``; ``management``, ``vmotion``, or
  ``faultToleranceLogging``.

- ``.MultiSelectAllowd``: Whether or not multiple vnics are allowed to be
  selected for the given ``nicType``.

- ``.CandidateVnic``: A list of HostVirtualNic_ objects that are available to
  be selected.

- ``.SelectedVnic``: An Array[str] of vnic ``Key`` strings that are selected
  for the given nic type.

The ``Key`` value stored in the ``.SelectedVnic`` Array is not available via
``NetworkConfig.Vnic``.  Neither is the ``Key`` values passed to
``DeselectVnicForType`` nor ``SelectVnicForType``. ``DeselectVnicForType`` and
``SelectVnicForType`` us the ``Device`` name.

Fortunately, the HostVirtualNic_ object contains the ``Device`` name, ``Key``
and the ``Portgroup`` of the vnic.  To associate the selected nic with a given
portgroup, one can loop through the ``.CandidateVnic`` list and look for the
vnic with the selected key.

Select a Vnic for a given use::

  mgmt_nic = vnm.QueryNetConfig('management')
  dev = None
  for candidate in mgmt_nic.CandidateVnic:
      if candidate.Portgroup == 'EG_MGMT':
          dev = candidate.Device
          break
      continue
  if dev:
      vnm.SelectVnicForNicType('management', dev)

Translate the Selected Vnic for the Management interface into its
corresponding Vnic device name::

  mgmt_nic = vnm.QueryNetConfig('management')
  dev = None
  for candidate in mgmt_nic.CandidateVnic:
      if candidate.Key == mgmt_nic.SelectedVnic[0]:
          dev = candidate.Device
          break
      continue
  print("Mangement Vnic Device Name: %s" % dev)

