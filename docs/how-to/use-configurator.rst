.. meta::
   :description: Configure Cloudflare Tunnel credentials, DNS, and ingress with the cloudflare-configurator charm.

.. _how_to_use_configurator:

Use the cloudflare-configurator charm
=====================================

The ``cloudflare-configurator`` charm manages the settings consumed by the
``cloudflared`` subordinate. It sends the tunnel token and optional DNS
resolver across ``cloudflared-route`` and publishes the configured public URL
through ``ingress``.

Prerequisites
-------------

Deploy and integrate both charms. The :ref:`basic deployment tutorial
<tutorial_basic_deployment>` shows the complete relation setup.

Set the public hostname
-----------------------

Set the hostname that should be published to the related frontend application:

.. code-block:: bash

   juju config cloudflare-configurator domain="$CLOUDFLARE_PUBLIC_HOSTNAME"

The configurator publishes the HTTPS hostname after both ``domain`` and
``tunnel-token`` are configured.

Configure DNS resolution
------------------------

Set ``nameserver`` when the tunnel must resolve origin names through a specific
resolver:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=8.8.8.8

Unset the option to use the resolver configuration of the host machine when the
Kubernetes DNS service is unavailable:

.. code-block:: bash

   juju config cloudflare-configurator nameserver=""

Update tunnel credentials
-------------------------

The ``tunnel-token`` option must refer to a Juju secret containing a key named
``tunnel-token``. Grant the secret to ``cloudflare-configurator`` before setting
the option. For example, when ``CLOUDFLARE_TUNNEL_TOKEN`` is already set in
the shell:

.. code-block:: bash

   secret_id="$(juju add-secret cloudflare-tunnel tunnel-token="$CLOUDFLARE_TUNNEL_TOKEN" | awk '/secret:/ {print $1}')"
   juju grant-secret "$secret_id" cloudflare-configurator
   juju config cloudflare-configurator tunnel-token="$secret_id"

Do not put the token directly in a documentation example or public
configuration file.
