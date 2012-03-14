.. _vmware_connection:

***********
Connection
***********

.. py:module:: vmware
   :platform: Windows

.. py:class:: VimConnection(url, username, password)

   When instantiating a :py:class:`VimConnection` object, it requires a URL to
   the vCenter or ESXi web service.  The web services is usually located at

   ::

     https://<vcenter_or_esxi_host>/sdk

   The username and password are also required.  Upon instantiation, the
   :py:class:`VimConnection` object will log into the vCenter or ESXi host.
   All other classes use a :py:class:`VimConnection` object to interact with
   vCenter and ESXi hosts.

   .. py:attribute:: connection (read-only)

      ``VMWare.Vim.VimClient`` |mo|.  If the :py:class:`VimConnection` was
      unable to connect, this will be ``None``.  Classes must use
      :py:attr:`vmware.VimConnection.connection` as the connection to the
      vCenter or ESXi host.