.. meta::
   :description: How to redeploy the Cloudflared charms in a new Juju model.

.. _how_to_redeploy:

How to redeploy
===============

The charms do not own persistent application data. To redeploy them in a new
model:

1. Deploy ``cloudflared`` and ``cloudflare-configurator`` from Charmhub.
2. Recreate the principal application's ``juju-info`` relation to
   ``cloudflared``.
3. Recreate the ``cloudflared-route`` relation between the two charms.
4. Recreate the ``ingress`` relation between the configurator and the frontend
   application, when one is used.
5. Restore the Juju secret, grant it to ``cloudflare-configurator``, and reapply
   ``domain`` and ``nameserver``.

Use the same Cloudflare Tunnel token to reconnect to the existing tunnel.
Verify the restored model with:

.. code-block:: bash

   juju status --relations
