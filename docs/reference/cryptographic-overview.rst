.. meta::
   :description: An overview of the cryptographic components used by the Cloudflared charms.

.. _reference_cryptographic_overview:

Cryptographic overview
======================

The charms do not implement cryptographic protocols. Juju protects the tunnel
credential as a secret, and ``cloudflared`` establishes the encrypted tunnel to
Cloudflare. Refer to the `Cloudflare Tunnel documentation <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/>`_
for protocol and certificate details.
