.. meta::
   :description: How to configure DNS resolution for the Cloudflare tunnel used by the cloudflared charm.

.. _how_to_configure_dns:

How to configure DNS
====================

By default, the ``cloudflare-configurator`` charm tries to resolve the
Kubernetes DNS service, ``kube-dns.kube-system.svc``. If the lookup is not
available on a machine cloud, ``cloudflared`` uses the host resolver
configuration instead.

If the tunnel must resolve names through a specific external or internal DNS
server, override the default with the ``nameserver`` option. This guide assumes
that the ``cloudflared`` and ``cloudflare-configurator`` charms are deployed and
integrated.

Set a custom DNS resolver
-------------------------

Configure the resolver on ``cloudflare-configurator``:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=8.8.8.8

After this configuration:

1. ``cloudflare-configurator`` sends the nameserver to ``cloudflared`` through
   the ``cloudflared-route`` relation.
2. ``cloudflared`` writes it to the resolver file for each installed
   ``charmed-cloudflared`` snap instance.
3. The snap instance uses the resolver when resolving names for its tunnel.

The instance path is based on the tunnel source. Direct configuration uses the
``charmed-cloudflared_config0`` instance, while relation-backed tunnels use an
instance named with the relation ID. The resolver file is stored under
``/var/snap/<instance>/current/etc/resolv.conf``.

To return to the default behavior, unset the option:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=""
