.. meta::
   :description: Deploy and integrate the cloudflared and cloudflare-configurator Juju charms.

.. _tutorial_basic_deployment:

Deploy the cloudflared charms
==============================

This tutorial deploys the ``cloudflared`` subordinate machine charm and the
``cloudflare-configurator`` charm. It assumes that a principal application
named ``frontend`` is already deployed in a machine-cloud model and provides
``juju-info`` while requiring ``ingress``.

What you'll do
--------------

1. Create an isolated Juju model.
2. Deploy both Cloudflare charms.
3. Integrate the charms with the ``frontend`` application.
4. Configure the tunnel secret and public hostname.
5. Verify the deployment status.

What you'll need
----------------

- Juju 3.x connected to a controller with a machine cloud.
- A machine where the subordinate ``cloudflared`` charm can run.
- A principal application named ``frontend`` that provides ``juju-info`` and
  requires ``ingress``.
- A Cloudflare Tunnel token in the ``CLOUDFLARE_TUNNEL_TOKEN`` environment
  variable.
- A hostname in the Cloudflare zone in ``CLOUDFLARE_PUBLIC_HOSTNAME``.

Set up the environment
----------------------

Create and select a model for this tutorial:

.. code-block:: bash

   juju add-model cloudflare-tutorial
   juju switch cloudflare-tutorial

Deploy the charms
-----------------

Deploy both charms from Charmhub:

.. code-block:: bash

   juju deploy cloudflared
   juju deploy cloudflare-configurator

Integrate the charms
--------------------

Attach the subordinate and connect the configurator to the frontend and
workload charms:

.. code-block:: bash

   juju integrate frontend:juju-info cloudflared:juju-info
   juju integrate frontend:ingress cloudflare-configurator:ingress
   juju integrate cloudflared:cloudflared-route cloudflare-configurator:cloudflared-route

Configure the tunnel
--------------------

Create a Juju secret, grant it to the configurator, and configure the hostname:

.. code-block:: bash

   secret_id="$(juju add-secret cloudflare-tunnel tunnel-token="$CLOUDFLARE_TUNNEL_TOKEN" | awk '/secret:/ {print $1}')"
   juju grant-secret "$secret_id" cloudflare-configurator
   juju config cloudflare-configurator tunnel-token="$secret_id" domain="$CLOUDFLARE_PUBLIC_HOSTNAME"

Verify the deployment
---------------------

Run ``juju status`` to check the current status and relations:

.. code-block:: bash

   juju status --relations

A healthy deployment has the subordinate attached to ``frontend``, an active
configurator unit, and connected ``cloudflared-route`` and ``ingress``
relations. The exact unit addresses and machine IDs depend on the model. A
successful status has the following shape:

.. code-block:: text

   App                     Version  Status  Scale  Charm
   cloudflare-configurator          active      1  cloudflare-configurator
   cloudflared                       active      1  cloudflared
   frontend                          active      1  frontend

   Relation                      Provides                 Consumes
   cloudflared-route             cloudflare-configurator  cloudflared
   ingress                       cloudflare-configurator  frontend
   juju-info                     frontend                  cloudflared

Clean up the environment
------------------------

Destroy the model when you finish:

.. code-block:: bash

   juju destroy-model cloudflare-tutorial --destroy-storage --force

Next steps
----------

- Learn how to :ref:`configure custom DNS settings <how_to_configure_dns>`.
- Learn how to :ref:`expose a front-end application <how_to_expose_frontend>`.
- Learn how to :ref:`use the configurator charm <how_to_use_configurator>`.
