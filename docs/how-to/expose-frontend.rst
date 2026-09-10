.. meta::
   :description: Expose an application through a Cloudflare Tunnel managed by Juju.

.. _how_to_expose_frontend:

Expose a front-end application
==============================

The ``cloudflare-configurator`` charm publishes a public URL to a frontend
application through its ``ingress`` relation. The ``cloudflared`` subordinate
runs the Cloudflare Tunnel process on the principal application's machine.
Cloudflare-side DNS and origin routing remain part of the tunnel setup.

Prerequisites
-------------

- A deployed frontend application named ``frontend`` that requires the
  ``ingress`` interface and provides ``juju-info``.
- The ``cloudflared`` and ``cloudflare-configurator`` charms are deployed and
  integrated.
- A tunnel token is configured on ``cloudflare-configurator``.

Set the public hostname
-----------------------

Store the hostname in ``CLOUDFLARE_PUBLIC_HOSTNAME`` and configure the
charm:

.. code-block:: bash

   juju config cloudflare-configurator domain="$CLOUDFLARE_PUBLIC_HOSTNAME"

Connect the application to the configurator's ingress endpoint:

.. code-block:: bash

   juju integrate frontend:ingress cloudflare-configurator:ingress

The configurator publishes the configured HTTPS hostname to the relation. The
frontend application consumes that URL through its ingress provider.

Verify external access
----------------------

1. Configure the matching DNS record and origin route in Cloudflare.
2. Confirm that the tunnel is connected in Cloudflare.
3. Open the configured HTTPS hostname and verify that the frontend responds.
4. If the request fails, run ``juju status --relations`` and check the
   :ref:`troubleshooting guide <how_to_troubleshoot>`.
