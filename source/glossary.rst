********
Glossary
********

.. glossary::
   :sorted:

   Managed Object
      Core data structure to the VMware API.  There are two main categories:

      - :term:`Managed Entity <Managed Entity>`: compoents that comprise the
        inventory of virtual systems.
      - Managed objects that provide services for the entire system.

      More information on managed objects can be found in
      :ref:`Further Reading <further_reading>`.

   Managed Entity
      Components that comprise the **inventory** of virtual components.  The
      known Managed Entities are:

      - ComputeResource_; Represents a set of physical compute resources for a
        set of virtual machines.

      - Datacenter_: Provides the interface to the common container object for
        hosts, virtual machines, networks, and datastores.

      - Datastore_: Represents a storage location for virtual machine files. A
        storage location can be a VMFS volume, a directory on Network Attached
        Storage, or a local file system path.

      - DistributedVirtualSwitch_: The interface to the distributed virtual
        switch objects.

      - Folder_: container for storing and organizing inventory objects.
        Folders can contain folders and other objects.

      - HostSystem_: provides access to a virtualization host platform.

      - Network_: Represents a network accessible by either hosts or virtual
        machines. This can be a physical network or a logical network, such as
        a VLAN.

      - ResourcePool_: Represents a set of physical resources: a single host,
        a subset of a host's resources, or resources spanning multiple hosts.

      - VirtualMachine_: VirtualMachine is the managed object type for
        manipulating virtual machines, including templates that can be
        deployed (repeatedly) as new virtual machines. This type provides

   Data Object
      *Improve*: Holds the actual information about a specific piece of the system.  Data
      Objects don't have methods [1]_ and aren't used to invoke operations on
      the vCenter server.  They are generally used as parameters which hold
      the information to update.

   Managed Object Reference
      A |DO| that provides a reference to the server-side objects used by
      client applications.

.. rubric:: Footnotes

.. [1] *Improve*: There may be a :term:`Data Object` with methods, however, interaction
       with the SDK is generally done via |MOR|\s
