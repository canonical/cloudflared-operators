.. meta::
   :description: Understand the security design, risks, and best practices for the Cloudflared charms.

.. _explanation_security:

Security overview
=================

Tunnel credentials are stored in Juju secrets. The secret must contain a
``tunnel-token`` key, and access must be granted only to the application that
needs it. Do not place the token in a model configuration file, a shell command
literal, or a public document.

The configurator reads the secret and sends the token through the private
``cloudflared-route`` relation. The subordinate writes the token to the
``charmed-cloudflared`` snap configuration on the principal application's
machine. Protect access to that machine and use Juju's normal model and secret
permissions.

The charms do not implement Cloudflare's cryptographic protocols. For
Cloudflare-specific tunnel security guidance, see the `Cloudflare Tunnel documentation
<https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/>`_.
