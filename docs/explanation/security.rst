.. meta::
   :description: Understand the security design, risks, and best practices for the Cloudflared charms.

.. _explanation_security:

Security overview
=================

Tunnel credentials are stored in Juju secrets. The secret must contain a
``tunnel-token`` key and must be granted to the application that consumes it.

The configurator reads the secret and sends the token through the
``cloudflared-route`` relation. The subordinate writes the token to the
``charmed-cloudflared`` snap configuration on the principal application's
machine.

For Cloudflare-specific tunnel security guidance, see the `Cloudflare Tunnel documentation
<https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/>`_.
