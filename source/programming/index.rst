VMware vSphere Programming via Python
======================================

VMware vSphere can be managed via multiple means.  The most common of which is
via the vSphere Client. Any setting can be configured via the vSphere Client.
However, the vSphere Client is not geared for automation nor for repetitive
tasks.

Other options, geared more towards automation and repition are:

  `vSphere CLI`_
    Perl scripts that can be installed on Linux or Windows.  Many, but not
    all, tasks and settings can be manipulated via the CLI.

  vMA_
    Virtual Machine with the `vSphere CLI`_ preinstalled

  PowerCLI_
    PowerShell cmdlets for managing vSphere.  Also includes .NET assemblies.
    All tasks that can be done via the vSphere Client can be done via
    PowerShell or the .NET assemblies.  However, some tasks are cumbersome.

  `VIX API`_
    High level API for Windows or Linux.  Bindings for C, Perl, and COM are
    provided.

  `Web Services SDK`_
    Complete Web API for managing all of vSphere.  The PowerCLI_ and .NET
    bindings use the `Web Services SDK`_.

All of the options above have different trade-offs.  The `vSphere CLI`_,
vMA_, and `VIX API`  aren't complete, though mostly so.  The PowerCLI_ is
cumbersome to use. The `Web Services SDK`_ is complete, but complex.
Especially if your chosen language doesn't have a Web Services implementation.

Fortunately, thanks to the advent of IronPython_, the .NET assemblies can be
used to access the `Web Services SDK`_ without having to deal with the hassle
that is PowerShell.


Purpose
-------

Provide information necessary to understand the way the VMware API works,
especially with regrards to intergration with IronPython_.



Contents:
---------
.. toctree::
   :maxdepth: 2

   boilerplate
   entities
   mor
   networking

