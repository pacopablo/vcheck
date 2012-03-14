********
API Docs
********

vCheck provides a Python package for interacting with and managing vCenter via
Python objects.  The API is modeled after the main objects in a vCenter
deployment.  Namely:

 |datacenterapi|:

   Models the datacenter.  Allows operations on various stuff

 |hostapi|:

   Host based operations such as networking, datastores, user management, etc.

 |vmapi|:

   VM operations such as start/stop/provision.

All top level objects require a


.. toctree::
   :maxdepth: 2

   connection
   datacenter
   host
   vm
