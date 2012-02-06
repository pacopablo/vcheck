********
Climbing
********

Once connected to the vCenter server via a ``VimClient``, we can begin work.
When working with vCenter, we are dealing with two types of objects: |mo|\s,
and |do|\s.

|MO|\s come in two varieties: Managed Entities and Managed Object *"service
providers"*.  Managed Entities represent pieces of **inventory** such as
HostSystem_, VirtualMachine_, and Datastore_. Managed Object *"service
providers"* are properties of |me|\s and provide |mor|\s needed to interact
with vCenter. begins with retreiving a |ME| object::

Retrieving Managed Entities
===========================

To find a |me| we use the ``FindEntityView`` or ``FindEntityViews`` method of
the ``VimClient``.

::

  hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, None, None)

A ``VMware.Vim.HostSystem`` is a |ME|.  The available entities are:

- ``ComputeResource``: Represents a set of physical compute resources for a
  set of virtual machines.

- ``Datacenter``: Provides the interface to the common container object for
  hosts, virtual machines, networks, and datastores.

- ``Datastore``: Represents a storage location for virtual machine files. A
  storage location can be a VMFS volume, a directory on Network Attached
  Storage, or a local file system path.

- ``DistributedVirtualSwitch``: The interface to the distributed virtual
  switch objects.

- ``Folder``: container for storing and organizing inventory objects.
  Folders can contain folders and other objects.

- ``HostSystem``: provides access to a virtualization host platform.

- ``Network``: Represents a network accessible by either hosts or virtual
  machines. This can be a physical network or a logical network, such as
  a VLAN.

- ``ResourcePool``: Represents a set of physical resources: a single host,
  a subset of a host's resources, or resources spanning multiple hosts.

- ``VirtualMachine``: VirtualMachine is the managed object type for
  manipulating virtual machines, including templates that can be
  deployed (repeatedly) as new virtual machines. This type provides
  methods for configuring and controlling a virtual machine.


We can also use filters to limit the results of ``FindEntityViews``.  For
example, if we only want hosts that have a name of  *esxi.example.org* we can
create a filter::

  filter = NameValueCollection()
  filter.Add("Name", "esxi.example.org")
  hosts = client.FindEntityViews(VMware.Vim.HostSystem, None, filter, None)

Additionally, regexes can be used in the filter.  When using a filter, one
must be careful regarding the key used.  It must match a property path.  I am
not aware of a document or method for determining all of the property paths
available.


Using Managed Object *"service providers"*
==========================================

Once we ahve a |me|, we can begin to look at both the configuration values, as
well as manipulate settings on the vCenter server.  |ME|\s contain Managed
Object *"service providers"*.  The *"service providers"*, in turn, contain
:ref:`Managed Object References (MORs) <mor>` which are used to manipulate the
settings on the vCenter server.

For most of our work we will be mainly interested in the ``ConfigManager``
*"service provider"* of the ``HostSystem`` |me|.

::

  >>> hosts[0]
  <VMware.Vim.HostSystem object at 0x000000000000017B [VMware.Vim.HostSystem]>
  >>> cm = hosts[0].ConfigManager
  >>> cm
  <VMware.Vim.HostConfigManager object at 0x000000000000017C [VMware.Vim.HostConfigManager]>
  >>> cm.NetworkSystem
  <VMware.Vim.ManagedObjectReference object at 0x000000000000017D [HostNetworkSystem-networkSystem-45]>


