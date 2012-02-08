****************
Pre-Flight Check
****************

Before any real work can be done, an IronPython Script needs to load the .NET
assemblies and connect to a vCenter server or ESX(i) host.  Connecting to an
ESXi server with a free license is possible.  However, while one can query the
configuration, one can not change the configuration [1]_.

Loading Assemblies
==================

As with other .NET assemblies and IronPython, a reference needs to be added to
the ``clr``.  Additionally, the ``NameValueCollection`` is used in filters, so
we need to import that as well. Finnaly, we import ``Arrary`` from ``System``
as it is used in many objects.

::

  import clr
  clr.AddReference('VMware.Vim')
  from System.Collections.Specialized import NameValueCollection
  from System import Array
  import VMware.Vim


Connecting to vCenter
=====================

When connecting to the vCenter (or ESXi) server, we need the *service URL* as
well as login credentials. The steps for conencting are:

- Create a ``VimClient`` object
- ``Connect`` to the *service URL*
- ``Login`` to the vCenter server.

Example code::

  client = VMware.Vim.VimClient()
  client.Connect('https://vcenter.example.org/sdk')
  client.Login('administrator', 'password')

As we can see, the *service URL* is simply the vCenter server with ``/sdk``
appended.  It is possible to configure the vCenter server for use over
``http://``, but it is not recommended.

Additionally, the ``client`` object becomes our main point of contact with the
vCenter server.  Through the ``client`` object we can load Virtual Machine
objects, Host objects, and other objects.

.. rubric:: Footnotes

.. [1] It may be possible to change some configuration options.  Networking
       changes result in a *RestrictedVersion* error.
