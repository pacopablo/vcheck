vCheck Documentation
=============================

Overview
--------

vCheck is an IronPython_ script to assist in managing a VMware vShpere
infrastructure.  It focuses on auditing configurations and adjusting
configurations based on and INI style configuration file.

Eaxmple Usage
--------------

Pull the existing configuration from an ESXi host::

  C:\Users\pacopablo\vcheck> ipy vcheck.py --retrieve --server=esxi.example.org esxi_config.ini


Verify the configuration of an ESXi host against a configuraiton stored in an
existing configuration file::

  C:\vcheck> ipy vcheck.py --verify --server=esxi.example.org esxi_config.ini


Update the ESXi configuration to match that in the specified configuration
file::

  C:\vcheck> ipy vcheck.py --repair esxi_config.ini


Structure
---------

The documentation is split into three secions:

1. Command usage
2. Code documentation
3. Programming with VMware SDK


Contents:
---------
.. toctree::
   :maxdepth: 2

   programming/index

   further_reading
   glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


