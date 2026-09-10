.. meta::
   :description: Troubleshoot common Cloudflared charm deployment and tunnel issues.

.. _how_to_troubleshoot:

How to troubleshoot
===================

Start with Juju status and the relation graph:

.. code-block:: bash

   juju status --relations
   juju debug-log --replay

Check the following conditions:

* ``cloudflared`` must have an active ``juju-info`` relation to a principal
  application.
* ``cloudflared-route`` must be related, unless the workload uses its direct
  ``tunnel-token`` configuration.
* The configured Juju secret must contain ``tunnel-token`` and be granted to
  the consuming application.
* ``cloudflare-configurator`` needs both ``domain`` and ``tunnel-token`` before
  it publishes ingress data or sends route data.
* A nameserver supplied by the configurator must resolve the intended origin
  names. Unset ``nameserver`` to use the host resolver when the Kubernetes DNS
  service is not available.
* Check the configured snap channel when a snap instance cannot be installed or
  refreshed.

If Juju reports an active workload but external requests fail, check the
Cloudflare tunnel connection, DNS record, and Cloudflare-side origin route.
Those settings are outside the charm relation data.
