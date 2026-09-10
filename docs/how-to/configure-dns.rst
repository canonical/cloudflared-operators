.. meta::
   :description: How to configure DNS resolution for the Cloudflare tunnel used by the cloudflared charm.

.. _how_to_configure_dns:

How to configure DNS
====================

The configurator passes a configured nameserver to ``cloudflared`` through the
``cloudflared-route`` relation. If no nameserver is configured, it tries to
resolve ``kube-dns.kube-system.svc``. On a machine cloud where that name is not
available, the workload uses the host resolver configuration.

This guide assumes that the ``cloudflared`` and ``cloudflare-configurator``
charms are deployed and integrated.

Set a custom resolver
---------------------

Set the ``nameserver`` option on the configurator:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=8.8.8.8

The workload writes the value into the resolver file for each installed snap
instance. The instance name depends on whether it comes from direct
configuration or a relation-backed tunnel.

To return to the host resolver configuration, unset the option:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=""
