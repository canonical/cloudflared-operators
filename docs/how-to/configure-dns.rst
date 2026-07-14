.. meta::
   :description: How to configure DNS resolution for the Cloudflare tunnel used by the cloudflared charm.

.. _how_to_configure_dns:

How to configure DNS
====================

By default, the ``cloudflared`` charm uses the Kubernetes cluster's internal DNS 
(``kube-dns.kube-system.svc``) to resolve internal service names when routing traffic from
Cloudflare to your applications.

If your architecture requires the tunnel to resolve names using a specific external DNS server or a
custom internal DNS, you can override this behavior using the ``cloudflare-configurator`` charm.

To configure a custom DNS resolver, set the ``nameserver`` configuration option on the
``cloudflare-configurator`` charm:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=8.8.8.8

After you run this configuration, the nameserver is set as follows:

1. The ``cloudflare-configurator`` charm passes the configured nameserver to the ``cloudflared``
charm via the ``cloudflared-route`` relation.
2. The ``cloudflared`` charm writes this nameserver into a dedicated ``resolv.conf`` file located
at ``/var/snap/charmed-cloudflared/current/etc/resolv.conf``.
3. The ``cloudflared`` snap instance uses this configuration to resolve domain names when
establishing routes to your internal services.

To revert to the default Kubernetes DNS, simply unset the configuration:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=""
